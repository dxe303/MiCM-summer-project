#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 11:45:16 2021

@author: xueerding
"""

import sys
import pandas as pd
import seaborn as sns
import matplotlib as plt

inputFile = sys.argv[1]  # first field should be input file path

# hierarchical clustering by cell line
data2 = pd.read_excel(inputFile, sheet_name="Edited", header=4, index_col=[0,1,2], skiprows=[5,])


data_to_clus2 = data2[['Total spikes', 'MFR', 'Number of bursts', 
                     'Number of network bursts', 'Synchrony index']]

groups2 = data2.index.get_level_values(0)

lut2 = dict(zip(groups2.unique(), ['firebrick', 'darkorange', 'gold', 'springgreen', 
                                   'deepskyblue', 'slateblue', 'purple']))

row_colors2 = groups2.map(lut2)
data_clusterGrid2 = sns.clustermap(data_to_clus2, standard_scale=1, figsize=(12, 10), 
                                   dendrogram_ratio=(.3, .3), cbar_pos=(0, .05, .03, .3),
                                   row_colors=row_colors2 )

data_clusterGrid2.savefig("hierarchical.png")

plt.show()