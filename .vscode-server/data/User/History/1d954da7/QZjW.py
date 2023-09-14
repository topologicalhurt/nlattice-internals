from typing import NewType
import pymesh as pm


class Types:
   MESH = NewType('Mesh', pm.Mesh) # Alias pm.Mesh.Mesh with Mesh to avoid verbosity


class Dirs:
    CONFIG_FDIR = './config.json'
    OUT_FDIR = './out'