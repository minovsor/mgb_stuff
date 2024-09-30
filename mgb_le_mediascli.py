"""
LE ARQUIVOS MEDIAS.CLI

@author: Mino
"""

from datetime import datetime
import pandas as pd



def mgb_read_mediascli(fileclim = 'medias.cli',
                       pathout = None,
                       pathout_others = None):
    
    with open(fileclim,'r') as f:
        linhas = f.readlines()
    
    # identifica numero de postos
    for i,line in enumerate(linhas):    
        if '*' in line:
            nclim = i
            break
    
    # organiza informacao dos postos
    postos= []
    for line in linhas[:nclim]:
        txt = line.strip().split()
        lon, lat = float(txt[0]), float(txt[1])
        codigo = txt[2]
        nome = ' '.join(txt[3:])
        postos.append([lon,lat,codigo,nome])
    
    df_gauges = pd.DataFrame(postos,columns=['lon','lat','code','name'])
    #... importante manter 'lon' e 'lat' pq usa no outro script de interplacao
   
    # auxiliares
    meses = [datetime(2024,m,1).strftime('%b') for m in range(1,13)]
    cols = ['codigo','nome'] + meses    

    # identifica linha do cabecalho de cada tipo de dado
    headers = {i:line for i,line in enumerate(linhas) if '*' in line}
    
    # identifica variaveis
    target_vars = {'temperature':'tas',
                   'humidity':'hurs',
                   'insolation':'insola',
                   'wind':'sfcwind',
                   'pressure':'ps',
                   }
    headers_vars = {}
    for k,v in headers.items():
        for kt, vt in target_vars.items():
            if kt in v.lower():
                #print(v,t)
                headers_vars[k] = vt   #atribui algo como {<nclim>: 'tas',}
            continue
       
    # leitura de dados de cada variavel
    dataframes_clima = {}
    for k in headers.keys():
        name = headers_vars[k]
        kk = k + 2
        j0 = kk
        j1 = kk + nclim
        coleta = []
        for d in linhas[j0:j1]:
            txt = d.split()
            codigo = txt[0]
            nome = txt[1]
            xval = list(map(float,txt[-12:]))    
            if len(txt)>14:
                nome = ' '.join(txt[::-1][12:][::-1][1:])
            coleta.append([codigo, nome] + xval)
        dataframes_clima[name] = pd.DataFrame(coleta, columns = cols)
        #... {'tas':pd.DataFrame, ...}
    
    # exporta para excel
    for k, df in dataframes_clima.items():
        if k =='tas':
            if pathout is not None: 
                df.to_excel(pathout + '_CLIMATOLOGY_REFERENCE_tas.xlsx')
        else:
            if pathout_others is not None: 
                df.to_excel(pathout_others + f'_CLIMATOLOGY_REFERENCE_{name}.xlsx')
            
    return df_gauges, dataframes_clima