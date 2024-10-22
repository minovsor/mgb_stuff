# -*- coding: utf-8 -*-
"""
Read HRXX dataset as dataframe

HRXX available at http://dx.doi.org/10.17632/9kjx9d7ycm.3

@author: Mino Sorribas
"""

from datetime import datetime,timedelta
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import netCDF4


# le arquivo netcdf
fp = 'HRXX_Amz_v1.0.nc'
f = netCDF4.Dataset(fp,'r')
vazao = f.variables['discharge']
qarr = vazao[0:]
f.close()

# monta dataframe
nt,nc = qarr.shape
times = [datetime(1910,1,1) + timedelta(t) for t in range(nt)]
list_mini = list(range(1,nc+1))

df = pd.DataFrame(data = qarr,
                  index = pd.DatetimeIndex(times),
                  columns = list_mini,
                  )
del qarr #libera memoria
