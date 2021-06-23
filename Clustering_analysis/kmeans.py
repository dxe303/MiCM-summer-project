#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 11:04:50 2021

@author: xueerding
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

<<<<<<< HEAD:Clustering_analysis/kmeans.py
data = pd.read_excel("/Users/xueerding/Desktop/MiCM/data/Extracted-Parameters.xlsx", sheet_name="Synuclein Triplication", header=4, index_col=[0,1], skiprows=[5,])
=======
#uncomment and add filepath to extracted parameters file
#data = pd.read_excel()
>>>>>>> f97b2d57c7b570e13d669a8eb50c73bdfb8a674b:kmeans.py

print(data.head(5))
print(data.tail(5))

kmeans = KMeans(n_clusters=3, init='k-means++')

data['cluster'] = kmeans.fit_predict(data[["Total spikes", "MFR", "Number of bursts", "Number of network bursts", "Synchrony index"]])


# visualize
centroids = kmeans.cluster_centers_
cen_x = [i[0] for i in centroids] 
cen_y = [i[1] for i in centroids]

data['cen_x'] = data.cluster.map({0:cen_x[0], 1:cen_x[1], 2:cen_x[2]})
data['cen_y'] = data.cluster.map({0:cen_y[0], 1:cen_y[1], 2:cen_y[2]})

colors = ['#DF2020', '#81DF20', '#2095DF']
data['c'] = data.cluster.map({0:colors[0], 1:colors[1], 2:colors[2]})


'''
# 2D plot
plt.scatter(data["Total spikes"], data["Number of bursts"], c=data.c, alpha = 0.6, s=10)
'''

# 3D plot
fig = plt.figure(figsize=(30,25))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(data["Total spikes"], data["MFR"], data["Synchrony index"], c=data.c, s=15)
ax.set_xlabel('Total spikes')
ax.set_ylabel('MFR')
ax.set_zlabel('Synchrony index')
<<<<<<< HEAD:Clustering_analysis/kmeans.py

'''
for i in range(data.shape[0]):
    plt.text(x=data["Total spikes"][i]+0.3, y=x=data["Total spikes"][i]+0.3)
plt.show()
'''

fig2 = plt.figure(figsize=(30,25))
ax2 = fig2.add_subplot(111, projection='3d')
ax2.scatter(data["Number of bursts"], data["Number of network bursts"], data["Synchrony index"], c=data.c, s=15)
ax2.set_xlabel('Number of bursts')
ax2.set_ylabel('Number of network bursts')
ax2.set_zlabel('Synchrony index')
plt.show()
=======
plt.show()
>>>>>>> f97b2d57c7b570e13d669a8eb50c73bdfb8a674b:kmeans.py
