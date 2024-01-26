# -*- coding: utf-8 -*-
"""
MAKES INTERPLU.HIG

@author: MINO SORRIBAS
"""

from datetime import datetime
import pandas as pd



# exporta chuvabin
def interplu_hig_header(dia, mes, ano, diaf, mesf, anof, nt, nu, nc, ng):
    """ monta cabecalho do interplu.hig
        dia,mes,ano :: data inicial
        diaf,mesf,anof :: data final
        nt,nu,nc :: numero de intervalos, urhs e catchments
        ng :: numero de postos/gauges/grid points
        
        df_pts :: pd.DataFrame([,,,],columns=['lon','lat','file'])
    """
    
    #check if nt makes sense
    ntx = (datetime(anof,mesf,diaf)-datetime(ano,mes,dia)).days
    if ntx!=nt:
        return f' ATENÇÃO: VERIFIQUE NT={nt} x NTx={ntx}\n'
    
    line = '!start \n'
    line += 'DAY'.rjust(10) + 'MONTH'.rjust(10) + 'YEAR'.rjust(10) + '\n'
    line += f'{dia}'.rjust(10) + f'{mes}'.rjust(10) + f'{ano}'.rjust(10) + '\n'

    line += '!end \n'
    line += 'DAY'.rjust(10) + 'MONTH'.rjust(10) + 'YEAR'.rjust(10) + '\n'
    line += f'{diaf}'.rjust(10) + f'{mesf}'.rjust(10) + f'{anof}'.rjust(10) + '\n'
    
    line += 'NC'.rjust(10) + 'NU'.rjust(10) + 'NT'.rjust(10)  + 'NP'.rjust(10) + '     (number of cells, HRCs, time intervals, stations)\n'
    line += f'{nc}'.rjust(10) + f'{nu}'.rjust(10) + f'{nt}'.rjust(10) + f'{ng}'.rjust(10) + '\n'

    line += '!FROM WHICH TIME INTERVAL DO YOU WANT TO START THE INTERPOLATION?\n'
    line += '1'.rjust(10) + f'        !CORRESPONDS TO {dia}/{mes}/{ano}\n'
    
    line += '!Grads file generation (1 to turn on - 0 turn off, matrix cell size) \n'

    line += "         0       0.1     '09:00z01jan1968       1dy'\n"
    
    line += "              code               long dec      lat dec \n"
    
    return line


def interplu_hig_postos(df_pts):
    """ monta linha para cada posto para a lista em interplu.hig """
    line_postos = ''
    for i,row in df_pts.iterrows():        
        line_postos += row.file.rjust(19) + f'{row.lon:.3f}'.rjust(21) + f'{row.lat:.3f}'.rjust(19) +'\n' 
    return line_postos


def interplu_hig_salva(dia, mes, ano, diaf, mesf, anof, nt, nu, nc, ng, df_pts, interplu_out = 'INTERPLU.HIG'):
    """ monta cabecalho e linhas de postos de uma vez """
    
    interplu_hig = interplu_hig_header(dia,mes,ano,diaf,mesf,anof,nt,nu,nc,ng)
    interplu_hig += interplu_hig_postos(df_pts)
    
    with open(interplu_out,'w') as f:
        f.write(interplu_hig)
    return print('gravou INTERPLU.HIG')


def interplu_hig_exemplo():
    
    dados = [
        [-43.850, -17.750,'00000000.txt'],
        [-43.750, -17.750,'00000001.txt'],
            ]
    df_pts = pd.DataFrame(data = dados, columns=['lon','lat','file'])
    
    # INPUT
    ng = df_pts.shape[0]
    dia, mes, ano = 1,1,1990
    diaf, mesf, anof = 31,12,2014
    nt = 2 #9130
    nu = 10
    nc = 1000   
    
    # RUN
    interplu_hig_salva(dia, mes, ano, diaf, mesf, anof, nt, nu, nc, ng, df_pts, 'EXEMPLO_INTERPLU.HIG')
    return _