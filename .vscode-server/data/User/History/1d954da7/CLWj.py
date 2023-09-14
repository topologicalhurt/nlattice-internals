import pymesh as pm
import json
from typing import NewType


class Meta:
    CONFIG = json.load


class Types:
    Mesh = NewType('Mesh', pm.Mesh) # Alias pm.Mesh.Mesh with Mesh to avoid verbosity


class Dirs:
    CONFIG_FDIR = '../config.json'
    OUT_FDIR = '../out'