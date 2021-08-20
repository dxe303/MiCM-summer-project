#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  6 14:28:43 2021

@author: ghislainedeyab
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import itertools
import numpy as np
import random as r 
from matplotlib.patches import Rectangle
#import neuronpy as neuron

#specify well  
well_list = ["A1_","A2_","A3_","A4_","A5_","A6_","B1_","B2_","B3_","B4_","B5_","B6_","C1_","C2_","C3_","C4_","C5_","C6_","D1_","D2_","D3_","D4_","D5_","D6_"]

for well in well_list:

    #import data
    data = pd.read_excel("/Users/ghislainedeyab/Desktop/AST23-2weeks.xlsx",sheet_name= well)
    
    #Creates a list of electrodes to plot
    electrode_list = []
    elec_row = 1
    elec_col = 0
    while len(electrode_list) < 16:
        while elec_col < 4:
            elec_col += 1
            electrode_list.append(well + str(elec_row) + str(elec_col))
        elec_col = 0
        elec_row += 1
    
       
    #Creates dictionary of each electrode and its spike data
    data_list = {k:[] for k in electrode_list}
    for k in data_list.keys():
        for index, row in data.iterrows():
            if row['Electrode'] == k:
                data_list[k].append(row['Time (s)'])
    
    elec_burst = {k: [] for k in electrode_list}#list of spike times involved in a burst
    for index, row in data.iterrows():
        for k,v in data_list.items():
            if row['Electrode'] == k:
                for i in v:
                    if i >= row['First spike time (sec)'] and  i <= row['Last spike time (sec)']:
                        elec_burst[k].append(i)
    
    for k,v in data_list.items():
        if len(v) == 0:
            data
    
        
    #Plot raster graph
    figure(num=None, figsize=(20,3),dpi=80,facecolor='w',edgecolor='k')
    plt.xlim(0,600)
    for key, val in data_list.items():
        if len(val) > 0:
            plt.scatter(data_list[key],[key]*len(val), marker="|", color = 'k', label=key)
        if len(val) == 0:
            rand = r.randint(70,90)
            plt.scatter(rand,key,marker="|",color='w')
          
    for key, val in elec_burst.items():
        plt.scatter(elec_burst[key],[key]*len(val), marker="|", color = 'b', label=key)
    
    #When calling on axis coordinates, plt.gca allows us to use the assigned axis 
    axis = plt.gca()
    
    beg_NB = [] #list of the start times of all the network bursts 
    end_NB = [] #list of the end times of all the network bursts 
    
    for index, row in data.iterrows():
        if row['Beginning of network burst'] > 0:
            beg_NB.append(row['Beginning of network burst'])
        if row['End of network burst'] > 0:
            end_NB.append(row['End of network burst'])
    
    # (x,y) are the coordinates of teh bottom left corner, width is in units of the x axis, and height is in units of y axis
    for beg, end in zip(beg_NB,end_NB):
        axis.add_patch(Rectangle((beg, -0.5),(end-beg),16, edgecolor = 'black',lw = 0.5, fill = False))
    
    plt.title(well)
    plt.xlabel('Time (sec)')
    plt.ylabel('Electrode')
    
    plt.show()
    
    
    
