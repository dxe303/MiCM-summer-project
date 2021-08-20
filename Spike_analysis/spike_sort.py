#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 15:48:01 2021

@author: xueerding
"""

import sys
import glob
import os
import csv
import pandas as pd

def spike_sort(inputFile):
    
    # read input into csv and aggregate by well
    df = pd.read_csv(inputFile, usecols=["Electrode", "Time (s)"])
    df.dropna(inplace=True)
    df2 = df.loc[df["Electrode"].str.fullmatch('\w\d_\d\d')]  # filter for electrode entries
    data = df2.groupby(df2["Electrode"].str[:2]).agg(list)

    # create folder for spike info by electrode
    outPath = inputFile[:-25] + '_well_list'
    os.mkdir(outPath)
    
    # write csv
    for well, row in data.iterrows():
        filename = outPath + '/' + well + '_spikes.csv'
        with open (filename, 'w') as csvfile: 
            writer = csv.DictWriter(csvfile, fieldnames=['Electrode', 'Time (s)'])
            writer.writeheader()
            for elec, time in zip(row['Electrode'], row['Time (s)']):
                writer.writerow({'Electrode': elec, 'Time (s)': time})
            csvfile.close()
    

input_folder = sys.argv[1]  # first command line argument should be input directory
        
# find spike files in input folder
files = glob.glob(input_folder + '/**/*spike_list.csv', recursive=True)
# calculate power spectrum for every spike file
for inputFile in files:
    spike_sort(inputFile)