from typing import NewType
import pymesh as pm


class Types:
    Mesh = NewType('Mesh', pm.Mesh) # Alias pm.Mesh.Mesh with Mesh to avoid verbosity


class Dirs:
    OUT_FDIR = './out'