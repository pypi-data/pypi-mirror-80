#!/usr/bin/env python
# 

import os, sys, re
import numpy as np
from astropy.table import Table
from scipy import interpolate
from scipy.interpolate import LinearNDInterpolator


def read_model_grid_interpolator_for_line_ratio(z, which_lines, unit_scale = 'Jansky'):
    
    # check input unit_scale
    if unit_scale not in ['Jansky', 'Kelvin']:
        raise ValueError('Error! unit_scale must be either \'Jansky\' or \'Kelvin\'!')
    
    # check input which_lines
    if np.isscalar(which_lines):
        raise ValueError('Error! which_lines must be a list or tuple with two line names!')
    
    if len(which_lines) < 2:
        raise ValueError('Error! which_lines must be a list or tuple with two line names!')
    
    # load model grid big table
    table_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data_Tables', 'Liu2020_COexc_model577f_combined_modeled_line_flux_big_table.fits')
    tb = Table.read(table_file)
    
    # check input which_lines
    for i in range(len(which_lines)):
        if which_lines[i].find('-') >= 0:
            which_lines[i] = which_lines[i].replace('-','')
        if which_lines[i].find('[') >= 0:
            which_lines[i] = which_lines[i].replace('[','')
        if which_lines[i].find(']') >= 0:
            which_lines[i] = which_lines[i].replace(']','')
        if which_lines[i] not in tb.colnames:
            raise ValueError('Error! The input line name %s is not in the model grid table! Acceptable line names are like "CO10", "CO21", "CO98", "CO109", "CO1110", "CI10')
    
    # load CO line ratio 
    print('Reading model grid line ratio of %s to %s'%(which_lines[0], which_lines[1]))
    data = tb[which_lines[0]].data / tb[which_lines[1]].data
    
    if unit_scale == 'Kelvin':
        tb_freq = {}
        tb_freq['CO10'] = 115.2712018
        tb_freq['CO21'] = 230.5380000
        tb_freq['CO32'] = 345.7959899
        tb_freq['CO43'] = 461.0407682
        tb_freq['CO54'] = 576.2679305
        tb_freq['CO65'] = 691.4730763
        tb_freq['CO76'] = 806.6518060
        tb_freq['CO87'] = 921.7997000
        tb_freq['CO98'] = 1036.9123930
        tb_freq['CO109'] = 1151.9854520
        tb_freq['CO1110'] = 1267.0144860
        tb_freq['CO1211'] = 1381.9951050
        tb_freq['CI10'] = 492.16065
        tb_freq['CI21'] = 809.34197
        data = data / (tb_freq[which_lines[0]]/tb_freq[which_lines[1]])**2
    
    data = np.log10(data)
    
    # free parameters are : z, lg_nH2_mean, lg_nH2_powerlaw_thresh, T_kin
    #grid_z = np.unique(tb['z'])
    #grid_lg_nH2_mean = np.unique(tb['lg_nH2_mean'])
    #grid_lg_nH2_powerlaw_thresh = np.unique(tb['lg_nH2_powerlaw_thresh'])
    #grid_T_kin = np.unique(tb['T_kin'])
    #coords = np.zeros((len(grid_z), len(grid_lg_nH2_mean), len(grid_lg_nH2_powerlaw_thresh), len(grid_T_kin), 4))
    #coords[..., 0] = grid_z.reshape((len(grid_z),1,1,1))
    #coords[..., 1] = grid_lg_nH2_mean.reshape((1,len(grid_lg_nH2_mean),1,1))
    #coords[..., 2] = grid_lg_nH2_powerlaw_thresh.reshape((1,1,len(grid_lg_nH2_powerlaw_thresh),1))
    #coords[..., 3] = grid_T_kin.reshape((1,1,1,len(grid_T_kin)))
    #coords = coords.reshape((data.size, 4))
    coords = np.column_stack((np.log10(1.0+tb['z'].data), tb['lg_nH2_mean'].data, tb['lg_nH2_powerlaw_thresh'].data, tb['T_kin'].data))
    
    interpolator = LinearNDInterpolator(coords, data)
    
    #print(interpolator((4.0, 4.0, 5.0, 50.0)))
    #print(data[np.logical_and.reduce((np.isclose(tb['z'],4.0), np.isclose(tb['lg_nH2_mean'],4.0), np.isclose(tb['lg_nH2_powerlaw_thresh'],5.0), np.isclose(tb['T_kin'],50.0)))])
    #--> checked consistent
    
    return interpolator



