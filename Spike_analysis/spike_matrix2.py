#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 23:11:50 2021

@author: xueerding
"""

import sys
import numpy as np
import pandas as pd
import seaborn

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import random as r 


inputFile = sys.argv[1]  # first field should be input file path

df = pd.read_csv(inputFile, usecols=["Electrode", "Time (s)"])

'''
df = pd.read_csv('/Users/xueerding/Desktop/MiCM/data/Extracted files/Feb132020_ND3439SNCA_WTest1_1h/Feb132020_ND3439SNCA_WTest1_1h(000)(000)_spike_list.csv', 
                 usecols=["Electrode", "Time (s)"])
'''

df.dropna(inplace=True)

temp= df.groupby(["Electrode"]).agg(list)
#print(temp)
data = temp.filter(regex="._.", axis=0)

dict = data.to_dict(orient='index')

data2 = pd.DataFrame( {key:pd.Series(value['Time (s)']) for key, value in dict.items()} )
data_list = data2.astype('float64')
print(data_list)

#raster = seaborn.heatmap(data2)

#Plot raster graph
figure(num=None, figsize=(100, 40),dpi=80,facecolor='w',edgecolor='k')
plt.xlim(0,600)
    
for key, val in data_list.items():
    if len(val) > 0:
        plt.scatter(data_list[key],[key]*len(val), marker="|", color = 'k', label=key)
        
    if len(val) == 0:
        rand = r.randint(70,90)
        plt.scatter(rand,key,marker="|",color='w')
  
plt.title(inputFile)
plt.xlabel('Time (sec)')
plt.ylabel('Electrode')
plt.savefig(inputFile[:-4])