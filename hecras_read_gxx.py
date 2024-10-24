# -*- coding: utf-8 -*-
"""

Reads XS from simple geometry files of HEC-RAS

Dec/2020

@author: Mino Sorribas
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# read geometry file
file = 'geometria.g14'
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

    if 'Reach XY' in line:
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


    if 'Type RM' in line:

        rm_order = rm_order+1

        # #Type RM Length L Ch R =
        values = line.replace('=',',').split(',')[-5:]
        Tipe,RM, L,Ch,R = [float(i) for i in values]

        # #XS GIS Cut Line =
        i = i+1
        line = dados[i]
        ncut = int(line.split('=')[-1])
        # get cutline coordinates
        strsize = 16
        cutline_xy = []
        icut = 0
        while icut<ncut:
            i = i+1
            line = dados[i]
            values = [float(line[i:i+strsize]) for i in range(0, len(line), strsize)]
            cpairs = [values[i:i+2] for i in range(0,len(values),2)]  #break in pairs
            cutline_xy.extend(cpairs)
            icut = len(cutline_xy)

        # #Node Last Edited Time=
        i = i+1
        line = dados[i]

        # #Sta/Elev=
        i = i+1
        line = dados[i]
        npair = int(line.split('=')[-1])
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


        dict_station[RM] = {
            'rm_order':rm_order,
            'rm':RM,
            'cutline':[[x1,y1],[x2,y2]],
            'staelev':staelev_arr,
            'npair':npair,
            }

    #update counter
    i=i+1



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
    name = d['rm']
    staelev = d['staelev']
    df = pd.DataFrame(staelev,columns=['x','z'])
    df['rs'] = name

    #append
    df_tudo = pd.concat([df_tudo,df],axis = 0, ignore_index=True)

# export to excel
df_tudo.to_excel('tabelao_xs.xlsx')
