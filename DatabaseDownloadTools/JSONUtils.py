
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
try:
	os.chdir('C:\Users\Emily\Documents\GitHub\CS229MTG')
except:
	pass

JSONUtilsVerbose = True;
#mana cost portion
manaCostGeneric = ['Generic Mana attr']
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
typesVector = ['Creature','Artifact','Land','Planeswalker',
'Tribal','Instant','Enchantment','Sorcery']
#description words
descriptionVector = []
with open('DatabaseDownloadTools\mechanic strings','r') as f:
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
totalVectorNames = manaCostGeneric+manaCostVector+cmcVector+colorsVector+\
	typesVector+descriptionVector+powerVector+\
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
	json_file = 'DatabaseDownloadTools\DATA-AllCards-x.json'
	with open(json_file, 'r') as f:
		cards = loads(f.read()) 
	if JSONUtilsVerbose: print 'Parsing JSON Complete.'
	#return the dictionary made
	return cards

def numAppearancesCaseInsensitive(string, substr):
	newstring = string.lower()
	newsubstr = substr.lower()
	return newstring.count(newsubstr)

def getManaVector(card):
	vector = []
	#try to get the card's mana- otherise 0 fill
	try:
		mc = str(card['manaCost'])
	except:
		#generic
		vector.append(0)
		#manatypes
		for manatype in manaCostVector:
			vector.append(0)
		return vector
	
	#get the generic cost
	singleDigitSearch = re.search('{[0-9]}',mc)
	doubleDigitSearch =  re.search('{[0-9][0-9]}',mc)
	if singleDigitSearch != None:
		vector.append(int(singleDigitSearch.group(0)[1:-1]))
	elif doubleDigitSearch != None:
		vector.append(int(doubleDigitSearch.group(0)[1:-1]))
	else:
		vector.append(0)
		
	#get the manatypes
	for manatype in manaCostVector:
		vector.append(numAppearancesCaseInsensitive(mc,manatype))
	return vector

def getVectorFromNumber(card,key):
	vector = []
	try:
		vector.append(int(str(card[key])))
	except:
		vector.append(0)
	return vector

def getVectorFromContaining(card, inputVector, key):
	vector = []
	if key not in card.keys():
		for input in inputVector:
			vector.append(0)
	else: 
		for input in inputVector:
			if input in card[key]:
				vector.append(1)
			else:
				vector.append(0)
	return vector
def getVectorFromCountOf(card,key):
	vector = []
	if key not in card.keys():
		vector.append(0)
	else: 
		vector.append(len(card[key]))
	return vector

def getLegalitiesVector(card):
	vector = []
	if 'legalities' not in card.keys():
		for format in formats1Vector:
			vector.append(0)
		for format in formats2Vector:
			vector.append(0)
	else: 
		for format in formats1Vector+formats2Vector:
			isLegal = False
			for legality in card['legalities']:
				if legality['format'] == format and legality['legality'] == 'Legal':
					isLegal = True
					
			if isLegal: vector.append(1)
			else: vector.append(0)
	
	return vector
	
def makeVectorFromCardData(card):
	vector = []
	#generic mana cost
	vector += getManaVector(card)
	vector += getVectorFromNumber(card,'cmc')
	vector += getVectorFromContaining(card, colorsVector,'colors')
	vector += getVectorFromContaining(card, typesVector,'types')
	vector += getVectorFromContaining(card, descriptionVector,'text')
	vector += getVectorFromNumber(card,'power')
	vector += getVectorFromNumber(card,'toughness')
	vector += getVectorFromCountOf(card,'printings')
	vector += getVectorFromCountOf(card,'rulings')
	vector += getLegalitiesVector(card)
	return vector

def getCardNameFromCardNumber(cardNumber,useRelevant):
	#open the file, get the card name
	#missing 0's:
	mm0s = missing0s(cardNumber)
	
	if useRelevant:
		filename = 'DatabaseDownloadTools/RelevantCardPriceData/RelevantCardData'+ mm0s + str(cardNumber)+'.txt'
	else:
		filename = 'DatabaseDownloadTools/cardPriceData/CardData'+ mm0s + str(cardNumber)+'.txt'
	
	#Check for existence of card
	try:
		with open(filename, 'r') as f:
			cardName = f.readline().strip()
		return cardName
	except: 
		return None
	
def retrieveCardDataIntoVector(cardNumber, cardDict, useRelevant):
	#get the card name
	cardName = getCardNameFromCardNumber(cardNumber, useRelevant)
	if cardName == None: return None
	
	#look in dictionary for card
	try:
		card = cardDict[cardName]
	except:
		print 'failed to map card to json'
		return None
		
		
	#Okay, time to parse a vector and return it!!
	return makeVectorFromCardData(card)

	
def findErrorsInMapping():
	if JSONUtilsVerbose: print 'Mapping cards from price data to JSON data and recording errors...'
	#attempt to retrieve data
	errfilename = 'FAILURESMappingPriceToCardName.txt'
	try: #delete if exists
		os.remove(errfilename)
	except OSError:
		pass
	with open(errfilename, 'w') as f:
		for x in range(1,28000):
			if x%500 ==0: print 'Processed '+str(x)+ 'cards...'
			if retrieveCardDataIntoVector(int(x), cardsDict) == None:
				f.write(str(x)+'\n')
	print 'Done!'

def findEtherCards(JSONCardsDict):
	print 'Searching for AEther!!'
	for key in JSONCardsDict:
		if u'therling' in unicode(key):
			print str(type(key))+': '+key+'\t\t'+unicode(key)

def testing(cardsDict):
	
	for x in range(1,28000):
		#if x%500 ==0: print 'Processed '+str(x)+ 'cards...'
		
		#get the card vector
		name = getCardNameFromCardNumber(x, False)
		if name != None: print name
		cardVector = retrieveCardDataIntoVector(int(x), cardsDict)
		if cardVector != None: print '\tVector length:' + str(len(cardVector))

def main(argv):
	
	#get dictionary
	cardsDict = parseJsonIntoCardsDictionary()
	findEtherCards(cardsDict)
		
	print 'Done!'
if __name__ == '__main__':
	main(sys.argv)
