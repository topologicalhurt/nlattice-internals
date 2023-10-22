import pymesh as pm
import numpy as np
import sys
# import matplotlib.pyplot as plt
# from is_inside_mesh import is_inside_turbo as is_inside
# from enum import Enum

def print_wire_data(wn):
    print(f"Dim: {wn.dim}")
    print(f"Vertices: {wn.num_vertices}")
    print(f"Edges: {wn.num_edges}")


def get_required_triangle_form(mesh):
    vertices = mesh.vertices
    faces = mesh.faces
    outer = []
    for i in range(len(faces)):
        points = []
        for j in range(len(faces[i])):
            v = faces[i][j]
            points.append(vertices[v])
        point_np = np.array(points)
        outer.append(point_np)
    outer_np = np.array(outer)
    print(outer_np.shape)
    return outer_np


def generate_interior_points(mesh, spacing):
    triangles = get_required_triangle_form(mesh)
    min_corner = np.amin(np.amin(triangles, axis=0), axis=0)
    max_corner = np.amax(np.amax(triangles, axis=0), axis=0)
    # random points below
    # P = (max_corner - min_corner) * np.random.random((5000, 3)) + min_corner

    # Grid style points below
    x_min, y_min, z_min = min_corner[0] + spacing, min_corner[1] + spacing, min_corner[2] + spacing
    max_x, max_y, max_z = max_corner[0], max_corner[1], max_corner[2]
    x, y, z = x_min, y_min, z_min

    P_list = []
    while x < max_x:
        while y < max_y:
            while z < max_z:
                temp = np.array([x, y, z])
                P_list.append(temp)
                z += spacing
            z = z_min
            y += spacing
        y = y_min
        x += spacing
    P = np.array(P_list)
    print(P.size)

    # P = P[is_inside(triangles, P)]
    # print(P.size)

    return P


def get_wireframe(mesh):
    v, f = get_wire_info_prototype(mesh)
    return get_wire_info(v, f)


def get_wire_info_prototype(mesh):
    return np.dot(mesh.vertices, 3), mesh.faces

def edges_from_faces(vertices, faces):
    edges = []
    check = []
    # check is to ensure we don't double up
    for f in range(len(vertices)):
        inner = []
        for v in range(len(vertices)):
            inner.append(False)
        check.append(inner)

    for v in range(len(faces)):

        for i in range(len(faces[v])):
            for j in range(i+1):
                if i == j:
                    continue

                x = faces[v][i]
                y = faces[v][j]
                if check[x][y]:
                    continue
                temp = np.array([x, y])
                check[x][y] = True
                check[y][x] = True
                edges.append(temp)
    return np.array(edges)


def get_wire_info(vertices, faces):
    # switching to the wrapper of si's tetgen library to try and get tetrahedral voxels of the object
    tet = pm.tetgen()
    tet.points = vertices
    tet.triangles = faces
    # tet.keep_convex_hull = True
    tet.max_tet_volume = 300
    # tet.min_dihedral_angle = 15.0
    tet.verbosity = 1
    tet.run()
    new_mesh = tet.mesh
    faces = new_mesh.voxels
    print(new_mesh.voxels)
    vertices = new_mesh.vertices
    

    np_edges = edges_from_faces(vertices, faces)

    # print(vertices)
    # print(inner_points)
    # all_points = np.concatenate((vertices, inner_points))
    # np.save("all_points", all_points)
    # interior_points, interior_edges = meshify_inside(inner_points)

    return vertices, np_edges


def meshify_inside(inner_points):
    # Singular triangle
    temp = inner_points[0][0]
    vertices = []
    for i in range(len(inner_points)):
        if inner_points[i][0] == temp:
            vertices.append(inner_points[i])
    vertices_np = np.array(vertices)
    tri = pm.triangle()
    tri.points = vertices_np
    tri.run()
    mesh_face = tri.mesh
    print(tri.points)

    return vertices_np, "hi"

# class tesellation_option(Enum):
#     Default = 1

# class node_placement_algo_option(Enum):
#     #TODO add other tetrahedralize function options here, will need to edit how main behaves to accomodate
#     Default = 1
#     Delaunay = 1

# class triangulation_option:
#     pass
#     #TODO may not implement

    

def parse_args():
    file_path = sys.argv[1] if len(sys.argv) > 1 else None
    #edge size = wire_thickness
    wire_thickness = sys.argv[2] if len(sys.argv) > 2 else None
    #corresponds to tesellation size
    longest_line = sys.argv[3] if len(sys.argv) > 3 else None
    tessellation_option = sys.argv[4]
    node_placement_algo_option = sys.argv[5] 
    # triangulation_option = sys.argv[6]
    

    if file_path is None or wire_thickness is None or longest_line is None or tessellation_option is None or node_placement_algo_option is None:
        print("Usage: python generate_surface_mesh.py <filepath> <wire thickness> <longest edge> <tessellation_option> <node_placement_algo_option> <triangulation_option>")
        exit()

    else:
        #TODO actually implenent the usage of options
        return file_path, float(wire_thickness), float(longest_line), tessellation_option, node_placement_algo_option


if __name__ == "__main__":
    path, thickness, longest_line, tesellation_option, node_placement_algo_option = parse_args()
    mesh = pm.load_mesh(path)

    print("dim, vertex_per_face, vertex_per_voxel")
    print(mesh.dim, mesh.vertex_per_face, mesh.vertex_per_voxel)

    print("creating wireframe")
    vertices, edges = get_wireframe(mesh)

    #this command takes hella long and sometimes gets killed by docker
    wire_network = pm.wires.WireNetwork.create_from_data(vertices, edges)
    print_wire_data(wire_network)
    
    # Inflator
    inflator = pm.wires.Inflator(wire_network)
    
    print("starting inflation")

    inflator.inflate(thickness, allow_self_intersection=True)
    mesh = inflator.mesh

    print("inflated, saving now")
    # save the mesh
    pm.save_mesh("Output.stl", mesh)

    