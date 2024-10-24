# -*- coding: utf-8 -*-
"""
CALCULA ESTATISTICAS PARA O MGB

@author: MINO SORRIBAS
"""

import numpy as np

def mgb_metrics(xobs, xsim, iniaju = 0, trans = 0, lowflow = 0):

  
    # Initialize output arrays
    metrics_names = ['n','nse','erv','kge_m','rmse',
                     'kge_corr','kge_bias','kge_var']       
    metrics = np.full(8, None)
    d_metrics = {k:v for k,v in zip(metrics_names,metrics)}
 
    # Convert Q<0 to np.nan, assume Q>0 can occur, like in simulation
    xobs[xobs<0.0] = np.nan
    xsim[xsim<0.0] = np.nan
 
    # Check if INIAJU is greater than N
    n = xobs.shape[0]
    if iniaju > n:        
        return d_metrics

    # Work with a copy to allow for transformations
    obs = np.copy(xobs[iniaju:])
    sim = np.copy(xsim[iniaju:])

    # Apply log or sqrt transformation if needed
    if trans == 1:
        obs = np.where(obs >= 0.0, np.log(obs + 0.0001), np.nan)
        sim = np.where(sim >= 0.0, np.log(sim + 0.0001), np.nan)
    elif trans == 2:
        obs = np.where(obs >= 0.0, np.sqrt(obs), np.nan)
        sim = np.where(sim >= 0.0, np.sqrt(sim), np.nan)

    # Compute mean of OBS and SIM values
    valid_indices = np.where(obs > 0.0)[0]
    if len(valid_indices) == 0:
        return d_metrics
    mean_obs = np.mean(obs[valid_indices])
    mean_sim = np.mean(sim[valid_indices])

    # Keep only low flow if LOWFLOW ==1
    if lowflow == 1:
        obs[obs <= mean_obs] = np.nan
        sim[sim <= mean_sim] = np.nan
        valid_indices = np.where(obs >= 0.0)[0]
        if len(valid_indices) == 0:
            return d_metrics
        # recalculate means        
        mean_obs = np.mean(obs[valid_indices])
        mean_sim = np.mean(sim[valid_indices])

    # Compute variance and covariance
    var_obs = np.var(obs[valid_indices])
    var_sim = np.var(sim[valid_indices])
    covar = np.cov(obs[valid_indices], sim[valid_indices])[0, 1]
    residuals = obs[valid_indices] - sim[valid_indices]
    sum_residuals_sq = np.sum(residuals**2)

    # Compute Nash-Sutcliffe Efficiency (NSE)
    sum_obs_sq = np.sum((obs[valid_indices] - mean_obs)**2)
    nse = 1.0 - sum_residuals_sq / sum_obs_sq

    # Compute Volume Error
    erv = (mean_sim / mean_obs - 1.0) * 100.0

    # Compute Kling-Gupta Efficiency (KGE)
    correlation = covar / np.sqrt(var_obs * var_sim)
    bias = mean_sim / mean_obs
    variability = (np.sqrt(var_sim) / mean_sim) / (np.sqrt(var_obs) / mean_obs)
    kge = 1.0 - np.sqrt((correlation - 1.0)**2 + (bias - 1.0)**2 + (variability - 1.0)**2)

    # Compute RMSE
    rmse = np.sqrt(sum_residuals_sq)

    # Estimate sigma as the standard deviation of residuals
    residual_variance = np.var(residuals)
    sigma = np.sqrt(residual_variance)
    rss = sum_residuals_sq
    l_res = rss / (2.0 * sigma**2) + np.log(sigma * np.sqrt(2.0 * np.pi))

    # Compute likelihoods
    l_nse = -1.0 / (2.0 - nse)
    l_kge = -kge

    # Output results
    metrics[0] = float(len(valid_indices))
    metrics[1] = nse
    metrics[2] = erv
    metrics[3] = kge
    metrics[4] = rmse
    metrics[5] = correlation
    metrics[6] = bias
    metrics[7] = variability
    d_metrics = {k:v for k,v in zip(metrics_names,metrics)}

    return d_metrics


def table_ecdf(x, method='default',ascending=True):
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
        
    return xs, ys
