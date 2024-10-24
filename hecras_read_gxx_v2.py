# -*- coding: utf-8 -*-
"""

Reads XS from simple geometry files of HEC-RAS

with some more recent alteration

Dec/2020

@author: Mino Sorribas
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# read geometry file
file = 'DRE_JoaoNeiva.g03'
with open(file,'r') as f:
    dados = f.readlines()
dados = [i.rstrip() for i in dados]


# get xs from geometry
dict_station = {}
nlin = len(dados)
i=0
rm_order = -1
while(i<nlin):


    line = dados[i]
    
    #TODO:
    #Junct Name=Junction 1      
    #Junct Desc=, 0 , 0 , 0 ,-1
    #Junct X Y & Text X Y=355068.25,7814894.5,355068.25,7814894.5
    #Up River,Reach=DEMETRIO        ,Afluente
    #Up River,Reach=PIRAQUE         ,Superior
    #Dn River,Reach=PIRAQUE         ,Inferior
    #Junc L&A=24.2,
    #Junc L&A=11.9,
    
    # IDENTIFICA TRECHO DO RIO
    if 'River Reach=' in line:
        print(line)
        values = line.split('=')[-1]
        RIVER, REACH = values.split(',')
        RIVER = RIVER.strip()
        REACH = REACH.strip()
        
    

    if 'Reach XY' in line:  #XS GIS
        print(line)      
        # #Reach XY=
        nxs = int(line.split('=')[-1])
        # get inverts coordinates
        strsize = 16
        invert_xy = []
        ixs=0
        while ixs<nxs:
            i = i+1
            line = dados[i]
            values = [float(line[i:i+strsize]) for i in range(0, len(line), strsize)]
            cpairs = [values[i:i+2] for i in range(0,len(values),2)]  #break in pairs
            invert_xy.extend(cpairs)
            ixs = len(invert_xy)
            

    if 'Type RM' in line:   #XS REACH INFO
        
        # indexador
        rm_order = rm_order+1
        
        #-----------------------
        # #Type RM Length L Ch R =
        #-----------------------
        values = line.replace('=',',').split(',')[-5:]
        Tipe,RM, L,Ch,R = [float(i) for i in values]
        
        # next line
        i = i+1
        line = dados[i]
        
        #-----------------------
        # READ DESCRIPTION
        #-----------------------
        if 'BEGIN DESCRIPTION' in line:
            description = ''
            _flag=True
            while (_flag):
                i = i+1
                line = dados[i]
                if 'END DESCRIPTION' not in line:
                    description = description + '\n' + line
                else:
                    _flag=False           
  
        # next line
        #i = i+1
        #line = dados[i]
        
        #-----------------------
        # #XS GIS Cut Line
        #-----------------------
        if 'XS GIS Cut Line' in line:
            print(i,line)

            ncut = int(line.split('=')[-1])
            # get cutline coordinates
            strsize = 16
            cutline_xy = []
            icut = 0
            while icut<ncut:
                i = i + 1
                line = dados[i]
                values = [float(line[i:i+strsize]) for i in range(0, len(line), strsize)]
                cpairs = [values[i:i+2] for i in range(0,len(values),2)]  #break in pairs
                cutline_xy.extend(cpairs)
                icut = len(cutline_xy)
    
            # #Node Last Edited Time=
            i = i + 1
            line = dados[i]
    
            # #Sta/Elev=
            i = i + 1
            line = dados[i]
            npair = int(line.split('=')[-1])  ##Sta/Elev=npair
            #get xs pairs values
            strsize=8
            ipair = 0
            staelev = []
            while ipair<npair:
                i = i+1
                line = dados[i]
                try:
                    #values = [float(i) for i in line.split()] #fails when has mergedvalues
                    values = [float(line[i:i+strsize]) for i in range(0, len(line), strsize)]
                    cpairs = [values[i:i+2] for i in range(0,len(values),2)]  #break in pairs
                    staelev.extend(cpairs)
                    ipair = len(staelev)
                except:
                    npair=npair-1
    
    
            # Processing dataset
            # make np table
            staelev_arr = np.array(staelev)
    
            # get start-end cutlines
            x1,y1 = cutline_xy[0]
            x2,y2 = cutline_xy[-1]
              
    
            dict_station[rm_order] = {
                'rm_order':rm_order,
                'rm':RM,
                'cutline':[[x1,y1],[x2,y2]],
                'staelev':staelev_arr,
                'npair': npair,
                'river': RIVER, #atencao, supo-se que foi ordenado
                'reach': REACH,
                'lob': None,
                'rob': None,
                'zlob': None,
                'zrob': None,                
                }
            

            # Keep running lines trying to find the Bank Stations
            j = i
            _flag = True
            while (_flag):
                j = j + 1
                line = dados[j]
                if line =='':
                    _flag= False
                    continue
                if 'Bank Sta=' in line:
                    banks = line.split('=')[-1]
                    lob, rob = banks.split(',')
                    lob, rob = float(lob), float(rob)
                    
                    dict_station[rm_order]['lob'] = lob
                    dict_station[rm_order]['rob'] = rob
                    
                    ilob = np.flatnonzero(np.isclose(staelev_arr[:,0],lob))
                    irob = np.flatnonzero(np.isclose(staelev_arr[:,0],rob))
                    zlob = staelev_arr[ilob,1]
                    zrob = staelev_arr[irob,1]
                    
                    dict_station[rm_order]['zlob'] = zlob[0]
                    dict_station[rm_order]['zrob'] = zrob[0]
                    continue
                    
            

    #update counter
    i = i + 1



# sort descending (->downstream)
stations = sorted(dict_station,reverse=True)
ignore = [False] * len(stations)


#... at this point we have a nice dictionary 'dict_station'

# to query data
# use dict_station[<number_of_river_station_xs>]
# 'staelev' has the tabela x-z
# 'rm' has the river station


# store all xs in dataframe
# adatar
df_tudo = pd.DataFrame()
for i,d in dict_station.items():
    _staelev = d['staelev']    #coordenadas do perfil transversal
    df = pd.DataFrame(_staelev, columns=['x','z'])
    for k in ['rm_order', 'rm', 'npair', 'river', 'reach','lob','rob','zlob','zrob']:
        df[k] = d[k]


    #append
    df_tudo = pd.concat([df_tudo,df],axis = 0, ignore_index=True)

# export to excel
df_tabelao = df_tudo[['x','z','rm_order','rm', 'npair', 'river', 'reach']]
df_tabelao.to_excel('tabelao_xs.xlsx')

# export resumo xs
df_suma = df_tudo.sort_values('x').groupby(['river','reach','rm']).first()[::-1]

# inclui o comprmiento maximo
df_sumax = df_tudo.sort_values('x').groupby(['river','reach','rm']).last()[::-1]['x']
df_suma['xmax'] = df_sumax
df_suma = df_suma.reset_index()
df_suma.to_excel('sumario_xs.xlsx')


# GERANDO GEOMETRIAS COM INEFFECTIVE FLOW AREA
with open('output_xs.gxx','w') as f:
    txt = ''
    i = 0
    while (i<nlin):
        line = dados[i]
        txt = txt + line + '\n'
        
        if '#Sta/Elev' in line:
            line = dados[i+1]
            values = [float(i.strip()) for i in line.split()]
            xi, zi = values[0],values[1]
        
        if '#Mann' in line:
            # verifica ultimo par x-z
            _line = dados[i-1]
            values = [float(i.strip()) for i in _line.split()]
            xf, zf = values[-2],values[-1]
            # verifica se ha Innef
            line_ = dados[i+2]
            if '#XS Ineff' not in line_:
                if 'Bank Sta' in line_:
                    value = line_.split('=')[-1]
                    lob,rob = value.split(',')
                    lob,rob = float(lob.strip()),float(rob.strip())
                    lob,rob = round(lob,1),round(rob,1)
                
                    x1,z1,x2,z2 = round(xi,1),round(zi,1),round(xf,1),round(zf,1)
                    align = lambda x: str(x).rjust(8)
                    aux1 = align(x1) + align(lob) + align(z1)
                    aux2 = align(x2) + align(rob) + align(z2)
                    line1 = '#XS Ineff= 2 ,-1\n' + aux1 + aux2 +'\n'
                    line2 = 'Permanent Ineff=\n       T       T\n'
                    
                    # escreve os valores de manning
                    i = i+1
                    txt = txt + dados[i] + '\n'
                    
                    # escreve #XS Ineff
                    txt = txt + line1 + line2
                    
                    #avanca para #BankSta
                   # i = i+1
                    
                else:
                    print('bank not found')
        i = i+1
    
    f.write(txt)
        
    
