import pymesh as pm
import os
import contextlib
import json
from typing import Optional
from functools import reduce
from operator import getitem
from python.pc.consts import Types, Dirs


@contextlib.contextmanager
def _seek_modify(fn: str, ow: any, *args, mode: Optional[str] = 'w') -> None:
    """
    Appends to a .json file

    - fn: file dir to append to
    - ow: if the mode is set to 'w' then the field is overwritten with this value
    - *args: the 'tree' of references to the field that should be changed
    - mode: default is to overwrite (expect a None to be yielded by context handler).
     Use 'a' if you wish to append to a list field
    """
    with open(fn, 'r+') as f:
        dat = json.load(f)
        if mode == 'a':
            yield reduce(getitem, args[:-1], dat)[args[-1]]
        elif mode == 'w': 
            yield None
            reduce(getitem, args[:-1], dat)[args[-1]] = ow
        else:
            raise ValueError('The mode must be one of: ["a"] ["w"]')
        f.seek(0)
        json.dump(dat, f, indent=4)
        f.truncate()


def _init_out_file(fp: str) -> None:
    """Creates the file pointed to by fp if none is found"""
    if not os.path.exists(fp):
        os.mkdir(fp)


def reset_objects_config():
    """Resets the object field in the config file"""
    with _seek_modify(Dirs.CONFIG_FDIR, [], 'Objects') as _:
        pass 


@contextlib.contextmanager
def mesh_save_handler(out_file: Types.Mesh, out_name: str) -> None:
    """
    A context handler for saving pymesh states and updating the config file.
    The context handler will yield the list of all objects in the config file
    which can be custom re-configured by the calling function and re-written
    to the config.

    Will yield None if the file already exists in the out directory

    - out_file: The mesh object to be saved
    - out_name: The name of the output file
    """
    _init_out_file(Dirs.OUT_FDIR)
    where_to = f'{Dirs.OUT_FDIR}/{out_name}'
    if not os.path.isfile(where_to):
        with _seek_modify(Dirs.CONFIG_FDIR, None, 'Objects', mode='a') as field:
            field.append({'Id': len(field), 'Dir': where_to})
            yield field
    else:
        yield None
    pm.save_mesh(where_to, out_file, anonymous=False)
