#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 10:04:06 2019

@author: dawn.king
"""

from __future__ import print_function
import boto3
import json


s3 = boto3.client('s3')
transcribe = boto3.client('transcribe')
transcribebucket='king-johego-nlp'




def lambda_handler(event, context):

    record = event['Records'][0]

    s3bucket = record['s3']['bucket']['name']
    s3object = record['s3']['object']['key']
    s3Path = "s3://" + s3bucket + "/" + s3object
    
    #remove '.mp3 and audio file name from key string'
    filename=s3object.split('/')
    filename=filename[1].replace('.mp3','')
    jobName = filename

    response = transcribe.start_transcription_job(
        TranscriptionJobName=jobName,
        LanguageCode='en-US',
        MediaFormat='mp3',
        Media={
            'MediaFileUri': s3Path
        },
        OutputBucketName=transcribebucket,
        Settings={
                'VocabularyName': 'Vocab',
                'ShowSpeakerLabels': True,
                'MaxSpeakerLabels': 2,

           }
    )

    print(json.dumps(response, default=str))

    return {
        'TranscriptionJobName': response['TranscriptionJob']['TranscriptionJobName']
    }