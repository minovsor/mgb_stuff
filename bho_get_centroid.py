# -*- coding: utf-8 -*-

import os
os.environ['USE_PYGEOS'] = '0'
try:
    os.environ.pop('PROJ_LIB')
else:
    pass
import numpy as np
import pandas as pd
import geopandas as gpd


# le baess bho 5k 2017
gdf_trechos = gpd.read_file('geoft_bho_2017_5k_trecho_drenagem.gpkg')
gdf_bacias = gpd.read_file('geoft_bho_2017_5k_area_drenagem.gpkg')



# trechos
gdf_trechos['xg'] = gdf_trechos.centroid 
gdf_trechos[['centro_x','centro_y']] = gdf_trechos.apply(lambda row: (row.xg.x,row.xg.y),result_type='expand',axis=1)
gdf_trechos.set_geometry('xg',drop=True).to_file('centroides_trechos.gpkg',driver='GPKG')


# bacias
gdf_bacias['xg'] = gdf_bacias.centroid  
gdf_bacias[['centro_x','centro_y']] = gdf_bacias.apply(lambda row: (row.xg.x,row.xg.y),result_type='expand',axis=1)
gdf_bacias.set_geometry('xg',drop=True).to_file('centroides_bacias.gpkg',driver='GPKG')


gdf_trechos.drop(['geometry','xg'],axis=1).to_excel('centroides_trechos.xlsx')
gdf_bacias.drop(['geometry','xg'],axis=1).to_excel('centroides_bacias.xlsx')
