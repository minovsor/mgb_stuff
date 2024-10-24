# -*- coding: utf-8 -*-
"""
ANO HIDROLOGICO

@author: MINO SORRIBAS
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def ano_hidro(ano, mes, mesini = 10):    
    mes_novo = mes - mesini + 1
    if mes_novo > 0:
        ano = ano
        mes = mes_novo
    else:
        mes = mes_novo + 12
        ano = ano - 1
    return int(ano), int(mes)

@np.vectorize
def vec_ano_hidro(ano, mes, mesini = 10):    
    mes_novo = mes - mesini + 1
    if mes_novo > 0:
        ano = ano
        mes = mes_novo
    else:
        mes = mes_novo + 12
        ano = ano - 1
    return int(ano), int(mes)


def df_to_anohidro(df, mesini = 10, expand = False):
    df_out = index_to_anohidro(df.index, mesini = mesini)
    if expand:
        df_out = pd.concat([df,df_out],axis=1)
    return df_out

def index_to_anohidro(dt_index, mesini = 10):    
    idx_hidro = dt_index.map(lambda x:ano_hidro(x.year, x.month, mesini = mesini))
    idx_hidro.names = ['year_h','month_h']
    return idx_hidro.to_frame()[['year_h','month_h']].set_index(dt_index)


def cols_to_anohidro(df, col_ano, col_mes, mesini):
        return df.apply(
            lambda x: ano_hidro(x[col_ano],x[col_mes], mesini = mesini),axis=1,
            result_type='expand').astype(int)  