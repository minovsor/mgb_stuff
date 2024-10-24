# -*- coding: utf-8 -*-
"""
CONVERTE BACIAS DO TERRAHIDRO

@author: MINO SORRIBAS
"""

#import os
#os.environ['USE_PYGEOS'] = '0'
#os.environ.pop('PROJ_LIB')

#import osgeo
import os
from osgeo import gdal, ogr
import numpy as np
import rasterio
import geopandas as gpd



def mouths_to_gpkg(th_mini, mouths_coords, output_gpkg = 'ms_mouths.gpkg'):
    # le a matriz dos rios contendo codigos de mini
    with rasterio.open(th_mini,'r') as src:
        #band = src.read(1).astype(int)
        
        # identifica linhas e colunas        
        ij = mouths_coords
        xs,ys = rasterio.transform.xy(src.transform,ij[:,0],ij[:,1])
        
        gdf = gpd.GeoDataFrame(data = mouths_coords,
                               columns = ['irow','jcol'],
                               geometry = gpd.points_from_xy(xs,ys,crs=src.crs))    
        gdf.to_file(output_gpkg)

    return xs,ys
    

def manymouths_subbasins(th_mini, th_rivers, mouths_coords,
                         output_rst = 'ms_manymouths.tif'):

    # le raster dos rios (codificados pelo exutorio = mini do exutorio)
    with rasterio.open(th_rivers,'r') as riv_mini:
        rivers = riv_mini.read(1).astype(int)        
            
        # le raster de minibacias
        # ... depois vamos ler os exutorios
        # ... em cada exutorio obteremos o codigo do 
        # ...
        with rasterio.open(th_mini,'r') as cat_mini:            
            mini = cat_mini.read(1).astype(int) # dados
            profile = cat_mini.profile    # propriedades do tif
            nodata_value = cat_mini.nodata   #valor de nodata
            
            # o raster inicial é a propria minibacia
            #out = np.copy(mini) 
            out = np.ones_like(mini)*nodata_value
            exut_list = []
            # identifica o codigo de mini, na boca do rio
            for i, line in enumerate(mouths_coords):
                row, col = line[0], line[1]
                exutcode = rivers[row,col]
                print(f'mouth {i}:({row},{col}) - exut {exutcode}')
            
                # identifica pixels do river atual (drenam ate o exutorio)
                # e resgata os codigos das minibacias nesses pixels
                targets = np.unique(mini[rivers==exutcode])
                ##mask = np.isin(out, targets)
                #out[mask] = exutcode
                
                mask = np.isin(mini, targets)
                out[mask] = exutcode
                
                # armazena os codigos de exutorio utilizados
                exut_list.append(exutcode)
                
            # os que nao foram utilizados, serao removidos
            #m = np.isin(out, exut_list)
            #out[m] = nodata_value
                
        
            # Update the profile with the shape of the 'out' array
            #profile['count'] = 1
            profile['dtype'] = 'int32'
    
            # Write the output raster
            with rasterio.open(output_rst, 'w', **profile) as dst:
                dst.write(out.astype(profile['dtype']), 1)
            
            fil,ext = os.path.splitext(output_rst)
            with rasterio.open(f'{fil}_mask.{ext}', 'w', **profile) as dst:
                out_mask = out.copy()
                out_mask[out!=nodata_value] = 1
                dst.write(out_mask.astype(profile['dtype']), 1)                 
                
    return 


def poligonize_with_gdal(input_rst, output_gpkg):
    # Open the raster file
    with gdal.Open(input_rst) as raster:
        band = raster.GetRasterBand(1)
    
        # Create an output GeoPackage
        driver = ogr.GetDriverByName('GPKG')
        with driver.CreateDataSource(output_gpkg) as geopackage:
            # Create a layer in the GeoPackage
            layer = geopackage.CreateLayer('polygons', geom_type=ogr.wkbPolygon)
        
            # Create a field for the value
            layer.CreateField(ogr.FieldDefn("value", ogr.OFTInteger))
    
            # Polygonize
            gdal.Polygonize(band, None, layer, 0, [], callback=None)
    return


# Define rasters 'mini' e 'rivers' que drenam pros exutorios
th_mini = 'th_mini.tif'
th_rivers = 'th_rivers.tif'


# Define arquivo de exutorios (c/ linhas e colunas)
#file_mouths = 'ordered_mouths.txt'
#mouths_coords = np.loadtxt(file_mouths).astype(int)

# Inicializa processamento
# 1. Monta geopackage de pontos dos exutorios
#_ = mouths_to_gpkg(th_mini, mouths_coords)

# 2. Monta raster de subbacias por exutorio
#_ = manymouths_subbasins(th_mini, th_rivers, mouths_coords,'ms_manymouths.tif')
#_ = poligonize_with_gdal('ms_manymouths.tif', 'ms_manymouths.gpkg')

# 3. Refaz para exutorios selecionados
file_mouths = 'selected_mouths.txt'
mouths_coords = np.loadtxt(file_mouths).astype(int)

_ = manymouths_subbasins(th_mini, th_rivers, mouths_coords,'ms_manymouths_selec.tif')
_ = poligonize_with_gdal('ms_manymouths_selec.tif', 'ms_manymouths_selec.gpkg')

