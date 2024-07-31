# -*- coding: utf-8 -*-
"""
GERADOR DE QOBS COM UMA COLUNA DE FALHAS

@author: MINO SORRIBAS
"""

from datetime import datetime,timedelta

#
iano = 2015
imes = 1
idia = 16
nt = 25918


# vamos falsificar o qobs com falhas
txt = '    Day    Month   Year        00000001\n'
d0 = datetime(*tuple(map(int,[iano,imes,idia])))
for i in range(0,nt):
    data = d0 + timedelta(days=i)
    dia = f'{str(data.day).zfill(2).rjust(7)}'
    mes = f'{str(data.month).zfill(2).rjust(7)}'
    ano = f'{str(data.year).rjust(6)}'
    falha = f'{-1:.7f}'.rjust(16)
    txt +=  dia+mes+ano+falha+'\n'
    
with open('qobs_fake.txt','w') as f:
    f.write(txt)