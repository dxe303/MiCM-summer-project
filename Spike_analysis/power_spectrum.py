#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 14:53:25 2021

@author: xueerding
"""

import sys
import numpy as np
import pandas as pd

import math
from scipy import signal
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = (20, 12)


inputFile = sys.argv[1]  # first field should be input file path
#inputFile = '/Users/xueerding/Desktop/MiCM/data/Extracted_files/Feb132020_ND3439SNCA_WTest3_2h/Feb132020_ND3439SNCA_WTest3_2h_well_list/C1_spikes.csv'

df = pd.read_csv(inputFile, header=None, names=["Electrode", "Time (s)"], 
                 dtype={"Electrode":'str', "Time (s)":'float'})

spike_list = df['Time (s)'].to_numpy()

# set bin size (s)
bin_size = 0.0005

# get spike count per time bin
bins = np.arange(0, math.ceil(df["Time (s)"].max()), bin_size)
timeSeries = pd.Series(data=np.zeros(bins.size, dtype='int'))

bin_num = 0
for spike in spike_list:
    while spike > bins[bin_num]:
        bin_num += 1
        if bin_num == bins.size:
            bin_num -= 1
            break
    timeSeries.at[bin_num] += 1 


# plot power spectral density using Welch's method
freq, psd = signal.welch(timeSeries, fs=1/bin_size, scaling='density')

plt.plot(freq, psd)
plt.title(inputFile[24:]+' power spectral density by well\n')
plt.xlabel('frequency [Hz]')
plt.ylabel('PS [V**2/Hz]')
plt.show()
#plt.savefig(inputFile[:-4] + '_pow_spec_freq_' + 1/bin_size)