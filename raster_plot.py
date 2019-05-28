# -*- coding: utf-8 -*-
"""
because the whole data is in a shity form, I have to extract the data 
manually
"""

#%% raster plot

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat
import os
import pandas as pd
import glob

path = "C:/Users/Antoi/pca_monkey/clean_data/"
file_list = glob.glob(path+"R*.txt")
data = pd.read_csv("clean_data/) 
for ith_train in range(len(data)):
    y = [ith_train +1 for i in range(len(data.spikes[ith_train]))]
    
    plt.plot(data.spikes[ith_train], y, '.', markersize=1, color="black")
          
plt.xlabel("time (ms)")
plt.ylabel("ith spike train")
plt.savefig("figures/one_neuron_spike_train.png")
plt.show()





