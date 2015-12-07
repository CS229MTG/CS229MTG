
"""
FILE: SortCards.py
------------------
Author: Emily Franklin

This is my attempt to download the data from 1 page. 
"""

import sys
import os
import string
import datetime
from .. import DataUtils

startCard=1
endCard=30000

dict = {}

def getFileNameFromCardNumber(c, src):
	cardNumber = str(c)
	#missing 0's:
	mm0s = DataUtils.missing0s(cardNumber)
	
	#open the file, get the lines
	filename = ''
	filename += 'CS229MTG/DatabaseDownloadTools/'
	filename += 'RelevantCardPriceData'
	filename += '/CardData'+ mm0s + cardNumber+".txt"
	return filename

def extractSetName(cardNumber):
	#get the prices
	filename = getFileNameFromCardNumber(cardNumber, True)
	try:
		with open(filename, 'r') as f:
			f.readline()
			setname = f.readline().strip()
	except:
		return 0
	
	#add to our list of sets
	if setname not in dict.keys():
		dict[setname] = str(cardNumber)
		return 1
	else:
		dict[setname] = str(dict[setname])+','+str(cardNumber)
		return 0

def main(argv):
	print 'Beginning to extract sets from cards...'
	numRelevant = 0
	for x in range(startCard,endCard):
		if x%500==0: print 'Extracted from ' + str(x) + ' files...'
		numRelevant += extractSetName(x)
	
	list = []
	for setname in dict:
		list.append(setname+':'+dict[setname])
	list.sort()
	
	with open('CS229MTG/DatabaseDownloadTools/Sets.txt','w') as f:
		f.truncate()
		for line in list:
			f.write(line+'\n')
	
	print 'Found ' + str(numRelevant)+' sets. Done!'
	
	
if __name__ == '__main__':
	main(sys.argv)
	
	