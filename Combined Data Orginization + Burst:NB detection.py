#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  1 21:30:56 2021

@author: ghislainedeyab
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 14:27:05 2021

@author: ghislainedeyab

Program to sort out spikes in excel sheet so that each sheet is one well with all spikes of all active electordes
This program takes approximately 6 minutes to run on an excel sheet with 530,000 rows. 
"""
import pandas as pd
import itertools
import xlsxwriter 
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema
from itertools import chain
import statistics as st

#sheetname = "Sheet2" #PUT SHEETNAME HERE

data = pd.read_excel("/Users/ghislainedeyab/Desktop/Book1.xlsx") #PUT FILE NAME

#data = data.dropna()


exception = input('please enter electrode numbers you dont want to analyze separated by commas: ')
exception_list = exception.split(',')


well_list = ["A1_","A2_","A3_","A4_","A5_","A6_","B1_","B2_","B3_","B4_","B5_","B6_","C1_","C2_","C3_","C4_","C5_","C6_","D1_","D2_","D3_","D4_","D5_","D6_"]

electrodes = []
total_list= []
elec_row = 1
elec_col = 0


electrode_list = []
for wells in well_list:
    while len(electrodes) < 16:
        while elec_col < 4:
            elec_col += 1
            electrodes.append(wells + str(elec_row) + str(elec_col))
        elec_col = 0 
        elec_row += 1     

    electrode_list.append(electrodes)
    electrodes = []
    elec_row = 1
    
new_electrode_list = list(itertools.chain.from_iterable(electrode_list))

electrode_dict = {k:[] for k in new_electrode_list}
inactive_electrode_dict = {}
active_dict = {}
inactive_dict = {}


output = xlsxwriter.Workbook("/Users/ghislainedeyab/Desktop/AST23_3weeks.xlsx")

for electrode in new_electrode_list:
    for row in data.itertuples():
        if electrode not in exception_list:
            if electrode == row.Electrode:
                electrode_dict[electrode].append(row._3)
        


            
for k, lst in electrode_dict.items():
    if len(lst) > 0:
        mfr = len(lst)/600
        if mfr >= 0.0833:
            active_dict[k] = mfr
        if mfr < 0.0833:
            inactive_dict[k] = mfr

               
for wells in well_list:
    ind = 1
    active_ind = 1
    inactive_ind = 1
    exc_index = 1
    worksheet = output.add_worksheet(wells)
    worksheet.write("A1","Electrode")
    worksheet.write("B1","Time (s)")
    worksheet.write("C1","Amplitude(mV)")
    worksheet.write("E1","Active electrodes")
    worksheet.write("F1","MFR(Hz)")
    worksheet.write("G1","Spike count")
    worksheet.write("I1","Inactive Electrodes")
    worksheet.write("J1","MFR(Hz)")
    worksheet.write("K1","Spike count")
    worksheet.write("M1","Excluded electrodes")
    
    for row in data.itertuples():
        if row.Electrode[:3] == wells and row.Electrode not in exception_list:
            worksheet.write(ind,0,row.Electrode)
            worksheet.write(ind,1, row._3)
            worksheet.write(ind,2,row._5)
            ind += 1
    for k, val in active_dict.items():
        if k[:3] == wells:
            worksheet.write(active_ind,4,k)
            worksheet.write(active_ind,5,val)
            worksheet.write(active_ind,6,val*600)
            active_ind += 1 
    for k, val in inactive_dict.items():
        if k[:3] == wells:
            worksheet.write(inactive_ind,8,k)
            worksheet.write(inactive_ind,9, val)
            worksheet.write(inactive_ind,10,val*600)
            inactive_ind += 1
    if len(exception_list) > 0:
        for ex in exception_list:
            worksheet.write(exc_index,12,ex)
            exc_index += 1
    inactive_ind = 1
    active_ind = 1
    ind = 1
    exc_index = 1

    electrode_list = []
    elec_row = 1
    elec_col = 0
    while len(electrode_list) < 16:
        while elec_col < 4:
            elec_col += 1
            electrode_list.append(wells + str(elec_row) + str(elec_col))
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
            #plt.show() 
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
    
    
    worksheet.write("O1", "Burst Electrode")
    worksheet.write("P1", "Number of spikes")
    worksheet.write("Q1","First spike time (sec)")
    worksheet.write("R1","Last spike time (sec)")
    worksheet.write("S1","Burst duration")
    
    
    burst_number = []
    burst_start = []
    burst_end = []
    burst_duration = []
    burst_electrode = []
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
                            burst_electrode.append(k)
                            spike = []
                        else:
                            spike = []
            
        for item in range(len(burst_electrode)):
            worksheet.write(item+1,14,burst_electrode[item])
        
        for item in range(len(burst_number)):
            worksheet.write(item+1,15,burst_number[item])
        
        for item in range(len(burst_start)):
            worksheet.write(item+1,16,burst_start[item])
        
        for item in range(len(burst_end)):
            worksheet.write(item+1,17,burst_end[item])
        
        for item in range(len(burst_duration)):
            worksheet.write(item+1,18,burst_duration[item])
            
    burstelectrode_list = [] #A list of all electrodes that had electrode bursts detected 
    for elec in burst_electrode:
        if elec not in burstelectrode_list:
            burstelectrode_list.append(elec)
    
    #lists containing data for bursting electroded need to be sorted from the first detected burst to the last
    if len(burst_start) > 0:
        lists_to_sort = zip(burst_start,burst_end,burst_number,burst_electrode,burst_duration) 
        sorted_lists = sorted(lists_to_sort)
        separate_lists = zip(*sorted_lists)
        burst_start,burst_end,burst_number,burst_electrode,burst_duration = [list(tuple) for tuple in separate_lists]
        
    
    data_list = {wells:[]} #A dictionary containing the start time for each electrode burst, the end time of each electrode burst, and the number of spikes in each electrode burst as three separate lists
    data_list[wells].append(burst_start)
    data_list[wells].append(burst_end)
    data_list[wells].append(burst_number)
    
   
    #Make IBeIH on log scale
    IBeI_list = [] #A list containing all the Inter burst intervals across all electrodes
    for k,v in data_list.items():
        for indx in range(len(v[0])):
            IBeI = v[0][indx] - v[0][indx-1] 
            if IBeI > 0:
                IBeI_list.append(IBeI)
    #print(IBeI_list)
    histdata_dict = {wells:[]} #Dictionary containng the y value for all bars in the histogram, the x values for all the bins, the value of all peaks after IBP, and the time of all peaks after IBP (as four separate lists)       
    
    (n, bins, patches) = plt.hist(IBeI_list, bins=np.logspace(np.log10(0.001),np.log10(10),num=50,endpoint=True, base=10,dtype=None),edgecolor='black')
    plt.gca().set_xscale("log")
    plt.title(wells)
    plt.xlabel('IBeI log scale (sec)')
    plt.ylabel('Frequency')
    plt.show() 
    histdata_dict[wells].append(np.array(n).tolist())
    histdata_dict[wells].append(np.array(bins).tolist())
    #print(histdata_dict)
    
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
        minvalue_dict = {wells:[]} #Dictionary contains all the minimum values between the IBP and subsequent peaks, their index, and the value of the subsequent peak being looked at (this information will be used to calculate the void paramater) 
    
        index_max = pre_y.index(max(pre_y))#The index of the highest peak
        peak_time = pre_x[index_max] #the time of the highest peak before the thresh
        peak_freq = pre_y[index_max] #the frequency of the highest peak before the thresh    
        histdata_dict[wells].append(post_y)
        histdata_dict[wells].append(post_x)
        
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
    
        minvalue_dict[wells].append(minvalues) 
        minvalue_dict[wells].append(minindex)
        minvalue_dict[wells].append(sub_peak)
    
      
    #Calculate the void parameter between the IBP and each subsequent peak
        for k,v in minvalue_dict.items():
            void_list = []
            for minimum, peak in zip(v[0],v[2]):
                void= 1 - (minimum/math.sqrt(peak_freq*peak))
                void_list.append(void)
            minvalue_dict[wells].append(void_list)
        
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
    
    
    #create columns for excel file
    worksheet.write("U1", "Number of electrode bursts")
    worksheet.write("V1", "Number of electrodes")
    worksheet.write("W1", "Beginning of network burst")
    worksheet.write("X1","End of network burst")
    worksheet.write("Y1","Network burst duration")
    worksheet.write("Z1","Average electrode burst duration")
    worksheet.write("AA1", "Number of spikes")
    
    #Set up lists that will hold new network burst data, each list will be written into the respective excel columns created above
    netburst_number = []
    num_electrode =[]
    netburst_start = []
    netburst_end = []
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
    for start, elec, end, spike, dur in zip(range(len(burst_start)),range(len(burst_electrode)),range(len(burst_end)), range(len(burst_number)), range(len(burst_duration))): 
        if burst_start[start] - burst_start[start-1] < IBeIth:#If the time between the start of two electrode bursts is below the IBeIth then count it as being part of a network burst
            if burst_start[start] - burst_start[start-1] > 0:
                if burst_start[start-1] not in network_start: #extracts start times of all electrode bursts in a NB
                    network_start.append(burst_start[start-1])
                network_start.append(burst_start[start])
                if burst_end[end-1] not in network_end: #extracts end times of all EB in a NB
                    network_end.append(burst_end[end-1])
                network_end.append(burst_end[end])
                if burst_number[spike-1] not in spike_num: #extracts number of spikes in each EB present in a NB
                    spike_num.append(burst_number[spike-1])
                spike_num.append(burst_number[spike])
                if burst_duration[dur-1] not in duration: #extracts the burst duration of each EB in a NB
                    duration.append(burst_duration[dur-1])
                duration.append(burst_duration[dur])
                if burst_electrode[elec-1] not in electrode: #keeps track fo which electrode is bursting
                    electrode.append(burst_electrode[elec-1])
                electrode.append(burst_electrode[elec])
                       
        
        
        else: 
            
            elec_number = set(electrode) #if the umber of electrodes present is laregr than 20% of all bursting electrodes than we can classify the cluster of electrode bursts as a NB
            if len(network_start)>0 and len(elec_number) >= (minpercent*num_bursting) and sum(spike_num) >= 50:
                netburst_number.append(len(network_start))
                netburst_start.append(min(network_start))
                netburst_end.append(max(network_end))
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
    for item in range(len(netburst_number)):
            worksheet.write(item+1,20,netburst_number[item])        
         
    for item in range(len(num_electrode)):
            worksheet.write(item+1,21,num_electrode[item])  
    
    for item in range(len(netburst_start)):
            worksheet.write(item+1,22,netburst_start[item]) 
    
    for item in range(len(netburst_end)):
            worksheet.write(item+1,23,netburst_end[item]) 
    
    for item in range(len(netburst_dur)):
            worksheet.write(item+1,24,netburst_dur[item]) 
    
    for item in range(len(elecburst_dur)):
            worksheet.write(item+1,25,elecburst_dur[item]) 
    
    for item in range(len(spike_number)):
            worksheet.write(item+1,26,spike_number[item]) 
              
output.close()


        
            
            
    
   


    

