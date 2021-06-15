#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 00:46:01 2021

@author: xueerding
"""
import sys
import pandas as pd
import itertools
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema
from itertools import chain
import statistics as st

inputFile = sys.argv[1]  # first field should be input file path
data = pd.read_csv(inputFile, names=["Electrode", "Time(s)", "Amplitude(mV)"])

print(data)

well = inputFile[len(inputFile) - 7 : len(inputFile) - 4]
exceptions = ["B6_11"]  # FIX THIS LATER

# create list of electrodes for current well
electrodes = []
elec_row = 1
elec_col = 1

while elec_row <= 4:
    while elec_col <= 4:  # so electrode columns are 0-3?
        electrodes.append(well + str(elec_row) + str(elec_col))
        elec_col +=1
    elec_col = 1 
    elec_row += 1 


# create dictionnary of electrodes mapped to time
electrode_dict = {k:[] for k in electrodes}

for index, row in data.iterrows():
    if row["Electrode"] not in exceptions:  # MAKE EXCEPTION LIST
        electrode_dict[row["Electrode"]].append(row["Time(s)"])
        

# create dictionnary of electrodes mapped to ISI
ISI_dict = {k:[] for k in electrodes}

for k, lst in electrode_dict.items():
        isi = []
        time = []
        for t in range(0,len(lst)):
            if lst[t] - lst[t-1] >= 0:
                isi.append(lst[t]-lst[t-1])
                time.append(lst[t-1])
        ISI_dict[k].append(isi)   
        ISI_dict[k].append(time)
        
        
        
timepeak_dict = {k:[] for k in electrode_dict} #Dictionary containing the times for each peak in each histogram
freqpeak_dict = {k:[] for k in electrode_dict} #Dictionary containing the bin frequency for each peak in each histogram 
histdata_dict = {k:[] for k in electrode_dict} #Dictionary containng the y value for all bars in the histogram, the x values for all the bins, the values of all peaks after IBP, and the IBP (as four separate lists)

#Create a histogram of ISI values for each electrode on a log scale (10^-1s or 0.1s = 100ms)     
for k, lst in ISI_dict.items():

    if len(lst[0]) > 1:
        (n, bins, patches) = plt.hist(lst[0], bins=np.logspace(np.log10(0.001),np.log10(1),num=50,endpoint=True, base=10,dtype=None),edgecolor='black')
        plt.gca().set_xscale("log")
        plt.title(k)
        plt.xlabel('ISI log scale (sec)')
        plt.ylabel('Frequency')
        plt.ylim(0,400)
        #plt.savefig(inputFile[:len(inputFile) - 8] + well + "_" + k + "_histogram")
        histdata_dict[k].append(np.array(n).tolist())
        histdata_dict[k].append(np.array(bins).tolist())
        
        #Extract local maxima for each histogram
        x_valuelist =[]
        maxima_array = argrelextrema(n, np.greater) #gives indices of local maxima in a numpy array
        maxima_lists= np.array(maxima_array).tolist() 
        maxima_list = list(map(int, chain.from_iterable(maxima_lists))) #turns the numpy array of indices into a flattened list
        for i in maxima_list:
            x_value = bins[i]
            y_value = n[i]
            x_valuelist.append(x_value)
            freqpeak_dict[k].append(y_value)
            timepeak_dict[k].append(x_value)
        histdata_dict[k].append(x_valuelist)


    


