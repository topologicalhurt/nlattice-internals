import unittest
import random
from generate_surface_mesh import *
import pymesh as pm
import numpy as np

class Test_generate_surface_mesh(unittest.TestCase):

    def test_vertices_connections(self):
        mesh = pm.load_mesh("./python/lattice_generation/stl_assets/bulbasaur.stl")
        vertices, edges = get_wireframe(mesh, 30)

        tet = pm.tetgen()
        tet.points = vertices
        tet.triangles = mesh.faces
        tet.max_tet_volume = slider_to_volume(vertices, max_volume_ratio)
        tet.verbosity = 0
        tet.run()
        new_mesh = tet.mesh
        tetras = new_mesh.voxels
        for i in range(1000):
            random_tetrahedron_index = random.randint(0, len(tetras))
            random_vertex_1 = random.randint(0, 3)
            random_vertex_2 = random.randint(0, 3)

            if random_vertex_1 == random_vertex_2:
                continue
            else:
                self.assertTrue(np.isin(np.array([tetras[random_tetrahedron_index][random_vertex_1],
                                                 tetras[random_tetrahedron_index][random_vertex_2]]),
                                        edges))

