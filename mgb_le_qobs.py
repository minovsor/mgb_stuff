# -*- coding: utf-8 -*-
"""
LEITURA QOBS

@author: MINO SORRIBAS
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime,timedelta

def le_qobs(fil_qobs = 'QOBS.qob'):

    # ARQUIVO COM VAZOES OBSERVADAS
    #fil_qobs = 'QOBS.qob'
    with open(fil_qobs,'r') as f:
        lidos = f.readlines()
        header_0 = lidos[0].split()
        dados = []
        for i in lidos[1:]:
            line = i.split()
            dia,mes,ano = list(map(int,line[:3]))
            valores = list(map(float,line[3:]))
            dados.append([datetime(ano,mes,dia)] + valores)
        header = ['datetime'] + header_0[3:]
        df_qobs = pd.DataFrame(dados, columns=header)
        df_qobs = df_qobs.set_index('datetime')
    
    return df_qobs
    
