#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from h5py import File
from silx.io.dictdump import dicttoh5, h5todict, load
import deepdish as dd
import h5io


## Loading functions

def h5_to_dict(*args, **kwargs):
    """ Convert a multilevel HDF5 file to a multilevel dictionary.
    """
    
    source = kwargs.pop('source', 'silx')

    if source == 'silx':
        return h5todict(*args, **kwargs)
    elif source == 'deepdish':
        return dd.io.load(*args, **kwargs)
    elif source == 'h5io':
        return h5io.read_hdf5(*args, **kwargs)
    

def loadH5Parts(filename, content, outtype='dict', alias=None):
    """
    Load specified content from a single complex HDF5 file.
    
    **Parameters**\n
    filename: str
        Namestring of the file.
    content: list/tuple
        Collection of names for the content to retrieve.
    outtype: str | 'dict'
        Option to specify the format of output ('dict', 'list', 'vals').
    alias: list/tuple | None
        Collection of aliases to assign to each entry in content in the output dictionary.
    """
    
    with File(filename) as f:
        if alias is None:
            outdict = {k: np.array(f[k]) for k in content}
        else:
            if len(content) != len(alias):
                raise ValueError('Not every content entry is assigned an alias!')
            else:
                outdict = {ka: np.array(f[k]) for k in content for ka in alias}
    
    if outtype == 'dict':
        return outdict
    elif outtype == 'list':
        return list(outdict.items())
    elif outtype == 'vals':
        return list(outdict.values())


def loadHDF(load_addr, hierarchy='flat', groups='all', track_order=True, dtyp='float', **kwargs):
    """ Load contents from an HDF.
    
    **Parameters**\n
    load_addr: str
        Address of the file to load.
    hierarchy: str | 'flat'
        Hierarchy of the file structure to load into.
    groups: list/tuple/str
        Name of the groups.
    dtype: str | 'float'
        Data type to be loaded into.
    **kwds: keyword arguments
        See ``h5py.File()``.
    
    **Return**\n
    outdict: dict
        Dictionary containing the hierarchical contents of the file.
    """

    outdict = {}
    if hierarchy == 'nested':
        outdict = load(load_addr, fmat='h5')

    elif hierarchy == 'flat':
        with File(load_addr, track_order=track_order, **kwds) as f:

            if groups == 'all':
                groups = list(f)

            for g in groups:
                for gk, gv in f[g].items():
                    outdict[gk] = np.asarray(gv, dtype=dtyp)

    return outdict


## Writing functions

def dict_to_h5(*args, **kwargs):
    """ Convert a multilevel dictionary to a multilevel HDF5 file.
    """

    source = kwargs.pop('source', 'silx')

    if source == 'silx':
        return dicttoh5(*args, **kwargs)
    elif source == 'deepdish':
        return dd.io.save(*args, **kwargs)
    elif source == 'h5io':
        return h5io.write_hdf5(*args, **kwargs)


def saveHDF(*groups, save_addr='./file.h5', track_order=True, **kwds):
    """ Combine dictionaries and save into a hierarchical structure.

    **Parameters**\n
    groups: list/tuple
        Group specified in the following manner that incorporates the name as a string
        and the content and or substructure as a dictionary, ['folder_name', folder_dict].
    save_addr: str | './file.h5'
        File directory for saving the HDF.
    """

    try:
        hdf = File(save_addr, 'w')

        for g in groups:
            grp = hdf.create_group(g[0], track_order=track_order)

            for gk, gv in g[1].items():
                grp.create_dataset(gk, data=gv, **kwds)

    finally:
        hdf.close()