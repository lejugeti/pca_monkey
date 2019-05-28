# -*- coding: utf-8 -*-
"""
Created on Mon May 27 15:23:56 2019

@author: Antoine
"""

#%% import this first and set the repository to the PCA_monkey project

from scipy.io import loadmat
import os
import pandas as pd
import glob
import numpy as np


def extract(x):
    """returns the spikes of a given dataframe row in a convenient way. The
    data are originally encoded as strings in the files.
    ---
    Return 
    
    An array containing the spike times as floats64
    """
    x = x.split(sep=", ")
    x[0] = x[0][1:]
    x[-1] = x[-1][:-1]
    
    return np.array(x, dtype=np.float64)

#%% extracting files from matlab encoding

global_path = "data/"

for macaque in glob.glob(global_path + "/r*"):
    
    path_to_glob = os.path.join(macaque, "prefront", "r*.mat")
    
    for file_name in glob.glob(path_to_glob):
        data = loadmat(file_name)["result"]
    
        #f1 extraction
        f1 = []
        for trial in range(1, len(data)):
            f1.append(data[trial,3][0,0])
        
        #trial extraction
        trials = []
        for trial in range(1, len(data)):
            trials.append(data[trial,1][0,0])
            
        #spikes extraction
        spikes = []
        for trial in range(1, len(data)):
            temp = []
            for measure in range(data[trial,5].shape[1]):
                for time in data[trial,5][0,measure][0]:
                    temp.append(time)
            temp.sort()
            spikes.append(temp)


        clean = pd.DataFrame({"trial":trials, "f1":f1, "spikes":spikes})
        clean.to_csv("C:/Users/Antoi/pca_monkey/clean_data/" + 
                     file_name[-14:-4] + ".txt")
    

#%% aggregating the repetitive files to have only 1 file per neuron
        
path = "clean_data/"

for file_name in glob.glob(path+ "R*"):
    
    #taking the neuron name -1 string to check if multiple files for 1 neuron
    neuron_name = file_name[-14:-5] 
    path_to_glob = os.path.join(path, neuron_name+"?.txt")
    
    if len(glob.glob(path_to_glob))>1 and file_name[-5]=="1":
        file_list = glob.glob(path_to_glob)
        data = pd.read_csv(file_list[0], index_col=0)
    
        #just taking the other files to concatenate them
        for file in file_list[1:]:
            temp = pd.read_csv(file)
            data = pd.concat((data, temp), ignore_index=True)
            os.remove(file)
            
        os.remove(file_name)
        data.to_csv(file_list[0][:-8]+".txt")

#changing names of remaining files  
for file_name in glob.glob(path+ "R*_001.txt"):
    neuron_name = file_name[-14:-8]
    destination = os.path.join("clean_data/", neuron_name+".txt")
    source = os.path.join("clean_data/", file_name[-14:])
    os.rename(source, destination)

#%% transforming the time data into spike counts for each neuron

old_path = "clean_data/"
new_path = "count_data/"

frequencies = [10, 14, 18, 24,30,34] 
bin_size = 500
max_length = 10000
bins = [[i*bin_size, (i+1)*bin_size] for i in range(int(max_length/bin_size))]

for file_name in glob.glob(old_path+ "R*"):
    data = pd.read_csv(file_name, index_col=0)
    
    #checking if all frequencies are tested
    ok = True
    for freq in frequencies:
        if freq not in data.f1.unique():
            ok = False
    
    if ok:
        new = {"f1":[], "count":[]}
        
        for freq in frequencies:
            new["f1"].append(freq)
            temp = data[data.f1==freq]
            temp = temp.reset_index()
            
            all_spikes = np.empty((0))
            for trial in range(len(temp)):
                all_spikes = np.concatenate((all_spikes,extract(temp.at[trial,"spikes"])))
            
            count = np.zeros(len(bins))
            for time in all_spikes:
                for index, ith_bin in enumerate(bins):
                    if ith_bin[0]<time<=ith_bin[1]:
                        count[index] = count[index] + 1
            
            count = count/len(temp)
            new["count"].append(count.tolist())
        
        
        new = pd.DataFrame(new)
        new.to_csv(os.path.join(new_path, file_name[-10:]))