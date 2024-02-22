# -*- coding: utf-8 -*-
"""
CONVERTE BACIAS DO TERRAHIDRO

@author: MINO SORRIBAS
"""

import os
os.environ['USE_PYGEOS'] = '0'
os.environ.pop('PROJ_LIB')

import osgeo
import numpy as np
import rasterio
from rasterio import CRS, Affine

import geopandas as gpd


# carrega linha/coluna dos exutorios
file_mouths = 'outputmouths.txt'
mouths_coords = np.loadtxt(file_mouths).astype(int)

# exutorio do doce
test_mouths_coords = np.atleast_2d([6127,13936])

# rasters de minibacia e rios que drenam pros exutorios
th_mini = 'th_mini.tif'
th_outputrivers = 'outputrivers.tif'


def mouths_coordinates(th_mini, mouths_coords):
    # le a matriz dos rios contendo codigos de mini
    with rasterio.open(th_mini,'r') as src:
        band1 = src.read(1).astype(int)    
        height = band1.shape[0]
        width = band1.shape[1]
        
        # grid inteiro
        #cols, rows = np.meshgrid(np.arange(width), np.arange(height))
        #xs, ys = rasterio.transform.xy(src.transform, rows, cols)
        #lons = np.array(xs)
        #lats = np.array(ys)
        
        # salva raster lon/lat em duas bandas
        #profile = src.profile
        #profile['dtype'] = 'float32'
        #profile['count'] = 2
        #with rasterio.open("ms_latlon.tif", 'w', **profile) as dst:
        #    dst.write(lons, 1) #lon
        #    dst.write(lats, 2) #lat        
        
        ij = mouths_coords
        xs,ys = rasterio.transform.xy(src.transform,ij[:,0],ij[:,1])
        
        gdf = gpd.GeoDataFrame(geometry = gpd.points_from_xy(xs,ys,crs=src.crs))    
        gdf.to_file('ms_mouths.gpkg')

    return xs,ys
    


# funcao para tentar single poins
def many_mouths(th_mini, th_outputrivers, mouths_coords):

    # le a matriz dos rios contendo codigos de mini
    with rasterio.open(th_outputrivers,'r') as riv_mini:
        rivers = riv_mini.read(1).astype(int)
        
            
        # le minibacias e vamos identificar quais estao nos rios
        with rasterio.open(th_mini,'r') as cat_mini:
            profile = cat_mini.profile  # propriedades do tif        
            mini = cat_mini.read(1).astype(int)
            out = np.copy(mini)
            
            # identifica o codigo de mini, na boca do rio
            for i, line in enumerate(mouths_coords):
                row,col = line[0],line[1]
                minicode = rivers[row,col]
                print(f'mouth {i}:({row},{col}) - mini {minicode}')
            
                # varre os codigos de minibacia
                #for i,c in enumerate(codes):
                targets = np.unique(mini[rivers==minicode]) # identifica minibacias em cada rio
                mask = np.isin(out, targets)
                out[mask] = minicode
        
            # Update the profile with the shape of the 'out' array
            #profile['count'] = 1
            profile['dtype'] = 'int32'
    
            # Write the output raster
            with rasterio.open("ms_subbacias_manymouths.tif", 'w', **profile) as dst:
                dst.write(out.astype(profile['dtype']), 1)  
                
    return 


# rodada
#_ = many_mouths(th_mini, th_outputrivers, mouths_coords)

