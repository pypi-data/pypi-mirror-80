#!/usr/bin/env python
# 
from __future__ import print_function
import os, sys, re
import numpy as np
from astropy.table import Table
import pymc3
import corner
from scipy import optimize

script_dir = os.path.dirname(__file__)
if not script_dir in sys.path:
    sys.path.append(script_dir)

from read_model_grid import read_model_grid_interpolator_for_line_ratio


def fit_line_ratio(z=None, unit_scale = 'Jansky', **kwargs):
    
    # check input z 
    if z is None:
        print('Please input a redshift, e.g., z=4.0')
        sys.exit()
    
    # check input unit_scale
    if unit_scale not in ['Jansky', 'Kelvin']:
        raise ValueError('Error! unit_scale must be either \'Jansky\' or \'Kelvin\'!')
    
    # prepare acceptable_keys
    acceptable_keys = {}
    # only accept CO(12-11) to CO(1-0)
    for i in range(1,12+1):
        for j in range(1,12+1):
            if j != i:
                acceptable_keys['R%d%d'%(i, j)] = ('CO%d%d'%(i, i-1), 'CO%d%d'%(j, j-1))
    
    for i in range(1,12+1):
        for j in range(1,2+1):
            if j != i:
                acceptable_keys['RCO%dCI%d'%(i, j)] = ('CO%d%d'%(i, i-1), 'CI%d%d'%(j, j-1))
    
    for i in range(1,2+1):
        for j in range(1,12+1):
            if j != i:
                acceptable_keys['RCI%dCO%d'%(i, j)] = ('CI%d%d'%(i, i-1), 'CO%d%d'%(j, j-1))
    
    # check input key
    #if len(kwargs.keys()) > 1:
    #    raise Exception('Error! Please input only one line ratio! Input arguments: %s'%(kwargs.keys()))
    
    for key in kwargs.keys():
        if not key.startswith('R'):
            continue
        if key not in acceptable_keys:
            raise ValueError('Error! The input argument %r is not in the acceptable key list: \n[%r]'%(key, ', '.join(list(acceptable_keys.keys()))))
        
        # 
        interpolator = read_model_grid_interpolator_for_line_ratio(z, which_lines=acceptable_keys[key], unit_scale=unit_scale)
        
        
        # function to find the value in interpolation grid
        #def my_MCMC_func(x, a, b, c, d):
        #    print('a', float(a))
        #    return interpolator(np.array([a, b, c, d]))
        #
        ## 
        #with pymc3.Model() as M_model:
        #    # 
        #    # priors
        #    a = pymc3.Uniform('a', z-0.01, z+0.01, testval = z) # z
        #    b = pymc3.Uniform('b', 3.0, 6.8, testval = 4.0) # lg_nH2
        #    c = pymc3.Uniform('c', 4.0, 5.25, testval = 5.0) # lg_nthresh
        #    d = pymc3.Uniform('d', 25.0, 100.0, testval = 50.0) # T_kin
        #    # 
        #    x = np.array([1.0])
        #    y = np.array([kwargs[key]])
        #    if 'e_'+key in kwargs:
        #        yerr = np.array([kwargs['e_'+key]])
        #    else:
        #        yerr = y * 0.2
        #    # 
        #    # func
        #    M_func = pymc3.Deterministic('M_func', my_MCMC_func(x, a, b, c, d) )
        #    # 
        #    # likelihood
        #    M_fit = pymc3.Normal("M_fit", mu=M_func, tau=1.0/((yerr)**2), observed=y)
        #    # 
        #    # sample
        #    trace = pymc3.sample(int(3000))
        #    # 
        #    # save to disk
        #    #pymc3.save_trace(trace, 'my_trace', overwrite=True)
        #    # 
        #    # extract results
        #    MDL_stats = {}
        #    for k in ['a','b','c','d']:
        #        MDL_stats[k] = {}
        #        MDL_stats[k]['mean'] = np.percentile(trace[k], 50, axis=0)
        #        MDL_stats[k]['L68'] = np.percentile(trace[k], 16, axis=0)
        #        MDL_stats[k]['H68'] = np.percentile(trace[k], 84, axis=0)
        #    # 
        #    samples = np.vstack([trace[k] for k in ['a','b','c','d']]).T
        #    print(samples.dtype)
        #    tmp = corner.corner(samples[:], labels=['a','b','c','d'], truths=[MDL_stats[k]['mean'] for k in ['a','b','c','d']]) # truths=[alpha_true, beta_x_true, beta_y_true, eps_true]
        #    tmp.savefig('Results_of_pymc3_fitting_%s_corner.pdf'%(key))
        #    #print('Saved to "Plot_pymc3_corner.pdf"!')
        #    # 
        #    # save to disk
        #    with open('Results_of_pymc3_fitting_%s.json'%(key), 'w') as fp:
        #        json.dump(MDL_stats, fp, sort_keys=True, indent=4)

        
        # 
        # scipy.optimize.minimize
        # 
        
        y = np.log10(kwargs[key]) # log10
        if 'e_'+key in kwargs:
            yerr = (kwargs['e_'+key]) / (kwargs[key]) * 1.08
        else:
            yerr = y*0.0 + 0.1
        
        #print('np.isscalar(y)', np.isscalar(y))
        if np.isscalar(y):
            y = np.array([y])
        
        #print('np.isscalar(yerr)', np.isscalar(yerr))
        if np.isscalar(yerr):
            yerr = np.array([yerr])
        
        #print('np.isscalar(z)', np.isscalar(z))
        if np.isscalar(z):
            z = np.array([z])
        
        #print('len(z)', len(z))
        #print('len(y)', len(y))
        #print('len(yerr)', len(yerr))
        if len(z) == 1 and len(y) > 1:
            z = y*0.0 + z # one z for all y
        elif len(z) > 1 and len(y) > 1 and len(z) != len(y):
            raise ValueError('Error! The input redshift is an array and it does not match the input %r array size of %d (len(z)=%d).'%(key, len(y), len(z)))
        
        
        #def my_fit_func(p):
        #    b, c, d = p
        #    ytofit = interpolator(z, b, c, d)
        #    return ytofit-y
        #result = optimize.minimize(my_fit_func, np.array([3.0, 3.0, 50.0]))
        #print('result', result)
        #result       fun: array([nan])
        
        fit_results = []
        
        for i in range(len(z)):
            
            print('Fitting %d/%d, z=%s, y=%s, yerr=%s'%(i+1, len(z), z[i], y[i], yerr[i]))
            
            b = np.arange(2.0, 5.0+0.05, 0.01) # lg_nH2
            c = np.arange(4.0, 5.0+0.2, 0.2) # lg_nthresh
            d = np.arange(25, 100+5.0, 1.0) # T_kin
            coords = np.zeros((1, len(b), len(c), len(d), 4))
            coords[..., 0] = np.log10(1.0+z[i])
            coords[..., 1] = b.reshape((1, len(b), 1, 1))
            coords[..., 2] = c.reshape((1, 1, len(c), 1))
            coords[..., 3] = d.reshape((1, 1, 1, len(d)))
            coords = coords.reshape(1*(len(b)*len(c)*len(d)), 4)
            ytofit = interpolator(coords)
            #print('ytofit.shape', ytofit.shape)
            
            if np.isfinite(y[i]) and not np.isnan(y[i]):
                
                wherebestfit = np.nanargmin(np.abs(ytofit - y[i]))
                #print('wherebestfit', wherebestfit)
                ybestfit = ytofit[wherebestfit]
                #for idx in [wherebestfit]:
                #    print(idx, coords[idx], ytofit[idx], y, yerr)
                
                # generate N times realization
                ndisturbed = 300
                ydisturbed = np.random.normal(y[i], yerr[i], ndisturbed)
                #print('ydisturbed', ydisturbed)
                pdisturbed = [[], [], [], []]
                wherefit = [np.nanargmin(np.abs(ytofit - t)) for t in ydisturbed]
                #print('wherefit', wherefit)
                pdisturbed[0] = [coords[t][0] for t in wherefit]
                pdisturbed[1] = [coords[t][1] for t in wherefit]
                pdisturbed[2] = [coords[t][2] for t in wherefit]
                pdisturbed[3] = [coords[t][3] for t in wherefit]
                
                #wherefit = np.argwhere(np.abs(ytofit - y) <= np.abs(yerr))
                #print('wherefit', wherefit)
                #for idx in wherefit:
                #    print(idx, coords[idx], ytofit[idx], y, yerr)
                
                #bestfit = coords[wherebestfit]
                #fit_L68 = [np.percentile(pdisturbed[0], 16, axis=0), 
                #           np.percentile(pdisturbed[1], 16, axis=0), 
                #           np.percentile(pdisturbed[2], 16, axis=0), 
                #           np.percentile(pdisturbed[3], 16, axis=0)]
                #fit_H68 = [np.percentile(pdisturbed[0], 84, axis=0), 
                #           np.percentile(pdisturbed[1], 84, axis=0), 
                #           np.percentile(pdisturbed[2], 84, axis=0), 
                #           np.percentile(pdisturbed[3], 84, axis=0)]
                
                fit_result = {}
                fit_result['z'] = {}
                fit_result['z']['best'] = 10**(coords[wherebestfit][0])-1.0 # inside the fitting it is log10(1.0+z)
                fit_result['z']['median'] = 10**(np.percentile(pdisturbed[0], 50, axis=0))-1.0
                fit_result['z']['L68'] = 10**(np.percentile(pdisturbed[0], 16, axis=0))-1.0
                fit_result['z']['H68'] = 10**(np.percentile(pdisturbed[0], 84, axis=0))-1.0
                fit_result['lg_nH2'] = {}
                fit_result['lg_nH2']['best'] = coords[wherebestfit][1]
                fit_result['lg_nH2']['median'] = np.percentile(pdisturbed[1], 50, axis=0)
                fit_result['lg_nH2']['L68'] = np.percentile(pdisturbed[1], 16, axis=0)
                fit_result['lg_nH2']['H68'] = np.percentile(pdisturbed[1], 84, axis=0)
                fit_result['lg_nthresh'] = {}
                fit_result['lg_nthresh']['best'] = coords[wherebestfit][2]
                fit_result['lg_nthresh']['median'] = np.percentile(pdisturbed[2], 50, axis=0)
                fit_result['lg_nthresh']['L68'] = np.percentile(pdisturbed[2], 16, axis=0)
                fit_result['lg_nthresh']['H68'] = np.percentile(pdisturbed[2], 84, axis=0)
                fit_result['T_kin'] = {}
                fit_result['T_kin']['best'] = coords[wherebestfit][3]
                fit_result['T_kin']['median'] = np.percentile(pdisturbed[3], 50, axis=0)
                fit_result['T_kin']['L68'] = np.percentile(pdisturbed[3], 16, axis=0)
                fit_result['T_kin']['H68'] = np.percentile(pdisturbed[3], 84, axis=0)
                fit_result['key'] = key
                fit_result['y'] = 10**y
                fit_result['y_best_fit'] = 10**ybestfit
                fit_result['best_chisq'] = (ybestfit - y[i])**2 / yerr[i]**2
                
                fit_results.append(fit_result)
            
            else:
                
                fit_result = {}
                fit_result['z'] = {}
                fit_result['z']['best'] = z[i]
                fit_result['z']['median'] = np.nan
                fit_result['z']['L68'] = np.nan
                fit_result['z']['H68'] = np.nan
                fit_result['lg_nH2'] = {}
                fit_result['lg_nH2']['best'] = np.nan
                fit_result['lg_nH2']['median'] = np.nan
                fit_result['lg_nH2']['L68'] = np.nan
                fit_result['lg_nH2']['H68'] = np.nan
                fit_result['lg_nthresh'] = {}
                fit_result['lg_nthresh']['best'] = np.nan
                fit_result['lg_nthresh']['median'] = np.nan
                fit_result['lg_nthresh']['L68'] = np.nan
                fit_result['lg_nthresh']['H68'] = np.nan
                fit_result['T_kin'] = {}
                fit_result['T_kin']['best'] = np.nan
                fit_result['T_kin']['median'] = np.nan
                fit_result['T_kin']['L68'] = np.nan
                fit_result['T_kin']['H68'] = np.nan
                fit_result['key'] = key
                fit_result['y'] = 10**y
                fit_result['y_best_fit'] = np.nan
                fit_result['best_chisq'] = np.nan
                
                fit_results.append(fit_result)
        
        return fit_results
        
        
        
        



