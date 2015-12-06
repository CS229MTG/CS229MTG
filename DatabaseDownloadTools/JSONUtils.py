
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
import os.path

JSONUtilsVerbose = True;
"""
Returns true if a file ends in .json
"""
def isJson(f):
	return len(f) > 5 and f[-5:] == '.json'
    
def missing0s(cardNumber):
    m0s = ''
    for x in xrange(1,6-len(str(cardNumber))):
        m0s += '0'
    return m0s

def parseJsonIntoCardsDictionary():
	if JSONUtilsVerbose: print 'Parsing JSON file...'
	#parse the json file
	json_file = 'DATA-AllCards-x.json'
	with open(json_file, 'r') as f:
		cards = loads(f.read()) 
	if JSONUtilsVerbose: print 'Parsing JSON Complete.'
	#return the dictionary made
	return cards

def retrieveCardDataIntoVector(cardNumber, cardDict):
	#open the file, get the card name
    #missing 0's:
	mm0s = missing0s(cardNumber)
	filename = 'cardPriceData/CardData'+ mm0s + str(cardNumber)+'.txt'
	
	try:
		with open(filename, 'r') as f:
			cardName = f.readline().strip()
	except: 
		return True
	
	#look in dictionary for card
	try:
		card = cardDict[cardName]
	except:
		return False
		
	return True

def main(argv):
	
	#get dictionary
	cardsDict = parseJsonIntoCardsDictionary()
	
	if JSONUtilsVerbose: print 'Mapping cards from price data to JSON data and recording errors...'
	#attempt to retrieve data
	errfilename = 'FAILURESMappingPriceToCardName.txt'
	try: #delete if exists
		os.remove(errfilename)
	except OSError:
		pass
	with open(errfilename, 'w') as f:
		for x in range(1,31):
			if not retrieveCardDataIntoVector(int(x), cardsDict):
				f.write(str(x)+'\n')
	print 'Done!'
	
if __name__ == '__main__':
	main(sys.argv)
