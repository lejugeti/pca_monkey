# -*- coding: utf-8 -*-
"""
Created on Mon May 27 15:23:56 2019

@author: Antoine
"""

#%% extracting files from matlab encoding

from scipy.io import loadmat
import os
import pandas as pd
import glob

global_path = "C:/Users/Antoi/pca_monkey/data/"


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
        
path = "C:/Users/Antoi/pca_monkey/clean_data/"

for file_name in glob.glob(path+ "R*"):
    
    #taking the neuron name -1 string to check if multiple files for 1 neuron
    neuron_name = file_name[-14:-5] 
    path_to_glob = os.path.join(path, neuron_name+"?.txt")
    
    if len(glob.glob(path_to_glob))>1 and file_name[-5]=="1":
        print("oui")
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
        