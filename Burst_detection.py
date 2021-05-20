#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 17:33:41 2021

@author: ghislainedeyab
"""



#Extracting the ISIth from the logISIH

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.signal import argrelextrema
from itertools import chain
import math
import xlsxwriter 


data = pd.read_excel("/Users/ghislainedeyab/Desktop/Spike_list_test.xlsx")

well = input("please enter well followed by _")


electrode_list = []
elec_row = 1
elec_col = 0
while len(electrode_list) < 16:
    while elec_col < 4:
        elec_col += 1
        electrode_list.append(well + str(elec_row) + str(elec_col))
    elec_col = 0
    elec_row += 1

data_list = {k:[] for k in electrode_list}
for k in data_list.keys():
    for index, row in data.iterrows():
        if row['Electrode'] == k:
            data_list[k].append(row['Time (s)'])

ISI_dict = {k:[] for k in electrode_list}

#Create a dictonary for each electrode with the electrode as the key and the ISI of all spike times as the values            
for k, lst in data_list.items():
    isi = []
    time = []
    for t in range(0,len(lst)):
        if lst[t] - lst[t-1] >= 0:
            isi.append(lst[t]-lst[t-1])
            time.append(lst[t-1])
    ISI_dict[k].append(isi)   
    ISI_dict[k].append(time)


timepeak_dict = {k:[] for k in electrode_list} #Dictionary containing the times for each peak in each histogram
freqpeak_dict = {k:[] for k in electrode_list} #Dictionary containing the bin frequency for each peak in each histogram 
histdata_dict = {k:[] for k in electrode_list} #Dictionary containng the y value for all bars in the histogram, the x values for all the bins, the values of all peaks after IBP, and the IBP (as four separate lists)

#Create a histogram of ISI values for each electrode on a log scale (10^-1s or 0.1s = 100ms)     
for k, lst in ISI_dict.items():

    if len(lst[0]) > 1:
        (n, bins, patches) = plt.hist(lst[0], bins=np.logspace(np.log10(0.001),np.log10(1),num=50,endpoint=True, base=10,dtype=None),edgecolor='black')
        plt.gca().set_xscale("log")
        plt.title(k)
        plt.xlabel('ISI log scale (sec)')
        plt.ylabel('Frequency')
        plt.ylim(0,400)
        plt.show() 
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


#Identifying peaks below and above the 100ms threshold
prethreshold_dict = {k:[] for k in electrode_list} # a dictionary of the all the peaks below the threshold of 100ms 
for (k,t), (k2,f) in zip(timepeak_dict.items(), freqpeak_dict.items()):
    if k == k2:
        prethreshold_freq = [] #a list of all the frequencies of bins identified as peaks that occur below the threshold of 100ms
        prethreshold_time = [] #a list of all the time of bins identified as peaks that occur below the threshold of 100ms
       
        for (b,n) in zip(t,f):
            if b <= 0.1:
                prethreshold_freq.append(n)
                prethreshold_time.append(b)
        prethreshold_dict[k].append(prethreshold_freq)
        prethreshold_dict[k].append(prethreshold_time)
        prethreshold_freq = []
        prethreshold_time = []
       

#Identifying the max peak and its time below and above 100ms threshold 
IBP_dict = {k:[] for k in electrode_list} # A dictionary representing the frequency, time, and index of the highest peak before 100ms.
for k,v in prethreshold_dict.items():
    if len(v[0]) > 0: 
        max_freq = max(v[0]) #finds the maximum frequency in the list of peaks before 100ms (This is the intraburst peak IBP)
        index = v[0].index(max_freq) #the index of maximum frequency 
        pre_threshold = []
        pre_threshold.append(max_freq)
        pre_threshold.append(v[1][index])
        pre_threshold.append(index)
        IBP_dict[k].append(pre_threshold)
        histdata_dict[k].append([pre_threshold[1]])
        pre_threshold =[]


#Modify histdata_dict so that it only contains the peaks that occur after the IBP
count = 0
for k,v, in histdata_dict.items():
    if len(v) == 4 and len([3]) >0:
        for time in v[2]:
            if time < v[3][0]:
                count = count + 1
        del v[2][0:count]
    count = 0
                
            
#Identifying all the minimum values between the IBP and subsequent peaks after the threshold
minvalue_dict = {k:[] for k in electrode_list} #Dictionary contains all the minimum values between the IBP and subsequent peaks, their index, and the value and index of the subsequent peak being looked at (this information will be used to calculate the void paramater) 
for k,v in histdata_dict.items():
    center_values= [] #list of all values between the IBP and each peak
    center_indeces =[] #list of all indeces of the bins between IBP and each subsequent peak 
    min_value = [] # the smallest bin between IBP and each subsequent peak
    min_index =[] #the index of the smallest bin
    peak_index = []
    peak_value=[]
    if len(v) >= 4:
        if len(v[3]) > 0 and len(v[2]) > 1: #if there is atleast one IBP and atleast one other peak
            index_IBP = v[1].index(v[3][0]) #finds the index of the IBP in the histogram
            for i in v[2]:
               index_peaks = v[1].index(i) #finds the index of each subsequent peak in the histogram
               if index_peaks != index_IBP:
                   peak_index.append(index_peaks)
                  
               for n in range(len(v[0])): #iterates through all bins in the histogram
                    for idx,val in enumerate(v[0]):
                        if n > index_IBP and n < index_peaks: #if the bin is located between the IBP and the subsequent peak
                            if n == idx:
                                center_values.append(val)
                                center_indeces.append(idx)
             
               if len(center_values) > 0: 
                   minimum_value = min(center_values)
                   min_value.append(minimum_value)
                   
                   for value, index in zip(center_values, center_indeces):
                       if value == minimum_value:
                           min_index.append(index)
                           break
              
               center_values =[]
               center_indeces =[]
    minvalue_dict[k].append(min_value)
    minvalue_dict[k].append(min_index)
    for index in peak_index:
            peak_value.append(v[0][index])
        
    minvalue_dict[k].append(peak_value)
    minvalue_dict[k].append(peak_index)
    
        

#Calculate the void parameter between the IBP and each subsequent peak
for k,IBP in IBP_dict.items():
    for k2, v in minvalue_dict.items():
        if len(IBP)>0 and len(v[2]) >0 and k == k2:
            void_list = []
            for value, peak in zip(v[0],v[2]):
                void = 1 - (value/math.sqrt(IBP[0][0]*peak))
                void_list.append(void)
            minvalue_dict[k].append(void_list)
       
            
        

#Find the smallest minimum peak for which the void parameter is greater than 0.7
ISIth_dict = {k:[] for k in electrode_list} #Dictionary containing the index of the ISIth, the time of the core ISIth and, the time of the boundary ISIth
for k,v in minvalue_dict.items():
    accepted_index = []
    if len(v) > 4:
        for void, minimum, index in zip(v[4],v[0],v[1]):
            if void > 0.7:
                accepted_index.append(index)
    if len(accepted_index) > 0:
        ISImin = min(accepted_index)
        ISIth_dict[k].append(ISImin)
  
        

for (k,v), (k2,v2) in zip(ISIth_dict.items(), histdata_dict.items()):
    if len(v) > 0:
        for index in range(len(v2[1])):
            if v[0] == index:
                ISIth_dict[k].append(v2[1][index])
                

for k,v in ISIth_dict.items():
    if len(v) > 0: 
        if v[1] > 0.1:
            ISIth_dict[k].append(0.1)


#Extracting burst information (note at what time each burst starts, the number of spikes ivolved, what time the last spike occurs at)            
minspikes = 5 #this is the threshold for the minimum number of spikes allowed in a burst

output = xlsxwriter.Workbook("/Users/ghislainedeyab/Desktop/Electrode_burst.xlsx")
outsheet = output.add_worksheet(well)
outsheet.write("A1", "Electrode")
outsheet.write("B1", "Number of spikes")
outsheet.write("C1","First spike time (sec)")
outsheet.write("D1","Last spike time (sec)")
outsheet.write("E1","Burst duration")


burst_number = []
burst_start = []
burst_end = []
burst_duration = []
electrode = []
for (k,v), (k2,v2) in zip(data_list.items(),ISIth_dict.items()):
    
    spike = []
    if len(v) > 0:
        if len(v2) > 1:
            for time in range(len(v)):
                if v[time] - v[time-1] > 0 and v[time] - v[time-1] <= v2[1]:
                    if v[time] not in spike:
                        spike.append(v[time])
                    if v[time-1] not in spike:
                        spike.append(v[time-1])
                else:
                    if len(spike) >= minspikes:
                        burst_start.append(spike[0])
                        burst_end.append(spike[-1])
                        burst_number.append(len(spike))
                        burst_duration.append(spike[-1] - spike [0])
                        electrode.append(k)
                        spike = []
                    else:
                        spike = []
        
    for item in range(len(electrode)):
        outsheet.write(item+1,0,electrode[item])
    
    for item in range(len(burst_number)):
        outsheet.write(item+1,1,burst_number[item])
    
    for item in range(len(burst_start)):
        outsheet.write(item+1,2,burst_start[item])
    
    for item in range(len(burst_end)):
        outsheet.write(item+1,3,burst_end[item])
    
    for item in range(len(burst_duration)):
        outsheet.write(item+1,4,burst_duration[item])
    
    

output.close()            
                    
           
              
            
        


#print(data_list)
#print(ISI_dict)
#print(ISIth_dict)
#print(minvalue_dict)
#print(histdata_dict)
#print(IBP_dict)
#print(postthreshold_dict)   



    
   
    
        


        
        
        
        




