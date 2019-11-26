#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 11:19:49 2019

@author: dawn.king
"""


from os import listdir
import pandas as pd
import json



df=pd.read_csv('/Users/dawn.king/Desktop/Johego/output.csv')



vocab=df[['RecordingSid','Input.Name']]

filename=listdir('/Users/dawn.king/Desktop/Johego/results/')
for file in filename:
    if file.endswith('.json'):
        data = json.load(open('/Users/dawn.king/Desktop/Johego/results/'+file, 'r', encoding='utf-8'))
    
        script=data['results']['transcripts'][0]['transcript']#.replace('"','')
    text_file = open("/Users/dawn.king/Desktop/Johego/results/"+file+".txt", "w")
    text_file.write(script)
    text_file.close()


