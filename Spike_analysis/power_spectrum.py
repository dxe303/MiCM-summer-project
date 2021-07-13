#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 10:51:36 2021

@author: xueerding
"""

import sys
import numpy as np
import pandas as pd

from scipy import signal
import matplotlib.pyplot as plt

'''
inputFile = sys.argv[1]  # first field should be input file path

df = pd.read_csv(inputFile, header=None, names=["Electrode", "Time (s)"])

'''
#inputFile = '/Users/xueerding/Desktop/MiCM/data/Extracted_files/Feb132020_ND3439SNCA_WTest3_1h/Feb132020_ND3439SNCA_WTest3_1h(000)(000)_spike_counts.csv'
#inputFile ='/Users/xueerding/Desktop/MiCM/data/Extracted_files/Feb132020_ND3439SNCA_BTest4_2h/Feb132020_ND3439SNCA_BTest4_2h(000)(000)_spike_counts.csv'
inputFile ='/Users/xueerding/Desktop/MiCM/data/Extracted_files/Feb132020_ND3439SNCA_WTest1_2h/Feb132020_ND3439SNCA_WTest1_2h(000)(000)_spike_counts.csv'
#inputFile ='/Users/xueerding/Desktop/MiCM/data/Extracted_files/Feb132020_ND3439SNCA_WTest3_2h_TTX/Feb132020_ND3439SNCA_WTest3_2h_TTX(000)(000)_spike_counts.csv'
df = pd.read_csv(inputFile, 
                 index_col='Interval Start (S)',
                 usecols=['Interval Start (S)',
                        'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 
                        'B1', 'B2', 'B3', 'B4', 'B5', 'B6',
                        'C1', 'C2', 'C3', 'C4', 'C5', 'C6',
                        'D1', 'D2', 'D3', 'D4', 'D5', 'D6',],
                 )


timeSeries = df.drop(df.tail(12).index).astype('int')
#timeSeries=df.filter(like='.', axis=0).astype('int')


axes = timeSeries.columns
fig, axes = plt.subplots(4, 6, sharex=True, sharey=True, 
                         subplot_kw=dict(xlabel='frequency [Hz]', ylabel='PSD [V**2]'),
                         gridspec_kw=dict(wspace=0.2, hspace=0.4))

fig.suptitle(inputFile[24:]+' power spectrum by well', size=12)

row = 0
col = 0
for column in timeSeries:
    freq, psd = signal.welch(timeSeries[column], scaling='spectrum')
    axes[row//6][col%6].plot(freq, psd)
    axes[row//6][col%6].set_title(column)
    row += 1
    col +=1
    

    #dict = {'frequency [Hz]':freq, 'PSD [V**2]':psd}
    #pow_spec = pd.Dataframe(dict)
    #outputFile = inputFile[:-16] + column + '_power_spectrum.csv'
    #pow_spec.to_csv(outputFile)

