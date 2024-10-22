# -*- coding: utf-8 -*-
"""
creo que arte do Siqueira

#bibliotecas adicionais
conda install -c conda-forge pandas
conda install -c conda-forge netcdf4

"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime,timedelta
import pandas as pd
import netCDF4
from time import sleep

nt,nc = 7305,33749

#read binary file from mgb
#f = 'D:/MGB_SA/Code/'Output/QTUDO.MGB'
path='D:/MGB_SA/Python/'
f = path + 'QTUDO.MGB'
data = np.fromfile(f, '<f4')
a = np.reshape(data,(nt,nc))

ic = 32415
plt.plot(a[:,ic],'b')
plt.show()

"""
#dataframe com datas
dstart = datetime(1990,1,1)
header = ['Mini'+str(i+1) for i in range(nc)]
df = pd.DataFrame(a,columns=header)
df = df.reset_index()
df['datas'] = df['index'].apply(lambda x: dstart+timedelta(x))
#df.groupby(df.index.month).mean()
df.head()
"""


## read netcdf and plot 
#filename
path='D:/MGB_SA/Python/'
ncfile = path + 'ETreal_MGB.nc'
f = netCDF4.Dataset(ncfile)

#mostra variaveis do netcdf
print(f.variables.keys())

#dates
times = f.variables['Time']
d111 = datetime(1,1,1)
dtimes = np.array([d111 + timedelta(days=(i-367)) for i in times[:]])

#coordinates
lat,lon = f.variables['Lat'],f.variables['Lon']
lons, lats = np.meshgrid(lon,lat)

#get etr
etr  = f.variables['ETreal'] 
#itime = 0    

# set map extent (fixed grid)    
dx = abs(0.5*(lon[1]-lon[0]))
extent = [lon[0]-dx,lon[-1]+dx,lat[-1]-dx,lat[0]+dx]

#plot
#it = 0
#plt.imshow(etr[it].T,extent=extent)
#plt.show()


##animation
fig,ax = plt.subplots()
im = ax.imshow(etr[0].T,extent=extent)

#def init():
#    im.set_data(etr[0].T)
#    return [im]

# animation function.  This is called sequentially
def animate(i):
    ax.set_title(dtimes[i])
    a = etr[i].T
    im.set_array(a)
    return [im]           


def run_animation():
    anim = animation.FuncAnimation(
        fig,animate,frames=range(0,365),interval=500,blit=False)
    plt.show()


run_animation()
