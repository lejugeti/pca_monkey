# -*- coding: utf-8 -*-
"""
PCA project for the CA6b course. Project realised by Antoine Parize

"""
#%% functions to use
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat
import os
import pandas as pd



        
path_list = os.listdir(os.path.join("rr014"))

table = loadmat("rr014/R14001_001")['result']


def table_index(table):
    """
    returns the index of the i-th table loaded, in case of the data organization changes
    """
    
    index_dict = {}
    for index, name in enumerate(table[0]):
        index_dict[name[0]] = index
    return index_dict


def meanrate_single_bin(table, time_bin, freq):
    """
    returns the mean spiking rate of i-th neuron for a given time bin and 
    frequency
    ---
    args:
        table: the i-th neuron table to look at.
        
        time_bin: a list of two boundaries for the time bin we want to look in
            time is in milliseconds here.
            example -> [1010, 1020]
        
        freq: the frequency to take into account for the mean.
    
    ---
    return
        
        mean of the i-th neuron in time_bin for a given frequency. The result is a numpy float.
    """
    
    time_min = time_bin[0]
    time_max = time_bin[1]
    essay_number = 0
    spike_count = 0
    #checks all the table trials for given frequency and time bin 
    for trial in range(1, len(table)):
        if table[trial, index_dict["f1"]][0][0] == freq:
            essay_number += 1
            for train in table[trial, index_dict["spikes"]][0]:
                for spike in train[0]:
                    if time_min <= spike < time_max:
                        spike_count += 1 
    
    return spike_count/essay_number


def meanrate_overall(table):
    """
    computes the mean spiking rate for the i-th neuron, over time and frequency
    """
    
    #get n_frequencies in table
    frequencies = list()
    for freq in table[1:, index_dict["f1"]]:
        if freq[0][0] not in frequencies:
            frequencies.append(freq[0][0])
    
    n_frequencies = np.sum(np.isreal(frequencies))
    
    #get n_timebin
    n_timebin = 1000
    all_time_bins = [[i, i+10] for i in range(0, 10000, 10)]
    
    #compute the sum of spiking rates
    rates_sum = 0
    for f1 in frequencies:
        for time_bin in all_time_bins:
            rates_sum += meanrate_single_bin(table, time_bin, f1)
    
    return (1/(n_timebin*n_frequencies))*rates_sum
    






index_dict = table_index(table)

a = meanrate_overall(table)
print(a)
#%% graphical help

import matplotlib.pyplot as plt


table = loadmat("C:/Users/Antoi/pca_monkey/rr014/R14001_001")['result']

for number, trial  in enumerate(table[1:, 5]):
    spikes = []
    for train in trial[0]:
        for spike in train[0]:
            spikes.append(spike)
    value = [number for i in range(len(spikes))]
    plt.plot(spikes, value, marker='.', linestyle = 'none', color="black", markersize = 0.5)

plt.show()




