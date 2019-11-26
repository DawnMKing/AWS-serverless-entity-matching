#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 12:42:21 2019

@author: dawn.king
"""
import boto3
import jellyfish as jf
import pandas as pd
from os import listdir

session = boto3.Session(profile_name='innovation')
comp = session.client('comprehend')
df=pd.read_csv('/Users/dawn.king/Desktop/Johego/permutate_vocab.csv')

vocab=df[['RecordingSid','Input.Name']]
filename=listdir('/Users/dawn.king/Desktop/Johego/results/text_results/')

for index,row in vocab.iterrows():
    result_list=[]
    for file in filename:    
        text_file = open("/Users/dawn.king/Desktop/Johego/results/text_results/"+file, "r")
        rename_file=file.replace('.json.txt','') 
        file=file.replace('.mp3.json.txt','')
        get_id=file.split('-')
        audio_id=get_id[1]
        match=jf.levenshtein_distance(row[0],audio_id)
#if matches audiofile name with dataframe row       
        if match==0:          
            names=row[1].split(',')
#get key phrases from txt file convert to list
            script=text_file.read()
            phrases=comp.detect_key_phrases(Text=script,LanguageCode='en')
            phrase_list=[]
            
            for item in phrases['KeyPhrases']:
                text=item['Text']
                phrase_list.append(text)
            print("##########", audio_id,phrase_list, len(phrase_list))
            for name in names:
                for phrase in phrase_list:
                    i=phrase.replace(' ','').replace('-','').lower()
                    key_word=name.replace(' ','').replace('-','').lower()
                    ld=jf.levenshtein_distance(i,key_word)
                    jw=jf.jaro_distance(i,key_word)
                     
                    if ld <=4 and jw >=0.60:
                        result_list.append([phrase,name,ld,jw])    
            
            resdf=pd.DataFrame(result_list,columns=['AWS Phrase','Output File', 'Levenshtein','Jaro'])
            isempty=resdf.empty
            print(isempty)
            if resdf.empty == False:
                print(resdf)
                csv_file = open("/Users/dawn.king/Desktop/Johego/results/NLP-results/"+rename_file+".csv", "w")
                resdf.to_csv("/Users/dawn.king/Desktop/Johego/results/NLP-results/"+rename_file+".csv") 
                csv_file.close()
     