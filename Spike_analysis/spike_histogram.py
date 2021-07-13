#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 12:05:33 2021

@author: xueerding
"""

import sys
import numpy as np
import pandas as pd


'''
inputFile = sys.argv[1]  # first field should be input file path

df = pd.read_csv(inputFile, header=None, names=["Electrode", "Time (s)"])

'''
inputFile = '/Users/xueerding/Desktop/MiCM/data/Extracted_files/Feb132020_ND3439SNCA_WTest3_2h/Feb132020_ND3439SNCA_WTest3_2h_well_list/B2_spikes.csv'
df = pd.read_csv(inputFile, header=None, names=["Electrode", "Time (s)"])


df.dropna(inplace=True)

temp= df.groupby(["Electrode"]).agg(list)

data = temp.filter(regex="._.", axis=0)

dict = data.to_dict(orient='index')



data2 = pd.DataFrame( {key:pd.Series(value['Time (s)']) for key, value in dict.items()} )
data_list = data2.astype('float64')
print(data_list)

ISIs = data2.diff()
print(ISIs)



#hist = ISIs.hist(bins=100, range=(0, max(ISIs.max())), density=True)   
#hist = ISIs.plot.hist(bins=1000, subplots=True, sharex=True, sharey=True, 
#                      xlabel='ISI', layout=(4,4), table=True)


logISIs = np.log10(ISIs)    

hist2 = logISIs.plot.hist(bins=100, title=inputFile[24:]+' histogram of logISIs by well',
                          xticks=np.arange(min(logISIs.min()), max(logISIs.max()), (max(logISIs.max())-min(logISIs.min()))/20) )

hist2.set_xlabel('logISI')
hist2.set_ylabel('Frequency per bin')
#hist2.title('Histogram of logISIs')
hist2.figsize = (12, 6)


#hist3 = logISIs.hist(bins=100, range=(0, max(logISIs.max())), density=True)  
hist4 = logISIs.plot.hist(bins=200, subplots=True, sharex=True, sharey=True,
                       xlabel='logISI', layout=(4,4),
                       title=inputFile[24:]+' histogram of logISIs by electrode')



