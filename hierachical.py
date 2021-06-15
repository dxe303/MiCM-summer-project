#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 11:04:50 2021

@author: xueerding
"""

import pandas as pd
import seaborn as sns

#uncomment and add filepath to extracted parameters file
#data = pd.read_excel("", 
#                     sheet_name="Edited", header=4, index_col=[0,1,2], skiprows=[5,])

data_to_clus = data[['Total spikes', 'MFR', 'Number of bursts', 
                     'Number of network bursts', 'Synchrony index']]

groups = data.index.get_level_values(0)
print(groups.unique())
lut = dict(zip(groups.unique(), ['firebrick', 'darkorange', 'gold', 'springgreen', 
                                 'deepskyblue', 'slateblue', 'purple']))
print(lut)
row_colors = groups.map(lut)
data_clusterGrid = sns.clustermap(data_to_clus, standard_scale=1, figsize=(12, 10), 
                                  dendrogram_ratio=(.3, .3), cbar_pos=(0, .05, .03, .3), 
                                  row_colors=row_colors)

#uncomment and add filepath to extracted parameters file
#data2 = pd.read_excel("", 
#                     sheet_name="Edited", header=4, index_col=[0,1,2], skiprows=[5,])

print(data2.head(5))
print(data2.tail(5))

data_to_clus2 = data2[['Total spikes', 'MFR', 'Number of bursts', 
                     'Number of network bursts', 'Synchrony index']]

groups2 = data2.index.get_level_values(0)
print(groups2.unique())
lut2 = dict(zip(groups2.unique(), ['firebrick', 'darkorange', 'gold', 'springgreen', 
                                   'deepskyblue', 'slateblue', 'purple']))
print(lut2)
row_colors2 = groups2.map(lut2)
data_clusterGrid2 = sns.clustermap(data_to_clus2, standard_scale=1, figsize=(12, 10), 
                                   dendrogram_ratio=(.3, .3), cbar_pos=(0, .05, .03, .3),
                                   row_colors=row_colors2 )
