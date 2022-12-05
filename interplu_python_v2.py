
import numpy as np
import pandas as pd
import json


# parametros
p = 2
dmax = 3.
filter_dates = False
mini_gtp = 'mini.gtp'
grid_csv = 'grid.csv'
pathout = './'

# le mini e armazena matriz de dados
dados = np.loadtxt(mini_gtp,skiprows=1)
# salva minibacia e coordenadas
mini_xy = dados[:,[1,2,3]]


# obtem o grid
df = pd.read_csv(grid_csv)

# inclui coordenadas
df_coords = df.apply(lambda x:json.loads(x['.geo'])['coordinates'], axis = 1, result_type='expand')
df_coords.columns = ['lon','lat']

# remove colunas desnecessarias
df = df.drop(['.geo','system:index'],axis=1)

# dados vetorizados
xyg = df_coords.values
precg = df.values       # grid de chuva [ngrid,nt]

# datas
datas = pd.to_datetime( df.columns ) # a partir das colunas do df original.
d1 = min(datas).strftime('%Y-%m-%d')
d2 = max(datas).strftime('%Y-%m-%d')

# filtragem de intervalo
if filter_dates:
    # transpoe o df para obter a sequencia de datas
    dft = df.T.copy()
    dft['datas'] = datas[:]
    dft = dft.set_index('datas')

    # sobrepoe o grid de chuva
    precg = dft.T.values


# loop nas minibacias
nc = len(mini_xy)
ng, nt = precg.shape
#print(nc,ng,nt)
results = []
for row in mini_xy:

    # mini e coordenadas
    ic = int(row[0])
    xyc = row[1:]

    # distancia ate os pontos de grid (ou de estacoes)
    dx = np.subtract.outer(xyc[0],xyg[:,0])
    dy = np.subtract.outer(xyc[1],xyg[:,1])
    dist = np.hypot(dx,dy)

    # verifica postos com chuva
    precs = np.zeros((nt))
    for j in range(nt):
        m = precg[:,j]>=0.
        dmin = np.where(m,dist,999999).min()
        dmax = 10.*dmin
        igood = (m & (dist<dmax) )  #pts uteis

        if any(igood):
            # ponderacao inverso distancia
            w = 1./(dist**p)
            w = np.where(np.isinf(w),1.,w)  # evita problemas em pontos proximos
            w = np.where(igood,w,0.)        # mantem pontos bons
            w /= w.sum(axis=0)              # normaliza
            w = w[np.newaxis,:]             # [1,ngrid]

            precs[j] = np.dot(w, precg[:,j])[0]
        else:
            precs[j] = 0.

    # aplica ao longo do tempo e armazena
    i = ic - 1
    results.append(precs)

    '''

    # ponderacao inverso distancia
    w = 1./(dist**p)
    w = np.where(np.isinf(w),1.,w)  # evita problemas em pontos proximos
    w = np.where(dist>3.,0.,w)    # zera grid distante
    w /= w.sum(axis=0)              # normaliza
    w = w[np.newaxis,:]             # [1,ngrid]

    # aplica ao longo do tempo e armazena
    i = ic - 1
    precs = np.dot(w, precg) #.flatten())
    results.append(precs)
    '''

    #if ic==1:
    #    print(xyc)
    #    print(xyg)
    #    print(dist)
    #    print(1./dist**p)
    #    print(w)

# armazena em matriz e ajusta dimensao para fortran
pcalc = np.array(results)

# salva em arquivo binario real4 little-endian
pcalc = pcalc.T
rainbin = pathout + 'rainbin.pbi'
_ = np.array(pcalc, order = 'F', dtype='<f4').tofile(rainbin)

# salva arquivo com informacoes em texto.
with open(pathout + 'rainbin.info','w') as f:
    f.write(f'NT = {nt}\n')
    f.write(f'NC = {nc}\n')
    f.write(f'DINI = {d1}\n')
    f.write(f'DFIM = {d2}\n')
