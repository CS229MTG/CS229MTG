
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

#mana cost portion
manaCostVector = [
	'{W}','{U}','{B}','{R}','{G}',
	'{X}',
	'{2/W}','{2/U}','{2/B}','{2/R}','{2/G}',
	'{W/P}','{U/P}','{B/P}','{R/P}','{G/P}'
]
#converted cost
cmcVector = ['Converted Mana Cost attr']
#colors
colorsVector = ['White','Blue','Black','Red','Green']
#types
typesVector = ['Creature','Artiface','Land','Planeswalker',
'Tribal','Instant','Enchantment','Sorcery']
#description words
descriptionVector = []
with open('mechanic strings','r') as f:
	lines = f.readlines()
	for line in lines:
		leline = line.strip()
		descriptionVector.append(leline)
#power
powerVector = ['Power attr']
#power
toughnessVector = ['Toughness attr']
#number rulings
rulingsVector = ['Number of rulings attr']
#number printings
printingsVector = ['Number of Printings attr']
#formats with banned/legal
formats1Vector = ['Commander','Standard','Modern','Legacy']
#format vintage
formats2Vector = ['Vintage']


#all vectors combined for reference
totalVectorNames = manaCostVector+cmcVector+colorsVector+
	typesVector+descriptionVector+powerVector+
	toughnessVector+rulingsVector+printingsVector+formats1Vector+formats2Vector


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

def makeVectorFromCardData(card):
	vector = []
	vector.append(0)
	return vector
	
def retrieveCardDataIntoVector(cardNumber, cardDict):
	#open the file, get the card name
	#missing 0's:
	mm0s = missing0s(cardNumber)
	filename = 'cardPriceData/CardData'+ mm0s + str(cardNumber)+'.txt'
	
	#Check for existence of card
	try:
		with open(filename, 'r') as f:
			cardName = f.readline().strip()
	except: 
		return None
	
	#look in dictionary for card
	try:
		card = cardDict[cardName]
	except:
		return None
		
		
	#Okay, time to parse a vector and return it!!
	

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
		for x in range(1,28000):
			if x%500 ==0: print str(x)+ 'cards through'
			if not retrieveCardDataIntoVector(int(x), cardsDict):
				f.write(str(x)+'\n')
	print 'Done!'
	
if __name__ == '__main__':
	main(sys.argv)
