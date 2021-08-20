#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 11:25:30 2020

@author: ghislainedeyab

This algorithm is adapted from Pasquale et.al 2010, it bins IBeI's across all electrodes into a log10 histogram produces two peaks
the first peak representing the IBeI of electrode bursts within a network burst, and the second peak represents the IBeI of electrode bursts between network bursts.
The IBeIth calculated from teh histogram is used as the maximum time interval allowed between bursts within a network burst. 
The minimum percentage of electrodes allowed in a network burst is set at 20% of all active electrodes.
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.signal import argrelextrema
from itertools import chain
import math
import xlsxwriter 
import statistics as st


well = input("please enter well followed by _")
data = pd.read_excel("/Users/ghislainedeyab/Desktop/Electrode_burst.xlsx",sheet_name=well)
sorted_data = data.sort_values('First spike time (sec)') #Sorts data from smallest electrode burst start time to largest 
final = sorted_data.reset_index(drop = True) #Reset index in sorted data
 
electrode_list = [] #A list of all electrodes that had electrode bursts detected 
for index, row in data.iterrows():
    if row['Electrode'] not in electrode_list:
        electrode_list.append(row['Electrode'])




data_list = {well:[]} #A dictionary containing the start time for each electrode burst, the end time of each electrode burst, and the number of spikes in each electrode burst as three separate lists
First_spike = []
Last_spike = []
number_spikes = []
for index, row in final.iterrows():
    First_spike.append(row['First spike time (sec)'])
    Last_spike.append(row['Last spike time (sec)'])
    number_spikes.append(row['Number of spikes'])
data_list[well].append(First_spike)
data_list[well].append(Last_spike)
data_list[well].append(number_spikes)


#Make IBeIH on log scale
IBeI_list = [] #A list containing all the Inter burst intervals across all electrodes
for k,v in data_list.items():
    for indx in range(len(v[0])):
        IBeI = v[0][indx] - v[0][indx-1] 
        if IBeI > 0:
            IBeI_list.append(IBeI)

histdata_dict = {well:[]} #Dictionary containng the y value for all bars in the histogram, the x values for all the bins, the value of all peaks after IBP, and the time of all peaks after IBP (as four separate lists)       

(n, bins, patches) = plt.hist(IBeI_list, bins=np.logspace(np.log10(0.001),np.log10(10),num=50,endpoint=True, base=10,dtype=None),edgecolor='black')
plt.gca().set_xscale("log")
plt.title(well)
plt.xlabel('IBeI log scale (sec)')
plt.ylabel('Frequency')
plt.show() 
histdata_dict[well].append(np.array(n).tolist())
histdata_dict[well].append(np.array(bins).tolist())


#Extract x and y values of local maxima     
x_valuelist =[] #List of the x values of all the peaks found in the histogram
y_valuelist = [] #List of the y values of all the peaks found in the histogram
maxima_array = argrelextrema(n, np.greater) #gives indices of local maxima in a numpy array
maxima_lists= np.array(maxima_array).tolist() 
maxima_list = list(map(int, chain.from_iterable(maxima_lists))) #turns the numpy array of indices into a flattened list
for i in maxima_list:
    x_value = bins[i]
    y_value = n[i]
    x_valuelist.append(x_value)
    y_valuelist.append(y_value)

    
#Identify the highest peak before 0.1 sec threshold and all peaks after it 
pre_x = [] #the times of all the maxima before the 0.1 sec thresh
pre_y = [] #the frequencies of all the maxima before the 0.1 sec thresh
post_x = [] #all the maxima times after the 0.1 sec thresh
post_y = [] #all the maxima frequencies after the 0.1 sec thresh
for x,y in zip(range(len(x_valuelist)),range(len(y_valuelist))):
    if x_valuelist[x] <= 0.1:
        pre_x.append(x_valuelist[x])
        pre_y.append(y_valuelist[y])
    if x_valuelist[x] > 0.1:
        post_x.append(x_valuelist[x])
        post_y.append(y_valuelist[y])
        
if len(pre_y) > 0 and len(post_y) > 0: #IF there are peaks present both before and after the threshold continue using the adaptive method
    minvalue_dict = {well:[]} #Dictionary contains all the minimum values between the IBP and subsequent peaks, their index, and the value of the subsequent peak being looked at (this information will be used to calculate the void paramater) 

    index_max = pre_y.index(max(pre_y))#The index of the highest peak
    peak_time = pre_x[index_max] #the time of the highest peak before the thresh
    peak_freq = pre_y[index_max] #the frequency of the highest peak before the thresh    
    histdata_dict[well].append(post_y)
    histdata_dict[well].append(post_x)
    
#Identifying all the minimum values between the IBP and subsequent peaks after the threshold
    minvalues = [] #a list of all minima found between the IBP and subsequent peaks
    minindex = [] #the index of the all the minima 
    sub_peak = [] #the vale of the subsequent peaks
    for k,v in histdata_dict.items():
        center_freq = [] #The y values of all the bars located between the IBP and subsequent peak being looked at
        center_times =[] #The x value of all the bars locacted between the IBP and subsequent peak being looked at 
        for peakt, peakf in zip(v[3],v[2]): #For the time and frequency of all subsequent peaks
            for freq,time in zip(v[0],v[1]): #For the frequency and time of all bins in the histograms
                if time > peak_time and time < peakt: #if the time of a bin is after the IBP and before the subsequent peak, add it to the centervalues
                    center_freq.append(freq)
                    center_times.append(time)          
            mincenter = center_freq.index(min(center_freq))
            minvalues.append(center_freq[mincenter])
            minindex.append(center_times[mincenter])
            sub_peak.append(peakf)
            center_freq = []
            center_times = []

    minvalue_dict[well].append(minvalues) 
    minvalue_dict[well].append(minindex)
    minvalue_dict[well].append(sub_peak)

  
