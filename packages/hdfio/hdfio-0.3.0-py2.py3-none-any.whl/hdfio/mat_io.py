#! /usr/bin/env python
# -*- coding: utf-8 -*-

from . import dict_io as io
import numpy as np
from h5py import File
from scipy.io import loadmat, savemat


# Conversion functions

def mat_to_h5(load_addr, h5_dir, keep_meta=False, loadkwargs={}, **kwargs):
    """ Convert mat file to HDF5 via dictionary.
    """

    sqm = loadkwargs.pop('squeeze_me', True)
    matdict = loadmat(load_addr, squeeze_me=sqm, **loadkwargs)
    
    if not keep_meta:
        matdict = dict((mk, mv) for mk, mv in matdict.items() if not mk.startswith('__'))

    fconv = kwargs.pop('fconv', io.dict_to_h5)
    fconv(matdict, h5_dir, **kwargs)


def h5_to_mat(load_addr, mat_dir, loadkwargs={}, **kwargs):
    """ Convert HDF5 to mat file via dictionary.
    """

    fconv = kwargs.pop('fconv', io.h5_to_dict)
    dct = fconv(load_addr, **loadkwargs)

    savemat(file_name=mat_dir, mdict=dct, **kwargs)
