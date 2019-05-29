# -*- coding: utf-8 -*-
"""
Created on Mon May 27 17:49:52 2019

@author: Antoine
"""

#%% peristimulus time histogram

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import glob



def scaled(x):
    """returns a normalized x array
    """
    return (x-np.mean(x))/np.std(x)


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


def set_bin(x, frequency):
    """defines the length of the time bins we have to use in order to perform
    an optimal peristimulus histogram
    """
    
    x = x[x.f1==frequency]
    x = x.reset_index()
    temp = []
    for i in range(len(x)):
        spike_train = extract(x.at[i,"spikes"])
        temp = temp + spike_train.tolist()
    
    borne_max = max(temp)
    
    means = []
    variances = []
    cost_function = []
    for bin_size in range(10, 500, 10):
        n_bins = np.ceil((borne_max)/bin_size)
        bins = [[i*bin_size, (i+1)*bin_size] for i in range(0,int(n_bins))]
        count = np.zeros(len(bins))
        
        #comparison of times with bins to count
        for time in temp:
            for i, ith_bin in enumerate(bins):
                if ith_bin[0]<time<=ith_bin[1]:
                    count[i] = count[i] + 1

        means.append(np.mean(count))
        variances.append(np.var(count))
        cost_function.append((2*np.mean(count)-np.var(count))/((len(x)*bin_size/1000)**2))
    
#    return (1+cost_function.index(min(cost_function))) *10
    return range(10, 500, 10), cost_function

def psth(x, save=False):
    """function which draws the normalized psth of a given neuron
    ---
    Arguments:
        x : dataframe of a given neuron
        
        save : specifies if the histogram will be saved or not
        """
    
    bin_size = 800
    
    for f in x.f1.unique():
        temp = x[x.f1==f]
        temp = temp.reset_index()
        
        all_spikes = np.empty((0))
        for i in range(len(temp)):
            spike_train = extract(temp.at[i,"spikes"])
            all_spikes = np.concatenate((all_spikes, spike_train))
        
        borne_max = max(all_spikes)
        n_bins = np.ceil(borne_max/bin_size)
        bins = [[i*bin_size, (i+1)*bin_size] for i in range(0,int(n_bins))]
        count = np.zeros(len(bins))
        
        for time in all_spikes:
            for index, ith_bin in enumerate(bins):
                if ith_bin[0]<time<=ith_bin[1]:
                    count[index] = count[index] + 1
        
        x_axis = [np.mean(ith_bin) for ith_bin in bins]
        plt.plot(x_axis, scaled(count), label=f"{f}Hz")
            
    plt.legend(loc=0)
    plt.xlabel("time (ms)")
    plt.ylabel("firing rate (Hz)")
    
    if save:
        plt.savefig(f"figures/psth/psth_{name}.png")
    plt.show()

       
path = "clean_data"
file_list = os.listdir(path)


for neuron in file_list:
    data = pd.read_csv(os.path.join(path,neuron), index_col=0)
    name = neuron.split(sep=".")[0]
    psth(data, save=False)


#%% drawing the cost function
bin_size, cost_function = set_bin(data, 10)
plt.plot(bin_size, cost_function)
plt.xlabel("bin size")
plt.ylabel("cost function")
plt.savefig("figures/cost_function.pdf")
plt.show()

