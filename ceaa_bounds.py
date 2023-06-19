'''

MGB-SA E CONTAS ECONOMICAS E AMBIENTAIS DA AGUA

Authors:
version (10 abr 2020): Mino Sorribas

- GERADOR DE TABELA DE MINIBACIAS INTERNAS A UM POLIGONO DE CONTORNO


* ATENCAO:
- CONSIDERA CENTROIDE DA MINIBACIA PARA VERIFICAR SE É INTERNO
- LIMITACOES: A METODOLOGIA NAO CONSIDERA A AREA DE INTERSECCAO DOS POLIGONOS
...

'''

#bibliotecas gerais
import logging
import os
from datetime import datetime,timedelta
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat #se quiser ler .mat
import itertools

#analise espacial
import pandas as pd
import geopandas as gpd
import shapely.speedups

shapely.speedups.enable()

# inicializa logger
logging.basicConfig(
    filename='logfile.log',
    filemode='w',
    level=logging.INFO,
    #level=logging.DEBUG,
    format='%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    )

logger = logging.getLogger(__name__)

# log salve em arquivo e mostra na tela (stream handler)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(console)


logger.info('Iniciou ceaa_mgb.py')

#-------------------------------------------
# CONFIGURACOES GERAIS
#-------------------------------------------
logger.info('Configuracoes gerais')

# opcoes adicionais
options = {}

# dimensoes dos binarios do mgb (intervalos e minibacias) e data de inicio
nt = 7305
nc = 33749
dstart = datetime(1990,1,1)

# caminhos principais
path_ceaa = 'F:/PosDoc/ceaa/base_ceaa/'
path_shp  = 'F:/PosDoc/ceaa/base_mgb_sa/'
#path_mgb = 'F:/PosDoc/SAFE_MS/MGB_SA/Code/Output/'

# arquivo mini.gtp em formato mini.xlsx
file_minigtp = path_ceaa + 'mini.xlsx'

# arquivos de shapefile do MGB-AS
file_mgb_rede = path_shp + 'MGB_SA_Rivers.shp'          #_SIRGAS2000.shp'
file_mgb_mini = path_shp + 'MGB_SA_Unit_Catchments.shp'  #_SIRGAS2000.shp'

# poligono de analise
file_regioes = path_ceaa + 'BR_RA_250GC_WGS1984/BR_RA_250GC_WGS1984.shp'


# opcional
options['select_region'] = ('NM_REGIAO','SUL')  #seletor de regiao
options['select_region'] = ('NM_REGIAO','NORTE')  #seletor de regiao


# TODO: testa se a configuracao de usuário é válida


#-----------------------------
# DEFINE FUNCOES
#-----------------------------
logger.info('Definindo funcoes')

def carrega_shape_mini(file):
    """ carrega shapefile mini e garante dtypes -> object"""
    gdf = gpd.GeoDataFrame.from_file(file) 
    crs = gdf.crs.copy()
    gdf = gdf.astype('O')
    gdf.crs=crs
    return gdf

def le_binario_mgb(filebin,nt,nc):
    """ read mgb binary files as numpy.array """
    return np.fromfile(filebin,'<f4').reshape(nt,nc)

def points_in_pols(gdf_points,gdf_pols):
    """ pontos em poligonos """
    return gpd.sjoin(gdf_points,gdf_pols,how='left',op='within')

def carrega_shape_contorno(file):
    """ carrega shapefile de contorno """
    gdf = gpd.GeoDataFrame.from_file(file) 
    crs = gdf.crs.copy()    #necessario, pois .astype perde o .crs    
    gdf = gdf.astype('O')   #converte -> object
    gdf.crs=crs             #recupera crs
    return gdf



#-------------------------------------------------------------------------------
# PRE-PROCESSAMENTO DO MGB (TOPOLOGIA E SHAPES)
#-------------------------------------------------------------------------------
logger.info('Preprocessamento de topologia e shapes do MGB')

# carrega mini.gtp e separa topologia
df_mini = pd.read_excel(file_minigtp)
df_topo = df_mini.loc[:,['Mini','MiniJus','Ordem']].astype('O')

# carrega shapefiles em geodataframe
gdf_mgb_rede = carrega_shape_mini(file_mgb_rede)
gdf_mgb_mini = carrega_shape_mini(file_mgb_mini)

# inclui colunas de topologia nos geodataframes
gdf_mgb_mini = gdf_mgb_mini.merge(df_topo,on='Mini',validate="many_to_one")
#gdf_mgb_rede = gdf_mgb_rede.merge(df_topo,on='Mini',validate="many_to_one")


# monta gdf de centroides
sel = ['Mini','MiniJus','Ordem','geometry']
gdf_mgb_xy = gdf_mgb_mini[sel]
gdf_mgb_xy = gpd.GeoDataFrame(gdf_mgb_xy,geometry=gdf_mgb_xy.centroid,crs="EPSG:4326")



#-------------------------------------------------------------------------------
# PRE-PROCESSAMENTO DO CONTORNO DE ANALISE
#-------------------------------------------------------------------------------
logger.info('Preprocessamento do contorno de analise')

# inicializa com Brazil no default
gdf_world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres')) 
gdf_brazil = gdf_world[gdf_world.name=="Brazil"]
gdf_contorno = gdf_brazil.copy()

# carrega poligono de contorno
try:
    gdf_contorno = carrega_shape_contorno(file_regioes)
except:
    print("Erro ao carregar shapefile: utilizando Brasil.")

# faz uma copia para realizar as analises (contorno poderia ter mais de 1 feature..)
gdf_dominio = gdf_contorno.copy()


# opcional: seleciona regiao a partir de critério no dicionario 'options'
status = options.get('select_region',None)
if status:
    k,v = status
    sel = gdf_contorno[k]==v
    gdf_dominio = gdf_contorno.loc[sel]




#----------------------------------------------------------
# PROCESSAMENTO - IDENTIFICAÇÃO DE CONTORNOS
#----------------------------------------------------------
logger.info('Processamento principal - Pontos Internos e Fronteiras')

# poligono de minibacias para trabalho
sel = ['Mini','MiniJus','Ordem','geometry']
gdw = gdf_mgb_mini[sel].copy()
gdw['borda'] =False
gdw['dentro']=False
gdw['aflu']  =False 
#gdw['deflu'] =False
#gdw['costa'] =False
gdw['ind_afl'] = False


# 1. identifica centroides de minibacias internos ao poligono
logger.info('... obtendo centroides internos')
gdf_sjoin = points_in_pols(gdf_mgb_xy,gdf_dominio)
is_inside = gdf_sjoin.index_right.notna()
#gdf_inside = gdf_sjoin[is_inside]

# atualiza no gdf de poligonos de minibacias
gdw['dentro'] = is_inside

# 2. identifica minibacias na regiao de fronteira
logger.info('... obtendo minibacias nas fronteiras')
def f_is_fronteira(geom):
    return gdf_dominio.geometry.overlaps(geom)
gdw['borda'] = gdw.apply(lambda row:f_is_fronteira(row.geometry),axis=1)


# exporta tabela de pontos mini dentro do contorno
#gdf_inside.loc[is_inside,'Mini'].to_excel('mini_dentro.xlsx')

## trash
##def f_is_inside(geom):
##    return gdf_dominio.geometry.contains(geom)


# 3. atualiza dominio de trabalho
logger.info('... atualizando dominio + fronteira')
gdw['dominio'] = (gdw['dentro'] | gdw['borda'])        #boolean

# atualiza gdfs de dominio
gdf_dominio = gdw[gdw['dominio']]                      #poligonos
gdf_mgb_xy['dominio'] = gdw['dominio']                 #->boolean nos centroides
gdf_dominio_xy = gdf_mgb_xy[gdf_mgb_xy['dominio']]     #pontos (centroides)


# identifica no dominio as minibacias que desaguam internamente
#idjus = gdf_dominio['Mini'].isin(gdf_dominio['MiniJus'])   #busca por afluentes
#iaflu = ~idjus                                             #minijus não encontrados - pode encontrar apenas 1 afluente...

#... cabeceiras nao sao problema
#iaflu = np.where(gdf_dominio['Ordem']==1,False,iaflu)

#TODO: o teste anterior é fraco pois aceita que basta encontrar 1 afluente.
#... no caso, podemos ter uma minibacia de fronteira que recebe agua de fora e de dentro.
#... ou seja, com mais de um afluente
#... o teste a ser feito é: para cada ponto na fronteira, verificar quais afluentes não estao no dominio.
#... esses afluentes que nao estao no dominio serao os afluentes finais.



# 4. busca afluentes do dominio na tabela geral e no proprio dominio
# atencao: todo esse processo utiliza o index do dataframe (nao o codigo de mini)
logger.info('... obtendo minibacias afluentes')
def f_busca_aflu(row,gdf_base):
    ''' retorna indices do gdf_base com os afluentes
        example: gdf_dominio.apply(f_encontra_aflu,args=(gdf_global,),axis=1)
    '''
    iaflu = gdf_base['MiniJus']==row['Mini']
    return gdf_base[iaflu].index.values

s_afl_mgb_mini = gdf_dominio.apply(f_busca_aflu,args=(gdf_mgb_mini,),axis=1)
s_afl_dominio  = gdf_dominio.apply(f_busca_aflu,args=(gdf_dominio,),axis=1)
#... TODO: calculo pode ser bem pesado se existem muitos features.

# obtem afluentes externos ao dominio comparando os dois conjuntos
s1 = s_afl_mgb_mini.transform(set)
s2 = s_afl_dominio.transform(set)
gdf_afl_conj = pd.concat((s1,s2),axis=1)
s_afl_externo = gdf_afl_conj.apply(lambda r: r[0].symmetric_difference(r[1]),axis=1)

# separa os indices dos afluentes externos
s_afl_indices = s_afl_externo.transform(list).transform(lambda x: np.nan if len(x)==0 else x).dropna()

#temporario
#afl_recebe = gdf_dominio.loc[s_afl_indice.index]
#afl_recebe['MiniAfl'] = s_afl_indice

# armazena indices de afluentes
gdw['ind_afl'] = s_afl_indices
gdw['entrada'] = np.where(gdw['ind_afl'].isna(),False,True)



## lista de indices
lista_afl_indices = list(itertools.chain.from_iterable(s_afl_indices.values.ravel()))

## TODO: obtem lista de minibacias correspondentes aos indices

#TOCHECK: acho que a lista é de indices, nao de minis
#iaflu = gdf_mgb_mini['Mini'].isin(lista_afl_mini)



# 5. busca defluentes do dominio
logger.info('... obtendo minibacias defluentes')
#


'''
# identifica no dominio as minibacias que desaguam para outro lugar
idmon  = gdf_dominio['MiniJus'].isin(gdf_dominio['Mini'])   #busca locais a jusante
ideflu = ~idmon                                             #mini nao encontrada

#...encontra locais certos, linha costeira, ou divisores espurios
#...testar divisores espurios com ordem==1 | drena
iverte = (gdf_dominio['Ordem']==1 and gdf_dominio['MiniJus']!=-1)
ideflu = np.where(iverte,False,ideflu)
'''

#---------------------------------------
# mostra no mapa
#---------------------------------------
fig,ax=plt.subplots(figsize=(8,12))

#poligonos
gdf_mgb_mini.plot(ax=ax,linewidth=0.25, edgecolor='white', color='lightgrey')
gdf_contorno.plot(ax=ax,linewidth=0.25, edgecolor='red', facecolor='None')

gdw[gdw['borda']].plot(ax=ax,edgecolor='black',facecolor='None')

#pontos
gdf_dominio_xy[gdw['dominio']].plot(ax=ax,color='blue',markersize=1.0)
gdf_dominio_xy[gdw['entrada']].plot(ax=ax,color='green')

#polyline
gdf_mgb_rede.plot(ax=ax,linewidth=0.2, color='blue')

#gdf_dominio_xy[iaflu].plot(ax=ax,color='green')
#gdf_dominio_xy[ideflu].plot(ax=ax,color='red')

plt.show()

#----------------------------------------------------------
# 2.  CALCULA COISAS 
#----------------------------------------------------------
#



#OU FAZ ISSO EM OUTRO .py

#gera shape de centroides com minijus
#df_mini = pd.read_excel('mini.xlsx')
#df_topo = df_mini.loc[:,['Mini','MiniJus']].astype('O')
#gdf_mgb_rede = gdf_mgb_rede.merge(df_topo,on='Mini',validate="many_to_one")


'''
def intersect_polygons(poly, boundary):
    if poly.overlaps(boundary):
        poly = poly.intersection(boundary)
    return poly

# polygons is a list of shapely Polygon objects
# contorno is a shapely Polygon object
new_polygons = [intersect_polygons(p, boundary) for p in polygons]
'''
