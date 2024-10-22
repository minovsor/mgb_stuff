# -*- coding: utf-8 -*-
"""
LE PARUSO

@author: Mino
"""


paruso = 'PARUSO.cal'


with open(paruso,'r') as f:
    # read all lines
    lido = f.readlines()

    # delete final empty lines
    reverse = lido[::-1]
    for i,v in enumerate(reverse):
        if 'qb' in v.lower():
            break
    lido = reverse[i:][::-1]

    # declare headers
    wsh_header = 'Watershed <id>\n'
    var_header = '       hru      Wm       b    Kbas    Kint      XL     CAP      Wc\n'

    # find number of HRU's
    for i,v in enumerate(lido):
        if 'wm' in v.lower(): # busca cabecalho
            ihru = i + 1
        if 'cs' in v.lower(): # busca fim das linhas de hru
            ics = i
            break
    nhru = ics - ihru

    # get HRU names
    hru_names = []
    for i in lido[ihru:ics]:
        hru_names.append(i.split()[0])

    # subbasin block size
    nlin = len(lido)
    nn = 2 + nhru + 4   # 2 headers, n-hru params, cs/ci/cb, qesp
    if nlin % nn !=0:
        print('something wrong in file')
        return None

    # split blocks
    i = 0
    nb = 0
    params = {}
    while (i+nn <=nlin):
        nb = nb + 1
        basin_block = lido[i:i+nn]
        params[nb] = basin_block

        # proximo
        j = i+nn
        i = j

    return params