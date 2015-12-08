
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014
Modifier: Emily Franklin (emily3)

CS145 parser modified heavily for CS229. 
"""

import sys
from json import loads
from re import sub
import re
import os
import os.path
import DataUtils

def getFileNameFromCardNumber(c, src):
	cardNumber = str(c)
	#missing 0's:
	mm0s = DataUtils.missing0s(cardNumber)
	
	#open the file, get the lines
	filename = ''
	filename += 'DatabaseDownloadTools/'
	filename += 'RelevantCardPriceData'
	filename += '/CardData'+ mm0s + cardNumber+".txt"
	return filename

def extractSetName(cardNumber):
	#get the sets
	filename = getFileNameFromCardNumber(cardNumber, True)
	try:
		with open(filename, 'r') as f:
			f.readline()
			setname = f.readline().strip()
		return setname
	except:
		return None

startCard=1
endCard=30000

#description words
setNamesVector = []
with open('DatabaseDownloadTools\SetNames.txt','r') as f:
	lines = f.readlines()
	for line in lines:
		leline = line.strip()
		setNamesVector.append(leline)

def getSetNameVector(cardNumber):
	vector = []
	thisSetName = extractSetName(cardNumber)
	if thisSetName == None: 
		return None
	
	error = True
	for setName in setNamesVector:
		if thisSetName == setName:
			vector.append(1)
			error = False
		else:
			vector.append(0)
	if error:
		print cardNumber
		return None
	
	return vector

def getCardNameFromCardNumber(cardNumber,useRelevant):
	#open the file, get the card name
	#missing 0's:
	mm0s = missing0s(cardNumber)
	
	if useRelevant:
		filename = 'DatabaseDownloadTools/RelevantCardPriceData/CardData'+ mm0s + str(cardNumber)+'.txt'
	else:
		filename = 'DatabaseDownloadTools/cardPriceData/CardData'+ mm0s + str(cardNumber)+'.txt'
	
	#Check for existence of card
	try:
		with open(filename, 'r') as f:
			cardName = f.readline().strip()
		return cardName
	except: 
		return None

def main(argv):
	
	for x in range(startCard,endCard):
		if x%500==0: print 'Card ' + str(x) + '...'
		vector = getSetNameVector(x)
		if vector != None: print str([x]+vector)
		
	print 'Done!'
if __name__ == '__main__':
	main(sys.argv)
