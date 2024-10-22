# -*- coding: utf-8 -*-
"""
Created on Wed May 18 16:47:26 2022

@author: Avell
"""


import numpy as np
from datetime import datetime,timedelta
import pandas as pd
import geopandas as gpd


# -- parametros de simulacao do mgb
nc = 33749
nt = 13149
dstart = datetime(1979,1,1)

# -- carrega mini.gtp em versao excel
df_mini = pd.read_excel('./input/mini.xlsx')
df_mini = df_mini.rename(columns={'Mini':'mini',
                                  'MiniJus':'minijus',
                                  'Area_(km2)':'areac'})



# -- carrega vazoes simuladas do mgb
filebin = './input/QTUDO_1979.MGB'
dados = np.fromfile(filebin,'<f4').reshape(nt,nc)
minis = range(1,nc+1)
dates = [dstart + timedelta(days=i) for i in range(nt)]
df_dados = pd.DataFrame(dados,index=dates,columns = minis)
del dados


df_dados = df_dados.iloc[365:,:]
# -- calcula vazoes de referencia
qm = df_dados.mean(axis=0)
q90 = df_dados.quantile(0.1,axis=0)
q95 = df_dados.quantile(0.05,axis=0)
#  ... minibacias nas linhas (indices) e vazoes nas colunas (atributos)
del df_dados

# -- salva
df = pd.concat([qm,q90,q95],axis=1)
df.columns = ['qmlt','q90','q95']
df.index.name = 'mini'

# -- df.round(6).to_csv('qtudo_stats.txt',sep=' ')

