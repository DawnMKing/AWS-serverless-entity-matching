#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 10:08:11 2019

@author: dawn.king
"""

from __future__ import print_function
import boto3
import json
import jellyfish as jf
import pandas as pd
from io import StringIO

s3 = boto3.client('s3')
comp = boto3.client('comprehend')
transcribebucket='king-johego-nlp'
vocabbucket = 'king-johego-test'
itemname='vocab/permutate_vocab.csv'

#get vocab list from csv file used to match phrases
def get_vocab(bucketname, itemname):
    
    csv_obj = s3.get_object(Bucket=bucketname, Key=itemname)
    body = csv_obj['Body']
    csv_string=body.read().decode('utf-8')
    df = pd.read_csv(StringIO(csv_string))
    vdf=df[['RecordingSid','Input.Name']]
    
    return vdf
    
    

#Load transcribed json file from king-johego-nlp bucket, convert to text
def get_script(bucketname, itemname):
    
    s3r = boto3.resource('s3')
    obj = s3r.Object(bucketname, itemname)
    body = obj.get()['Body'].read().decode('utf-8')
    json_content = json.loads(body)
    script=json_content['results']['transcripts'][0]['transcript']

    return script
    
#match adio file with vocab list    
def get_audio_match(filename):   
    
    vocab=get_vocab(vocabbucket, itemname)
    for index,row in vocab.iterrows():
        match=jf.levenshtein_distance(row[0],filename)
        #if matches audiofile name with filename      
        if match==0:          
            names=row[1].split(',')
            return names   
            
def get_scores(vocab_list,phrases):
    
    phrase_list=[];result_list=[]
    for item in phrases['KeyPhrases']:
        text=item['Text']
        phrase_list.append(text)

    for name in vocab_list:
        for phrase in phrase_list:
            i=phrase.replace(' ','').replace('-','').lower()
            key_word=name.replace(' ','').replace('-','').lower()
            ld=jf.levenshtein_distance(i,key_word)
            jw=jf.jaro_distance(i,key_word)
             
            if ld <=4 and jw >=0.60:
                result_list.append([phrase,name,ld,jw])    
    df_result=pd.DataFrame(result_list,columns=['AWS Phrase','Output File', 'Levenshtein','Jaro'])    
    return df_result

def csv_to_s3(s3, df_result, bucket, filepath):
    csv_buf = StringIO()
    df_result.to_csv(csv_buf, header=True, index=False)
    csv_buf.seek(0)
    s3.put_object(Bucket=bucket, Body=csv_buf.getvalue(), Key=filepath)
    print(f'Copy {df_result.shape[0]} rows to S3 Bucket {bucket} at {filepath}, Done!')


def lambda_handler(event, context):
    
    record = event['Records'][0]
    s3bucket = record['s3']['bucket']['name']#To do, rename code variable that uses this
    s3object = record['s3']['object']['key']    

#remove '.json from and audio file key string'
    filename=s3object.replace('.json','')
    print(json.dumps(event))
    
    script=get_script(transcribebucket, s3object)
    phrases=comp.detect_key_phrases(Text=script,LanguageCode='en')
    vocab_list=get_audio_match(filename)
    if vocab_list is None:
        pass
    else:
        df_result=get_scores(vocab_list,phrases)
        print("WOHOOOOOOO",df_result)
        isempty=df_result.empty
        print(isempty)
        if df_result.empty == False:
            csv_to_s3(s3, df_result, vocabbucket, filepath='results/'+filename+'.csv')