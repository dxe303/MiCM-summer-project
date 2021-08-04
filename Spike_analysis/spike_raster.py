#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 23:11:50 2021

@author: xueerding
"""

import sys
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import random as r 


inputFile = sys.argv[1]  # first field should be input file path

df = pd.read_csv(inputFile, header=None, names=["Electrode", "Time (s)"])

'''
inputFile = '/Users/xueerding/Desktop/MiCM/data/Extracted_files/Feb132020_ND3439SNCA_WTest3_2h/Feb132020_ND3439SNCA_WTest3_2h_well_list/C1_spikes.csv'
df = pd.read_csv(inputFile, header=None, names=["Electrode", "Time (s)"])
'''

df.dropna(inplace=True)

temp= df.groupby(["Electrode"]).agg(list)

data = temp.filter(regex="._.", axis=0)

data_dict = data.to_dict(orient='index')

data2 = pd.DataFrame( {key:pd.Series(value['Time (s)']) for key, value in data_dict.items()} )
data_list = data2.astype('float64')


#Plot figure
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(20, 6))
#fig.dpi=80
fig.facecolor='w'
fig.edgecolor='k'

# plot spike histogram with 1 sec bins
bin_size = 1
bins = np.arange(0, math.ceil(df["Time (s)"].max()), bin_size)
data = pd.Series(data=np.zeros(bins.size, dtype='int'))
spike_list = df['Time (s)'].to_numpy()

bin_num = 0
for spike in spike_list:
    while spike > bins[bin_num]:
        bin_num += 1
        if bin_num == bins.size:
            bin_num -= 1
            break
    data.at[bin_num] += 1

timeSeries = data
ax1.plot(bins, timeSeries)


# plot raster plot
for key, val in data_list.items():
    if len(val) > 0:
        ax2.scatter(data_list[key],[key]*len(val), marker="|", color = 'k', label=key)
        
    if len(val) == 0:
        rand = r.randint(70,90)
        ax2.scatter(rand,key,marker="|",color='w')
  
plt.suptitle(inputFile)
plt.xlabel('Time (sec)')
plt.xlim(0,600)
#ax1.set_ylim(0, 6000)
ax1.set_yscale('log', base=10, subs=[2,3,4,5,6,7,8,9])
ax1.set_ylabel('Number of spikes/1 sec interval')
ax2.set_ylabel('Electrode')
plt.savefig(inputFile[:-4])
#plt.show()
