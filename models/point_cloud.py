import pymesh as pm
import inspect
from typing import Optional, NewType
from models.dir_utils import mesh_save_handler, reset_objects_config
from models.consts import Types, Dirs, MetaD


Conf = MetaD.CONFIG


class PointCloud:

    def __init__(self, bmod: Optional[Types.Mesh] = None, mod_fname: Optional[str] = None):
        """
        Parameters:
        - mod: a provided mesh (expected)
        - mod_fname: a file to load the mesh from if a mesh isn't provided
        """
        if not (bmod is None) ^ (mod_fname is None):
            raise ValueError('Illegal argument combination: one of [mod] [mod_fname] must be null (None)!')

        if mod_fname:
            self.mod_fname = mod_fname
            self._bmod = pm.load_mesh(mod_fname)
            self._bmod.enable_connectivity()
        else:
            self._bmod = bmod
        self._pmod = PointCloud._make_pmod(self._bmod)
    
    @staticmethod
    def _make_pmod(bmod: Types.Mesh) -> Types.Mesh:
        """Factory function defining inheritance pattern for the point cloud
        'copy' of the base mesh"""
        class Pmod(pm.Mesh):
            """Define inheritance pattern for the point cloud mesh"""
            def __init__(self, bmod: Types.Mesh):
                super().__init__(bmod._Mesh__mesh)
    
                # Not really necessary to use reflections but use below if that's preferred
                # attr = inspect.getmembers(pm.Mesh, lambda a:not(inspect.isroutine(a)))
                # pub_attr = [a for a in attr if not(a[0].startswith('__') and a[0].endswith('__'))]
                # for a in pub_attr:
                #     self.__setattr__(a[0], a[1])

        return Pmod(bmod)
    
    def change_pmesh(self) -> None:
        bool_mod = pm.load_mesh(Dirs.MODEL2_FDIR)
        csg = pm.CSGTree({
            'intersection': [{'mesh': bool_mod}, {'mesh': self._pmod}]
        })
        self._pmod = csg.mesh
    
    def save_pmesh(self) -> None:
        with mesh_save_handler(self._pmod, 'point_cloud.stl'):
            pass
        
    def get_bmod(self) -> Types.Mesh:
        """Returns the base model mesh before applying PC ops"""
        return self._bmod
    
    def get_pmod(self) -> Types.Mesh:
        """Returns the model after"""
        return self._pmod
