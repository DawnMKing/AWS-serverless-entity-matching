#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 12:50:39 2019

@author: dawn.king
"""
import boto3
import jellyfish as jf
import pandas as pd
import json



session = boto3.Session(profile_name='innovation')
comp = session.client('comprehend')
s3=session.client('s3')
s3r = session.resource('s3')
bucket = s3r.Bucket('king-johego-nlp')
transcribebucket='king-johego-nlp'
region='us-east-1'
df=pd.read_csv('/Users/dawn.king/Desktop/Johego/Data/permutate_vocab.csv')

vocab=df[['RecordingSid','Input.Name']]
download_path='/Users/dawn.king/Desktop/Johego/ConsoleScript/'


def ListFiles(s3):
    """List Audio Files in specific S3 URL"""  
    response = s3.list_objects_v2(Bucket=transcribebucket)

    for content in response.get('Contents', []):
        yield content.get('Key')
 

      
filename = ListFiles(s3)        


for file in filename:
    if file.endswith('.json'):
        audiofilename=file.replace('.json','')
        obj = bucket.Object(file).get() 
        data = obj['Body'].read().decode('utf-8') 
        json_content = json.loads(data)
        script=json_content['results']['transcripts'][0]['transcript']
            
        for index,row in vocab.iterrows():
            result_list=[]         
            match=jf.levenshtein_distance(row[0],audiofilename)
    #if matches audiofile name with dataframe row       
            if match==0:              
                names=row[1].split(',')
    #get key phrases from txt file convert to list
                phrases=comp.detect_key_phrases(Text=script,LanguageCode='en')
                phrase_list=[]
                
                for item in phrases['KeyPhrases']:
                    text=item['Text']
                    phrase_list.append(text)
                
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
                    csv_file = open("/Users/dawn.king/Desktop/JohegoResults/"+audiofilename+".csv", "w")
                    resdf.to_csv("/Users/dawn.king/Desktop/JohegoResults/"+audiofilename+".csv") 
                    csv_file.close()
        else:
            pass
     
