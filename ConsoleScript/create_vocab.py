#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 16:21:08 2019

@author: dawn.king
"""
import boto3
import pandas as pd
import json

session = boto3.Session(profile_name='innovation')

trans = session.client('transcribe')

vocab_list=['SUTTON-IN-HOME-SENIOR-CARE','SUTTON-IN-HOME','SUTTON-IN-HOME-SENIOR',\
            'HOME-SENIOR-CARE','SENIOR-CARE','SUTTON','Home','Senior','Care','ELDON-MONTESSORI-SOCIETY-INC',\
            'ELDON-MONTESSORI','ELDON-MONTESSORI-SOCIETY','MONTESSORI-SOCIETY-INC','MONTESSORI-SOCIETY',\
            'Eldon','Montessori','society','DAV-INC','DAV','D.A.V','TIGER-TOTS-CHILD-DEVELOPMENT',\
            'Tiger','tots','tiger-tots','tiger-tots-child','TOTS-CHILD-DEVELOPMENT','development',\
            'NEWBORNS-IN-NEED',"Newborns",'need','OPERATING-ROOM','operating','WORLD-DISCOVERIES-DAYCARE',\
            'world','world-discoveries','discoveries-daycare','SPRINGFIELD-SPARC-O.F.C',\
            'springfield','Sparc','SPRINGFIELD-SPARC','NAMI','nami']

def GetVocab():
    response=trans.create_vocabulary(VocabularyName='Vocab',LanguageCode='en-US',Phrases=vocab_list)        
    return response
VocabName=GetVocab()
print(VocabName)
    



