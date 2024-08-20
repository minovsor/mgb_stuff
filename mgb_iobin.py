# -*- coding: utf-8 -*-
"""
LEITURA E ESCRITA DE ARQUIVOS BINARIOS

@author: MINO SORRIBAS
"""
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

def arr_to_binario(arr_dados, filebin, nt, nc, dstart, save_info=True):
    """ fornecendo a matriz com NT linhas e NC colunas
        gera binario similar a 'chuvabin' e um arquivo .info
    """
    
    # salva o binario
    _ = np.array(arr_dados, order = 'F', dtype='<f4').tofile(filebin)
    
    # salva info
    if save_info:
        ano, mes, dia = dstart.year, dstart.month, dstart.day
        fileinfo = filebin[:-4] + '.info'    
        num2str = lambda x:str(x).rjust(13)
        info = f'NT ={num2str(nt)}\n'
        info+= f'NC ={num2str(nc)}\n'
        info+= f'DINI (ANO,MES,DIA) =' + num2str(ano) + num2str(mes) + num2str(dia)
        with open(fileinfo,'w') as f:
            f.write(info)
    return 

def dataframe_to_mgb_binary(df_dados, filebin, save_info = True):
    arr_dados = df_dados.to_numpy()
    nt, nc = df_dados.shape
    dstart = df_dados.index[0].to_pydatetime()
    return arr_to_binario(arr_dados, filebin, nt, nc, dstart, save_info)



def read_mgb_binary(filebin, nt, nc):
    """ Read binary (MGB format) as np.array """
    #'<f4' indicates little-endian (<) float(f) 4 byte (4)
    arr_dados = np.fromfile(filebin,'<f4').reshape(nt,nc)
    return arr_dados


def read_mgb_binary_as_dataframe(filebin, nt, nc, dstart):
    """ Read full binary (MGB format) as dataframe """
    # read mgb binary
    arr_dados = read_mgb_binary(filebin, nt, nc)

    # make timeseries dataframe
    times = [dstart + timedelta(days=i) for i in range(nt)]
    df = pd.DataFrame(arr_dados, columns=range(1,nc+1), index=times)
    
    return df



def read_info_old(fileinfo):
    # le arquivo de informacoes
    info = pd.read_csv(fileinfo,sep='=',header=None)
    nt = int(info.loc[0,1])
    nc = int(info.loc[1,1])
    dstart = datetime(*list(map(int,info.loc[2,1].split())))
    return nt,nc,dstart


def read_info(fileinfo):
    # le arquivo de informacoes
    with open(fileinfo,'r') as f:
        lidos = f.readlines()
    # obtem nt e nc
    nt = int(lidos[0].split('=')[-1])
    nc = int(lidos[1].split('=')[-1])
    # obtem data de inicio
    txt = lidos[2]
    #  testa se esta usando '='
    if txt.split('=')[0]==txt:
        anomesdia = txt.split()[-3:]
        ano, mes, dia = list(map(int,anomesdia))
    else: #
        ano, mes, dia = list(map(int,(txt.split('=')[-1].split())))
    dstart = datetime(ano,mes,dia)

    return nt,nc,dstart


def read_chuvabin_as_dataframe(filebin, nt, nc, dstart):
    return read_mgb_binary_as_dataframe(filebin, nt, nc, dstart)

