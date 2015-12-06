
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
import os
from json import loads
from re import sub
try:
	os.chdir('C:\Users\Emily\Documents\GitHub\CS229MTG\DatabaseDownloadTools')
except:
	print 'no'
	
	
	
CategoriesDict = {}
UserDict = {}
BidsList = []
ItemsList = []


		
"""
Returns true if a file ends in .json
"""
def isJson(f):
	return len(f) > 5 and f[-5:] == '.json'

def parseJson():
	json_file = 'DATA-AllCards-x.json'
	with open(json_file, 'r') as f:
		cards = loads(f.read()) # creates a Python dictionary of Items for the supplied json file
		
	
	while True:
		cardName = raw_input("Enter card name:")
		if cardName == 'exit': break
		if cardName == '': break
		try:
			thiscard = cards[cardName]
		except:
			print 'Card not found'
			continue
		try:
			legalities = thiscard['legalities']
			for legality in legalities:
				print '\t'+legality['format']+': \t'+legality['legality']
		except:
			print 'CARD ATTRIBUTE FAILURE'
			for key in thiscard.keys():
				if thiscard[key] is str:
					print key+': '+str(thiscard[key])
				else:
					print key+': '+str(len(thiscard[key]))
		
def main(argv):
		parseJson()
	
if __name__ == '__main__':
	main(sys.argv)
