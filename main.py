import argparse
import pymesh as pm

from python.utils.utils import time_it
from python.pc.consts import Dirs
from python.pc.point_cloud import PointCloud
from python.frontend.gui import launch_main_win_streamlit, draw_line_3d

parser = argparse.ArgumentParser(description='Nlattice is a 3D mesh latticing lib. Read more here: ' +
                                             'https://github.com/topologicalhurt/nlattice-internals')
parser.add_argument('--no-gui', action='store_true', help='Flag which determines if GUI is on or off')
parser.add_argument('--cache-pmesh', action='store_false', help='Flag which determines if object is cached in out')
parser.add_argument('--test', action='store_true', help='Flag which determines to display a test intersection')
args = parser.parse_args()


class SharedPc:
    """"Basic PTR pattern - points to the point cloud so main() doesn't have to be encapsulated in a class"""
    def __init__(self):
        self._pc = None

    def set_pc(self, pc: pm.Mesh):
        self._pc = pc

    def get_pc(self):
        return self._pc


@time_it
def main(spc: SharedPc):
    pc = PointCloud(mod_fname=Dirs.MODEL_FDIR)
    spc.set_pc(pc)

    if args.test:
        print('Running benchmark on mesh...')
        pc.intersect_pmesh()
    else:
        print('Creating mesh point point cloud...')
        pc.create()

    if args.cache_pmesh:
        print('Caching pmesh...')
        pc.save_pmesh()


if __name__ == '__main__':
    shared_pc = SharedPc()
    main(shared_pc)
    point_cloud = shared_pc.get_pc()
    if not args.no_gui:
        launch_main_win_streamlit(centroid_coincident=point_cloud.get_centroid_coincident(),
                                  draw_centroid_coincident=True)
