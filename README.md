# AWS-serverless-entity-matching
AWS Lambda Function and Console code to transcribe audio files (AWS Transcribe) and entity matching (AWS Comprehend) with Levenshtein and Jaro-Winkler Scoring


# Requirements
Python 3.6

AWS Account
## For Console Code
AWS CLI set up
## For Layer Script
Docker 

# Parameters to modify/name
1.	S3 bucket name for raw audio files: ‘king transcribe-test’
2.	S3 bucket name for transcribed audio files: ‘king-comprehend-test’
3.	Vocabulary name: Vocab
4.	Transcribe lambda function name
5.	Comprehend lambda function


# Deploy Lambda Functions

1.	Go to AWS Cloud Management Console
2.	Select Services s3	

	a. Click Create bucket for audio files
	
	b. Name bucket (here its king-transcribe-test) and select region (US East N. Virginia), hit next. For these purposes, continue to hit next until bucket is created.
  	
	c. Create a Policy for the bucket 

 		i.	Enter s3 bucket, click Create Folder 
			
			1.	name the folder audio_files

  		ii.	Enter s3 bucket, click Create Folder 
			
			1.	name the folder vocab
			
			2.	upload permutate_vocab.csv 

		iii.	Enter s3 bucket, click Create Folder 
			
			1.	name the folder results

	d.	Create another bucket named ‘king-comprehend-test’ and select ‘US East N. Virginia’

3.	Select Lambda Service
 
	a.	Click Create Lambda Function

		i.	Select Author from Scratch

		ii.	Name Function TranscriptionJob

		iii.	Select Runtime Python 3.6

This might take a few seconds.
		
		iv.	Select Add Trigger
			
			1.	Select s3
			
			2.	Select Bucket ‘king-transcribe-test’
			
			3.	Add Prefix audio_files/
			
			4.	Add Suffix .mp3
		
		v.	Under Configuration Tab, Select TranscriptionJob in Designer
			
			1.	Copy and paste lambda_transcribe.py to enable inline code editing

			2.	Click save

		vi.	Under Permissions Tab, Click Manage these permissions. This will take you to the IAM console.
		
		vii. On left side, click Policies (take note of the role ARN at top of page

1.	Check S3 and Transcribe Full Access

2.	Click Policy Actions, Attach

3.	Find the role ARN name and check box

4.	Click attach policy

	b.	Click Create Lambda Function
		
		i.	Select Author from Scratch
		
		ii.	Name Function ComprehendJob
		
		iii.	Select Runtime Python 3.6

This might take a few seconds.
		
		iv.	Select Add Trigger
			
			1.	Select s3
			
			2.	Select Bucket ‘king-comprehend-test’
			
			3.	Add Suffix .json

		v.	Select ComprehendJob in Designer
			
			1.	Copy and paste lambda_nlp.py to enable inline code editing
			
			2.	Click save

		vi.	Under Permissions Tab, Click Manage these permissions. This will take you to the IAM console.
		
		vii.	On left side, click Policies (take note of the role ARN at top of page

1.	Check S3  and Comprehend Full Access
2.	Click Policy Actions, Attach
3.	Find the role ARN name and check box
4.	Click attach policy

	viii.	Create Lambda Layer
		
		1.	In terminal, navigate to lambda_layer folder
		
		2.	Select Add Layer, click back to Layers tab
		
		3.	Select Create Layer and fill out

		4.	Upload jellyfish.zip and pandas.zip
		
		5.	Click save




Set up is now complete. You should be able to upload the audio files to you’re the ‘king-transcribe-test’ bucket.
