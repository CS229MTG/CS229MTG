
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
from ..DatabaseDownloadTools import DataUtils

		
"""
Returns true if a file ends in .json
"""
def isJson(f):
	return len(f) > 5 and f[-5:] == '.json'

def parseJsonIntoCardsDictionary():
	#parse the json file
	json_file = 'DATA-AllCards-x.json'
	with open(json_file, 'r') as f:
		cards = loads(f.read()) 
	print len(cards)
	#return the dictionary made
	return cards

def retrieveCardData(cardNumber, cardDict):
	#open the file, get the card name
    #missing 0's:
	mm0s = missing0s(cardNumber)
	filename = 'cardPriceData/CardData'+ mm0s + cardNumber+'.txt'
	
	with open(filename, 'r') as f:
		cardName = f.readline().strip()
	
	#look in dictionary for card
	return cardDict[cardName]

def main(argv):
	print 'HELLO'
	if len(argv) < 2:
		print >> sys.stderr, 'Usage: python JSONUtils <card number>'
		sys.exit(1)
	
	#get dictionary
	cardsDict = parseJsonIntoCardsDictionary()
	
	#attempt to retrieve data
	for f in argv[1:]:
		retrieveCardData(int(f), cardsDict)
	
if __name__ == '__main__':
	main(sys.argv)
