keyFileName = 'data/WSJ_24.pos'
responseFileName = 'results_WSJ_24.pos'

def score (keyFileName, responseFileName):
	keyFile = open(keyFileName, 'r')
	key = keyFile.readlines()
	responseFile = open(responseFileName, 'r')
	response = responseFile.readlines()
	print(len(key))
	print(len(response))
	if len(key) != len(response):
		print("length mismatch between key and submitted file")
		exit()
		
from data.score import score

score (keyFileName, responseFileName)

