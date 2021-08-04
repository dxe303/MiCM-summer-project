#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 08:29:27 2021

@author: xueerding
"""

import sys
import os
import numpy as np
import pandas as pd

import math
from scipy import signal
import matplotlib.pyplot as plt

powspec = {}  # initialize dict of power spectrums
bin_size = 0.0005  # default bin size
input_folder = sys.argv[1]  # first command line argument should be input directory

# check if custom bin size set
if len(sys.argv) == 2:
    try:
        if float(sys.argv[2]) > 0:
            bin_size = float(sys.argv[2])
        else:
            print('bin size must be positive')
    except:
        print('bin size not valid')

'''
test = ['/Users/xueerding/Desktop/MiCM/data/Extracted_files/Feb132020_ND3439SNCA_BTest4_1h/Feb132020_ND3439SNCA_BTest4_1h_well_list/C2_spikes.csv',
        '/Users/xueerding/Desktop/MiCM/data/Extracted_files/Feb132020_ND3439SNCA_BTest4_1h/Feb132020_ND3439SNCA_BTest4_1h_well_list/C5_spikes.csv',
        '/Users/xueerding/Desktop/MiCM/data/Extracted_files/Feb132020_ND3439SNCA_BTest2_1h/Feb132020_ND3439SNCA_BTest2_1h_well_list/D5_spikes.csv',
        '/Users/xueerding/Desktop/MiCM/data/Extracted_files/Feb132020_ND3439SNCA_BTest2_1h/Feb132020_ND3439SNCA_BTest2_1h_well_list/C4_spikes.csv',
        '/Users/xueerding/Desktop/MiCM/data/Extracted_files/Feb132020_ND3439SNCA_BTest2_1h/Feb132020_ND3439SNCA_BTest2_1h_well_list/C2_spikes.csv',
        '/Users/xueerding/Desktop/MiCM/data/Extracted_files/Feb132020_ND3439SNCA_BTest2_1h/Feb132020_ND3439SNCA_BTest2_1h_well_list/C1_spikes.csv',
        '/Users/xueerding/Desktop/MiCM/data/Extracted_files/Feb132020_ND3439SNCA_BTest2_1h/Feb132020_ND3439SNCA_BTest2_1h_well_list/B4_spikes.csv',
        '/Users/xueerding/Desktop/MiCM/data/Extracted_files/Feb132020_ND3439SNCA_BTest2_1h/Feb132020_ND3439SNCA_BTest2_1h_well_list/A3_spikes.csv',
        ]
for inputFile in test:
'''
# find spike files in input folder
files = [f for f in os.listdir(input_folder) if f.endswith('_spikes.csv')]
# calculate power spectrum for every spike file
for inputFile in files:

    df = pd.read_csv(inputFile, header=None, names=["Electrode", "Time (s)"])
    
    spike_list = df['Time (s)'].to_numpy()
    
    
    # set bin size (s)
    bins = np.arange(0, math.ceil(df["Time (s)"].max()), bin_size)
    timeSeries = pd.Series(data=np.zeros(bins.size, dtype='int'))
    
    # get spike count per time bin
    bin_num = 0
    for spike in spike_list:
        while spike > bins[bin_num]:
            bin_num += 1
            if bin_num == bins.size:
                bin_num -= 1
                break
        timeSeries.at[bin_num] += 1
        
    # calculate power spectral density using Welch's method
    freq, psd = signal.welch(timeSeries, fs=1/bin_size, scaling='density')
    powspec[inputFile[-13:-11]] = psd
    plt.plot(freq, psd, '--')

# average the power spectral densities
powspec_df = pd.DataFrame(data=powspec)
powspec_df['mean'] = powspec_df.mean(axis=1)
print(powspec_df)

# plot average power spectral density
plt.plot(freq, powspec_df['mean'], linewidth=2.5)
plt.title('Average power spectral density')
plt.xlabel('frequency [Hz]')
plt.ylabel('PS [V**2/Hz]')
plt.legend(powspec.keys())
plt.show()


