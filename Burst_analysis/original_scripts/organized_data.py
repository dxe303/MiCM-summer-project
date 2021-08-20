#!/usr/bin/env python3
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

sheetname = "Feb132020_ND3439SNCA_BTest2_1h"

data = pd.read_excel("/Users/ghislainedeyab/Desktop/Feb132020_ND3439SNCA_BTest2_1h(000)(000)_spike_list_1.xlsx",sheet_name=sheetname)
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


output = xlsxwriter.Workbook("/Users/ghislainedeyab/Desktop/Test1.xlsx")

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
        print(row.Electrode)
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


              
output.close()



            
            
    
   


    

