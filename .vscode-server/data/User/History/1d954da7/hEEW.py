import pymesh as pm
import json
from typing import NewType


class Types:
    Mesh = NewType('Mesh', pm.Mesh) # Alias pm.Mesh.Mesh with Mesh to avoid verbosity


class Dirs:
    CONFIG_FDIR = '../config.json'
    OUT_FDIR = '../out'


class MetaD:
    with open(Dirs.CONFIG_FDIR, 'r') as f:
        dat = json.load(f)
        CONFIG = dat