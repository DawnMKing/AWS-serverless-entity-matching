#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 17:22:54 2019

@author: dawn.king
"""
import boto3
import json
import os
import sys
import time
import botocore
import requests
import pandas as pd

session = boto3.Session(profile_name='innovation')
s3 = session.client('s3')
transcribe = session.client('transcribe')

databucket = 'king-johego-test'
transcribebucket='king-johego-transcribe'
subfolder = 'audio-files'
region='us-east-1'
df=pd.read_csv('/Users/dawn.king/Desktop/Johego/Data/output.csv')

def ListFiles(s3):
    """List Audio Files in specific S3 URL"""  
    response = s3.list_objects_v2(Bucket=databucket, Prefix=subfolder)
    for content in response.get('Contents', []):
        yield content.get('Key')

def TranscripeFiles(file_list):

    for file in file_list:
        audiofilename=file.replace('.mp3','').split('/')

        if audiofilename[1]=="": #skip first row of list output becuase only list /audio-files and not mp3           
            pass
        else:
            Media_url='https://s3.amazonaws.com/king-johego-test/'+file
            response = transcribe.start_transcription_job(
                TranscriptionJobName=audiofilename[1],
                LanguageCode='en-US',
                MediaFormat='mp3',
                Media={
                    'MediaFileUri': Media_url
                },
        #  OutputBucketName=transcribebucket
            Settings={
                'VocabularyName': 'Vocab',
                'ShowSpeakerLabels': True,
                'MaxSpeakerLabels': 2,

           }
            )
                     
            

if __name__ == "__main__":
#get list of audio files stored in s3
    file_list = ListFiles(s3)
##transcribe the files
    TranscripeFiles(file_list)



        



