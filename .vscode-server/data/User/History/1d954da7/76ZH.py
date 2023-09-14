import pymesh as pm
import json
from typing import NewType


class Types:
    Mesh = NewType('Mesh', pm.Mesh) # Alias pm.Mesh.Mesh with Mesh to avoid verbosity


class Dirs:
    MODEL_FDIR = '../install/test_model.stl'
    MODEL2_FDIR = '../install/test_model2.stl'
    CONFIG_FDIR = '../config.json'
    OUT_FDIR = '../out'


class MetaD:
    with open(Dirs.CONFIG_FDIR, 'r') as f:
        dat = json.load(f)
        CONFIG = dat
        