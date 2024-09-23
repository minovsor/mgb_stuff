# MONTA TABELA DA CDF
@author: MINO SORRIBAS
import numpy as np
from scipy import interpolate,stats
def table_ecdf(x, method='default',ascending=True, simplify=100):
    
    # x: values, y:quantiles
    xs = np.sort(x)
    nx = float(len(xs))
    ix = np.arange(1, nx+1)    
    if not ascending:
        xs = xs[::-1]

    if method == 'default':        
        ys = ix/nx
    elif method =='weibull':
        ys = ix/(nx + 1)
    elif method == 'grigorten':   #extreme value I
        ys = (ix - 0.44)/(nx + 0.12)
    elif method == 'hazen':
        ys = (ix - 0.375)/(nx + 0.25)
    elif method == 'cunnane':
        ys = (ix - 0.40)/(nx + 0.20)
    elif method == 'hosking':
        ys = (ix - 0.35)/nx
    elif method == 'blom':
        ys = (ix - 0.5)/nx
    
    if (simplify>0 and simplify < ys.size):
        # interpolador de f(q) -> x
        yy = np.linspace(0.,1.,simplify)
        fint = interpolate.interp1d(ys, xs,
                                    fill_value=(xs[0],xs[1]),
                                    bounds_error=False)
        xs = fint(yy)
        ys = yy
    
    return xs, ys


def fit_cdf_tail(ecdf, qtail=0.9, distn='gamma'):
    """ essa funcao recebe a ecdf tabelada e ajusta dist na cauda superior"""
    dist_ref = getattr(stats,distn)
    x,cdf = ecdf
    a = x[cdf>qtail]
    params = dist_ref.fit(a)
    xtail = a[0]
    fitted_cdf_tail = {'distn': dist_ref.name,
                       'params': params,
                       'qtail': qtail,  #o quantil original usado no corte
                       'xtail': xtail,
                       }    
    return fitted_cdf_tail

 
def fn_x2F(x, x2F, fitted_cdf_tail):
    """ Dado valor de x, obtem quantil (0-1) a partir da ecdf interpolada
    ou do ajuste dist na cauda superior"""
    
    # tenta encontrar o quantil pelo valor na ecdf
    try:
        F = x2F(x)
        F = F.flatten()[0]
        branch = 'ecdf'
    except:
        # vai usar o ajuste de cauda
        distn = fitted_cdf_tail['distn']
        dist_ref = getattr(stats,distn)
        params = fitted_cdf_tail['params']
        F = dist_ref.cdf(x,*params)
        F = F.flatten()[0]
        # cuidado: ate aqui o quantil obtido é ao longo da cauda
        # branch = 'tail'
        # ajuste para final o quantil real
        q0 = fitted_cdf_tail['qtail']
        F = q0 + (1.-q0)*F   #ajusta pela proporcao da cauda
    return F #branch


def fn_F2x(q, F2x, fitted_cdf_tail):
    """ Dado o valor do quantil (0-1), obtem o valor na ecdf interpolada
    ou do ajuste de dist na cauda superior """
    
    # tenta obter o valor pelo quantil na ecdf
    try:
        x = F2x(q).flatten()[0]        
    except:
        # vai usar o ajuste da cauda
        distn = fitted_cdf_tail['distn']
        dist_ref = getattr(stats,distn)
        params = fitted_cdf_tail['params']
        # cuidado: precisamos ajustar o quantil na regiao da cauda
        q0 = fitted_cdf_tail['qtail']
        x0 = fitted_cdf_tail['xtail']
        qx = (q - q0)/(1-q0)
        x = dist_ref.ppf(q,*params)
    return x
