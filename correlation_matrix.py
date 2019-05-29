# -*- coding: utf-8 -*-
"""
Created on Tue May 28 16:20:00 2019

@author: Antoine
"""

#%% import this first

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import glob


def extract(x):
    """returns the spikes of a given dataframe row in a convenient way. The
    data are encoded as strings in the files.
    ---
    Return 
    
    An array containing the spike times as floats64
    """
    x = x.split(sep=", ")
    x[0] = x[0][1:]
    x[-1] = x[-1][:-1]
    
    return np.array(x, dtype=np.float64)

def extract_all(x):
    """return a concatenated array of all the spike counts in a given dataframe
    """
    all_counts = np.empty((0))
    for i in range(len(x)):
        all_counts = np.concatenate((all_counts, extract(x.at[i,"count"])))
    
    return all_counts

def mean_overall(x):
    """compute the mean firing rate of neuron x by averaging the data over
    all time bins and frequencies
    """
    all_counts = extract_all(x)
    
    return np.mean(all_counts)
        
    
    
#%% correlation matrix
    
path = "count_data"
 
file_list = glob.glob(os.path.join(path, "R*"))
cov_matrix = np.zeros((len(file_list), len(file_list)))

done = 0
for i, ith_file in enumerate(file_list):
    neuron_i = pd.read_csv(ith_file, index_col=0)
    count_i = extract_all(neuron_i)
    
    for j, jth_file in enumerate(file_list):
        neuron_j = pd.read_csv(jth_file, index_col=0)
        count_j = extract_all(neuron_j)
        cov_matrix[i,j] = np.cov(count_i, count_j)[0,1]
        
        done += 1
        print(100*done/(len(file_list)**2))

#save the matrix into a text file
cov_matrix.dump("covariance_matrix.txt")

#%% second technique without the np.cov function    
path = "count_data"
 
file_list = glob.glob(os.path.join(path, "R*"))
cov_matrix = np.zeros((len(file_list), len(file_list)))

done = 0
for i, ith_file in enumerate(file_list):
    neuron_i = pd.read_csv(ith_file, index_col=0)
#    count_i = extract_all(neuron_i)
    mean_i = mean_overall(neuron_i)
    
    for j, jth_file in enumerate(file_list):
        neuron_j = pd.read_csv(jth_file, index_col=0)
#        count_j = extract_all(neuron_j)
        mean_j = mean_overall(neuron_j)
#        cov_matrix[i,j] = np.cov(count_i, count_j)[0,1]
        cov = 0
        for row in range(len(neuron_i)):
            count_i = extract(neuron_i.at[row, "count"])
            count_j = extract(neuron_j.at[row, "count"])
            for time_bin in range(len(count_i)):
                cov += (count_i[time_bin]-mean_i)*(count_j[time_bin]-mean_j)
        
        cov_matrix[i,j] = cov/120
        done += 1
        print(100*done/(len(file_list)**2))

#save the matrix into a text file
#cov_matrix.dump("covariance_matrix.txt")
#%% see the axis

cov_matrix = np.load("covariance_matrix.txt", allow_pickle=True)
