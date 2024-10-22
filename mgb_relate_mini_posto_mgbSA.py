
import numpy as np
from scipy.io import loadmat
import pandas as pd  


#fmat_codigos_ANA = './Code/Matlab/Variables/codes_ANA.mat'
#fmat_mini_ANA = './Code/Matlab/Variables/GaugeCentroid_ANA.mat'

# nome dos arquivos
fmat_codigos_ANA = 'codes_ANA.mat'
fmat_mini_ANA = 'GaugeCentroid_ANA.mat'

# leitura 
mini = loadmat(fmat_mini_ANA)['GaugeCentroid']
codes = loadmat(fmat_codigos_ANA)['codes']

# organiza os dados
lista_mini = mini.ravel().tolist()
lista_codes_str = list(map(lambda x:x[0],codes.ravel()))

# monta um dataframe e salva em excel
df = pd.DataFrame(index=lista_mini,data=lista_codes_str,columns=['posto_ANA'])
df.index.rename('mini',inplace=True)
df = df.sort_index()
df.to_excel('mini_posto_ANA.xlsx')
