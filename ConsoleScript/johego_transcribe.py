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
df=pd.read_csv('/Users/dawn.king/Desktop/Johego_GitHub/Data/output.csv')

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
                     
            
            
def get_completed_jobs():
    next_token = " "
    # boto3 will throw an error if you provide an empty NextToken but it doesn't
    # have a no-value placeholder so we'll abuse kwargs:
    kwargs = {}

    while True:
        try:
            response = transcribe.list_transcription_jobs( **kwargs)
            print(response)
        except botocore.exceptions.ClientError as exc:
            if exc.response["Error"]["Code"] == "ThrottlingException":
                print("Rate-limiting encountered; will retry in 5 seconds…")
                time.sleep(5)
                continue
            else:
                print("Error while listing jobs:", exc, file=sys.stderr)
                raise

        for summary in response["TranscriptionJobSummaries"]:
            yield summary["TranscriptionJobName"]

        next_token = response.get("NextToken")
        if not next_token:
            break
        else:
            kwargs["NextToken"] = next_token


def download_completed_jobs(results_directory):
    for job_name in get_completed_jobs():
        output_name = os.path.join(results_directory, "%s.json" % job_name)

        if os.path.exists(output_name):
            continue

        results = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        transcript_url = results["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
        print(f"Retrieving {job_name}",transcript_url)

        resp = requests.get(transcript_url)
        if not resp.ok:
            print(
                f"{job_name}: HTTP {resp.status_code} {resp.reason} {transcript_url}",
                file=sys.stderr,
            )
            continue

        with open(output_name, "w+") as output_file:
            json.dump(resp.json(), output_file)
if __name__ == "__main__":
    # FIXME: add some command-line parsing:
#get list of audio files stored in s3
    file_list = ListFiles(s3)
    #print("FileName",file_list)
#    for file in file_list:
#        print(file['Key'])
##transcribe the files
    #TranscripeFiles(file_list)


    a=get_completed_jobs()
    print('aaa',a)

    

###make output directory and download completed job
    #NEED TO ADD a job waiter function here. until then you must comment out the section below
    #until all jobs have transcribed, once transcribed uncomment below and comment the TranscribeFIles function above
    base_dir = os.path.realpath("results")
    os.makedirs(base_dir, exist_ok=True)
    download_completed_jobs(base_dir)            



