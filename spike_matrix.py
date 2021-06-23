#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 23:11:50 2021

@author: xueerding
"""

import pandas as pd
import csv

dict = {}
with open('/Users/xueerding/Desktop/MiCM/data/ACSF test 1h after seeding(000)(000)_spike_list.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    header = next(csv_reader)
    for row in csv_reader:
        if row[7] != '':
            if row[7] in dict:
                dict[row[7]].append(float(row[8]))
            else:
                dict[row[7]] = [float(row[8]),]
            
print(dict)
            
df = pd.DataFrame({key: pd.Series(value) for key, value in dict.items()})
print(df)