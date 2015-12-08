
"""
FILE: DownloadSinglePage.py
------------------
Author: Emily Franklin

This is my attempt to download the data from 1 page. 
"""

import sys
import os
import string
import datetime
import JSONUtils
from toolz import dicttoolz
from pip._vendor.requests.structures import LookupDict


verbose = False

def missing0s(cardNumber):
	if len(str(cardNumber)) == 1:
		return '0'
	else:
		return ''
	
def getTopDeckVectorDescriptor():
	list = []
	
	txt = ['Winner\'s main deck','Winner\'s side deck', 'other main decks','other side decks', 'all decks']
	for x in range(0,60):
		tn = (x-x%5)/5+1
		list.append('Tournament '+str(tn)+', '+txt[x%5])
		
	return list
	
	
def readDeckAndSideDeck(tourNumber,DeckNumber):
	#open the file, get the lines
	filename = 'DatabaseDownloadTools/Top8Decks/RawData/'+ missing0s(tourNumber)+str(tourNumber) + '/Deck ('+str(DeckNumber)+").txt"
	if verbose: print 'Opening '+filename
	
	MainDeck = []
	SideDeck = []
	isAWinnerDeck = False
	with open(filename, "r") as ins:
		ismaind = True
		lines = ins.readlines()
		for line in lines:
			line = line.strip()
			if line == 'W' or line == '\xef\xbb\xbfW': #UTF-8 in tourney 5 deck 8 (AEther)
				isAWinnerDeck = True
				continue;
			if line == '' or line == '\r\n' or line == '\n' or line == '\r'or line == ' ':
				ismaind = False;
				continue;
			if ismaind: 
				MainDeck.append(line)
			else:
				SideDeck.append(line)
	
	return (MainDeck, SideDeck, isAWinnerDeck)

def retrieveCardDataIntoVector(cardNumber, cardDicts,useRelevant):
	vector = []
	
	cardName = JSONUtils.getCardNameFromCardNumber(cardNumber,useRelevant)
	if cardName == None: return None
	
	for dict in cardDicts:
		if cardName in dict:
			vector.append(int(dict[cardName]))
		else:
			vector.append(0)
	
	return vector

def testVectorRetrieval(lookupDicts):
	print 'Starting Vector Retrieval for all cards...'
	allCardsVectors = []
	for x in range(1,30000):
		if x%500 == 0: print 'Processed '+str(x)+' cards...'
		v = retrieveCardDataIntoVector(x, lookupDicts, False)
		if v != None:
			v = [x] + v 
			allCardsVectors.append(v)
		
	print 'Done! Printing cards that were in a tournament deck... \n'
	for cardVector in allCardsVectors:
		if sum(cardVector[1:]) > 0:
			print '{:<60}'.format(JSONUtils.getCardNameFromCardNumber(cardVector[0],False))\
				+ str(cardVector[1:])
	
	print 'All done!'

def addCardDataToDict(cardData,dict):
	#split 4 Air Elemental into [4] [Air elemental]
	dataparts = cardData.strip().split(' ',1)
	cardName = dataparts[1]
	numAppearnces = int(dataparts[0])

	#if in the dictionary, add; otherwise, insert
	if cardName in dict:
		dict[cardName] = dict[cardName] + numAppearnces
	else:
		dict[cardName] = numAppearnces

def parseTopDecksIntoReadableData():
	if verbose: print 'Reading from Top Decks information...'
	
	#This is what we pass back
	lookupDicts = []
	
	#go throught the tournaments
	for tournament in range(1,13):
		if verbose: print 'Tournament #'+str(tournament)
		#make dictionaries of cardName-to-number appearing
		WinnerMainDeckDict = {}
		WinnerSideDeckDict = {}
		MainDeckDict = {}
		SideDeckDict = {}
		AllDeckDict = {}
		
		#go through decksof this tournament, populate dictionaries 
		for deck in range(1,9):
			if verbose: print '\tDeck #'+str(deck)	
			(MainDeck, SideDeck, isAWinnerDeck) = readDeckAndSideDeck(tournament, deck)
			AllDeck = MainDeck+SideDeck
			if not isAWinnerDeck: 
				for card in MainDeck:
					addCardDataToDict(card, MainDeckDict)
				for card in SideDeck:
					addCardDataToDict(card, SideDeckDict)
			else: 
				for card in MainDeck:
					addCardDataToDict(card, WinnerMainDeckDict)
				for card in SideDeck:
					addCardDataToDict(card, WinnerSideDeckDict)
			for card in AllDeck:
				addCardDataToDict(card, AllDeckDict)
			
		lookupDicts.append(WinnerMainDeckDict)
		lookupDicts.append(WinnerSideDeckDict)
		lookupDicts.append(MainDeckDict)
		lookupDicts.append(SideDeckDict)
		lookupDicts.append(AllDeckDict)
	
	if verbose: print 'Done reading top decks.'
	return lookupDicts

def printHumanReadableLookupDictStats(lookupDicts):
	labels = ['Winner Main Deck','Winner Side Deck','Main Decks\t','Side Decks\t','All Decks\t']
	
	for idx, dict in enumerate(lookupDicts):
		#print '\t\t'+str(dict)
		print 'Tournament:'+str((idx-(idx%5))/5+1)+'\tType:'+labels[idx%5]+'\t Cards:'+str(len(dict))

def verifyMappingJSONToDicts(lookupDicts):
	JSONCardsDict = JSONUtils.parseJsonIntoCardsDictionary()
	
	errorCount = {}
	for (i,dict) in enumerate(lookupDicts):
		tourneyInfo = 'Tournament:'+str((i-(i%5))/5+1)
		if (i%5 ==0): print 'Processing ' + tourneyInfo + '...' 
		for (idx,key) in enumerate(dict):
			if key not in JSONCardsDict.keys():
				thiskey = tourneyInfo+': '+key
				if thiskey not in errorCount:
					errorCount[thiskey] = 1
				else:
					errorCount[thiskey] += 1
	print '\n'
	for key in errorCount:
		print key + ':' + str(errorCount[key])

def main(argv):
	lookupDicts = parseTopDecksIntoReadableData()
	
	#testVectorRetrieval(lookupDicts)
	verifyMappingJSONToDicts(lookupDicts)
	
	
	
if __name__ == '__main__':
	main(sys.argv)