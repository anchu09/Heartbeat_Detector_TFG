#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 13:01:42 2023

@author: dani
"""

import os 
import pandas as pd
import glob
import csv
path= 'semi_preprocessed_signals/normalized_ecg'
os.chdir(os.getcwd()[:-len("heartbeat_detector")])

files = glob.glob(path + "/*.csv")


diccionarioDatos={}

for filename in files:
    diccionarioDatos[filename[(len(path)+1):len(filename)-4]]=pd.read_csv(filename,index_col=None,on_bad_lines='skip', delimiter="\t", header=None)


    for key in diccionarioDatos.keys():
        
        for i, chunk in enumerate(diccionarioDatos[key].groupby(diccionarioDatos[key].index // 5000)):
            chunk_filename = "./sliced_signals/ecgs/{}/{}_part{:03d}.csv".format(key, key, i+1)
            chunk[1].to_csv(chunk_filename, index=False, header=False, quoting=csv.QUOTE_NONE,escapechar='\\')


    diccionarioDatos.pop(filename[(len(path)+1):len(filename)-4])