#Calculate the void parameter between the IBP and each subsequent peak
    for k,v in minvalue_dict.items():
        void_list = []
        for minimum, peak in zip(v[0],v[2]):
            void= 1 - (minimum/math.sqrt(peak_freq*peak))
            void_list.append(void)
        minvalue_dict[well].append(void_list)
    
#Find the smallest minimum peak for which the void parameter is greater than 0.7        
    
    accepted_time = [] #A list of minima that have a void parameter above 0.7
    for k,v in minvalue_dict.items():
        for void, minimum, time in zip(v[3],v[0],v[1]):
            if void > 0.7:
                accepted_time.append(time)
        if len(accepted_time) > 0:
            IBeIth = min(accepted_time)
        elif len(accepted_time) == 0: #If there is no void parameter above 0.7 then use the fixed threshold method (fixed threshold of 100ms)
            IBeIth = 0.1
            
if len(pre_y) == 0 or len(post_y) == 0: #If there is not altleast one peak before 100ms and one peak after 100ms then use the fixed threshold method (fixed threshold of 100ms)
    IBeIth = 0.1
                                      
print(IBeIth)  
#Extracting burst information (note at what time each burst starts, the number of spikes ivolved, what time the last spike occurs at)            
minpercent = 0.1875 #this is the threshold for the minimum number of spikes allowed in a burst
num_bursting = 16 #the number of bursting electrodes 

#extract raw electrode burst data into lists
electrode_list = final['Electrode'].tolist()
spike_list = final['Number of spikes'].tolist()
first_list = final['First spike time (sec)'].tolist()
last_list = final['Last spike time (sec)'].tolist()
dur_list = final['Burst duration'].tolist()

#create columns for excel file
output = xlsxwriter.Workbook("Network_burst.xlsx")
outsheet = output.add_worksheet(well)
outsheet.write("A1", "Number of electrode bursts")
outsheet.write("B1", "Number of electrodes")
outsheet.write("C1", "Beginning of network burst")
outsheet.write("D1","End of network burst")
outsheet.write("E1","Network burst duration")
outsheet.write("F1","Average electrode burst duration")
outsheet.write("G1", "Number of spikes")

#Set up lists that will hold new network burst data, each list will be written into the respective excel columns created above
burst_number = []
num_electrode =[]
burst_start = []
burst_end = []
netburst_dur = []
elecburst_dur = []
spike_number = []

#lists that will be used to extract data out of the raw electrode burst data and into the above lists 
network_start = []
network_end = []
electrode = []
spike_num = []
duration =[]

#extract parameters from raw electrode burst data
for start, elec, end, spike, dur in zip(range(len(first_list)),range(len(electrode_list)),range(len(last_list)), range(len(spike_list)), range(len(dur_list))): 
    if first_list[start] - first_list[start-1] < IBeIth:#If the time between the start of two electrode bursts is below the IBeIth then count it as being part of an electrode burst
        if first_list[start] - first_list[start-1] > 0:
            if first_list[start-1] not in network_start: #extracts start times of all electrode bursts in a NB
                network_start.append(first_list[start-1])
            network_start.append(first_list[start])
            if last_list[end-1] not in network_end: #extracts end times of all EB in a NB
                network_end.append(last_list[end-1])
            network_end.append(last_list[end])
            if spike_list[spike-1] not in spike_num: #extracts number of spikes in each EB present in a NB
                spike_num.append(spike_list[spike-1])
            spike_num.append(spike_list[spike])
            if dur_list[dur-1] not in duration: #extracts the burst duration of each EB in a NB
                duration.append(dur_list[dur-1])
            duration.append(dur_list[dur])
            if electrode_list[elec-1] not in electrode: #keeps track fo which electrode is bursting
                electrode.append(electrode_list[elec-1])
            electrode.append(electrode_list[elec])
            
    else: 
        elec_number = set(electrode) #if the number of electrodes present is larger than 20% of all bursting electrodes than we can classify the cluster of electrode bursts as a NB
        if len(network_start)>0 and len(elec_number) >= (minpercent*num_bursting) and sum(spike_num) >= 50:
            burst_number.append(len(network_start))
            burst_start.append(min(network_start))
            burst_end.append(max(network_end))
            elecburst_dur.append(st.mean(duration))
            netburst_dur.append(max(network_end) - min(network_start))
            spike_number.append(sum(spike_num))
            num_electrode.append(len(elec_number))
            
            network_start = []
            network_end = []
            electrode = []
            spike_num = []
            duration =[]
            
        else:
            network_start = []
            network_end = []
            electrode = []
            spike_num = []
            duration =[]

#Write all network burst information into a new excel file 
for item in range(len(burst_number)):
        outsheet.write(item+1,0,burst_number[item])        
     
for item in range(len(num_electrode)):
        outsheet.write(item+1,1,num_electrode[item])  

for item in range(len(burst_start)):
        outsheet.write(item+1,2,burst_start[item]) 

for item in range(len(burst_end)):
        outsheet.write(item+1,3,burst_end[item]) 

for item in range(len(netburst_dur)):
        outsheet.write(item+1,4,netburst_dur[item]) 

for item in range(len(elecburst_dur)):
        outsheet.write(item+1,5,elecburst_dur[item]) 

for item in range(len(spike_number)):
        outsheet.write(item+1,6,spike_number[item])  



output.close()            


                