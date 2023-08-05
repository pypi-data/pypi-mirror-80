#! /usr/bin/env python
# -*- coding: utf-8 -*-

from . import dict_io as io
import numpy as np
from h5py import File
import json
from silx.io.dictdump import dicttojson


# Conversion functions

def h5_to_json(load_addr, json_dir, indent=None, mode='w', fconv=io.h5_to_dict, **kwargs):
    """ Convert HDF5 to json via a dictionary.
    """
    
    dct = fconv(load_addr, **kwargs)
    
    # Turn numpy arrays json-serializable
    for dk, dv in dct.items():
        if type(dv) == np.ndarray:
            dct[dk] = dv.tolist()
        
    dicttojson(dct, json_dir, indent, mode)


def json_to_h5(load_addr, h5_dir, fconv=io.dict_to_h5, loadkwargs={}, **kwargs):
    """ Convert json to HDF5 via dictionary (minimal version).
    """

    with open(load_addr, 'r') as jsn:
        dct = json.load(jsn, **loadkwargs)

    fconv(dct, h5_dir, **kwargs)