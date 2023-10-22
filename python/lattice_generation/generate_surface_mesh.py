import pymesh as pm
import numpy as np
import sys


def print_wire_data(wn):
    print(f"Dim: {wn.dim}")
    print(f"Vertices: {wn.num_vertices}")
    print(f"Edges: {wn.num_edges}")


def get_wireframe(mesh, max_volume_ratio):
    v, f = get_wire_info_prototype(mesh)
    return get_wire_info(v, f, max_volume_ratio)


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
            for j in range(i + 1):
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


def slider_to_volume(vertices, n):
    min_corner = np.min(vertices, axis=0)
    max_corner = np.max(vertices, axis=0)

    size = max_corner - min_corner
    volume = size[0] * size[1] * size[2]

    return volume / (n ** 2)


def get_wire_info(vertices, faces, max_volume_ratio):
    # switching to the wrapper of si's tetgen library to try and get tetrahedral voxels of the object
    tet = pm.tetgen()
    tet.points = vertices
    tet.triangles = faces

    tet.max_tet_volume = slider_to_volume(vertices, max_volume_ratio)
    print("max volume ratio is passed: " + str(tet.max_tet_volume))
    # tet.min_dihedral_angle = 15.0
    tet.verbosity = 1
    tet.run()
    new_mesh = tet.mesh
    faces = new_mesh.voxels
    print(new_mesh.voxels)
    vertices = new_mesh.vertices

    np_edges = edges_from_faces(vertices, faces)

    return vertices, np_edges


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
    # edge size = wire_thickness
    wire_thickness = sys.argv[2] if len(sys.argv) > 2 else None
    # corresponds to tesellation size
    max_volume_ratio = sys.argv[3] if len(sys.argv) > 3 else None
    tessellation_option = sys.argv[4]
    node_placement_algo_option = sys.argv[5]
    triangulation_option = sys.argv[6]

    if file_path is None or wire_thickness is None or max_volume_ratio is None or tessellation_option is None or node_placement_algo_option is None:
        print(
            "Usage: python generate_surface_mesh.py <filepath> <wire thickness> <longest edge> <tessellation_option> <node_placement_algo_option> <triangulation_option>")
        exit()

    else:
        # TODO actually implenent the usage of options
        return file_path, float(wire_thickness), float(
            max_volume_ratio), tessellation_option, node_placement_algo_option


if __name__ == "__main__":
    path, thickness, max_volume_ratio, tesellation_option, node_placement_algo_option = parse_args()
    mesh = pm.load_mesh(path)

    print("dim, vertex_per_face, vertex_per_voxel")
    print(mesh.dim, mesh.vertex_per_face, mesh.vertex_per_voxel)
    print("creating wireframe")
    vertices, edges = get_wireframe(mesh, max_volume_ratio)

    # this command takes hella long and sometimes gets killed by docker
    wire_network = pm.wires.WireNetwork.create_from_data(vertices, edges)
    print_wire_data(wire_network)

    # Inflator
    inflator = pm.wires.Inflator(wire_network)

    print("starting inflation")

    inflator.inflate(thickness, allow_self_intersection=True, per_vertex_thickness=False)
    mesh = inflator.mesh

    print("inflated, saving now")
    # save the mesh
    pm.save_mesh("Output.stl", mesh)
