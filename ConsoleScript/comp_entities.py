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
            phrases=comp.detect_entities(Text=script,LanguageCode='en')
            syntax = comp.detect_syntax(Text=script,LanguageCode='en')

            phrase_list=[]
            #print(phrases)
            ent_df=None;syn_df=None
            for item in phrases['Entities']:
                if ent_df is None:
                    ent_df=pd.DataFrame(item,index=[0])
                else:
                    ent_df=ent_df.append(item,ignore_index=True)
            csv_file = open("/Users/dawn.king/Desktop/Johego/results/entity-results/"+rename_file+".csv", "w")
            ent_df.to_csv("/Users/dawn.king/Desktop/Johego/results/entity-results/"+rename_file+".csv") 
            csv_file.close() 
            
            for i in syntax['SyntaxTokens']:
                #print(i)
                #print(i['PartOfSpeech']['Tag'])
                df_ap=i['PartOfSpeech']['Tag']
                #print(df_ap)
                if syn_df is None:
                    syn_df=pd.DataFrame(i,index=[0])
                else:
                    syn_df=syn_df.append(i,ignore_index=True)



            print(syn_df)


            csv_file = open("/Users/dawn.king/Desktop/Johego/results/syntax-results/"+rename_file+".csv", "w")
            syn_df.to_csv("/Users/dawn.king/Desktop/Johego/results/syntax-results/"+rename_file+".csv") 
            csv_file.close()                    
