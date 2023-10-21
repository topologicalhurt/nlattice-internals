from meshlib import mrmeshnumpy as mn
import plotly.graph_objects as go
import numpy as np


def visualise(mesh, edge_size, tess_size):
    verts = mn.getNumpyVerts(mesh)
    faces = mn.getNumpyFaces(mesh.topology)

    # Scale the vertices based on tessellation size
    verts = verts * tess_size

    vertsT = np.transpose(verts)
    facesT = np.transpose(faces)

    m = mesh.volume

    fig = go.Figure(data=[
        go.Mesh3d(
            # Modify edge_size and tess_size to scale the mesh
            x=vertsT[0],
            y=vertsT[1],
            z=vertsT[2],
            i=facesT[0],
            j=facesT[1],
            k=facesT[2],
        )
    ])

    fig.update_layout(scene=dict(bgcolor='white'))  # Change background color to white
    return fig
