# -*- coding: utf-8 -*-
"""

@author: Mino Sorribas
"""
import numpy as np
import pandas as pd
from datetime import datetime,timedelta

def dump_mgb_binary_to_npy(filebin, fileout, nt, nc):
    """ Read binary file (MGB format) and dump content to .npy """

    # read from file
    #'<f4' indicates little-endian (<) float(f) 4 byte (4)
    dados = np.fromfile(filebin,'<f4').reshape(nt,nc)

    # dump fo hard disk
    np.save(fileout,dados)
    return None




def read_npy_as_mmap(filenpy):
    """ Read .npy binary file and make memory-map array"""

    # make memory-map from file (doest not consume memory!)
    dados_mmap = np.load(filenpy,mmap_mode='r')

    return dados_mmap




def mmap_to_dataframe(dados_mmap, list_t, list_c, dstart):
    """ Read data from memmap as dataframe

        Args:
            dados_mmap (np.memmap) :: memory map of binary .npy

            list_t (list) :: list of integer of selected timesteps

            list_c (list) :: list of integer of selected catchments

            dstart (datetime) :: first date in dados_mmap

        Returns:
            df (pd.DataFrame) :: time-series of selected values
    """

    # adjust loc in array
    ixt_ = [i for i in list_t]
    ixc_ = [int(i-1) for i in list_c]  # mini column [1,nc] -> python [0,nc-1]

    # get selection
    idx = np.ix_(ixt_, ixc_)
    a = dados_mmap[idx]

    # make timeseries dataframe
    times = [dstart + timedelta(days=i) for i in list_t]
    df = pd.DataFrame(a, columns=list_c, index=times)

    return df
