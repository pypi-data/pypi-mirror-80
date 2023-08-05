#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from h5py import File
import json
from silx.io.dictdump import dicttoh5, h5todict, dicttojson


# Conversion functions

def h5_to_json(load_addr, json_dir, indent=None, mode='w', **kwargs):
    """ Convert HDF5 to json via a dictionary.
    """
    
    dct = h5todict(load_addr, **kwargs)
    
    # Turn numpy arrays json-serializable
    for dk, dv in dct.items():
        if type(dv) == np.ndarray:
            dct[dk] = dv.tolist()
        
    dicttojson(dct, json_dir, indent, mode)


def json_to_h5(load_addr, h5_dir, **kwargs):
    """ Convert json to HDF5 via dictionary (minimal version).
    """

    with open(load_addr, 'r') as jsn:
        dct = json.load(jsn)

    dicttoh5(dct, h5_dir, **kwargs)