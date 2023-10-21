import regex as re
import pymesh as pm
from sys import version as pyv

if __name__ == '__main__':
    # Support only for python 3.10+
    groups = re.match('^([0-9]+)\.([0-9]+)', pyv).groups()
    # assert int(groups[0]) >= 3 and int(groups[1]) >= 10

    # Basic geom loading in pymesh
    pm.test()
    mesh = pm.load_mesh("test_model.stl")
    print(f'n_verts: {mesh.num_vertices}, n_faces: {mesh.num_faces}, n_vox: {mesh.num_voxels}')
