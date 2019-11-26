#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 11:53:57 2019

@author: dawn.king
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 17:22:54 2019

@author: dawn.king
"""
from os import listdir
import boto3
session = boto3.Session(profile_name='innovation')
s3 = session.client('s3')
trans = session.client('transcribe')

filename=listdir('/Users/dawn.king/Desktop/Johego_GitHub/audio_files/')
for file in filename:
   print(file)
   if file.endswith(".mp3"):
       file=file.replace(".mp3","")
       print(file)
       trans.delete_transcription_job(TranscriptionJobName=file)




