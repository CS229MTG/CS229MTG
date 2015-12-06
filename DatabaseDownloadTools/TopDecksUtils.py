
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


verbose = False

def missing0s(cardNumber):
	if len(str(cardNumber)) == 1:
		return '0'
	else:
		return ''

def removeCarriageReturn(list):
	for idx, line in enumerate(list):
		list[idx] = line[:-1]
	
def readDeckAndSideDeck(tourNumber,DeckNumber):
	#open the file, get the lines
	filename = 'Top8Decks/RawData/'+ missing0s(tourNumber)+str(tourNumber) + '/Deck ('+str(DeckNumber)+").txt"
	if verbose: print 'Opening '+filename
	
	MainDeck = []
	SideDeck = []
	with open(filename, "r") as ins:
		ismaind = True
		for line in ins:
			if line == '' or line == '\r\n' or line == '\n' or line == '\r':
				ismaind = False;
				continue;
			if ismaind: 
				MainDeck.append(line)
			else:
				SideDeck.append(line)
		
	
	removeCarriageReturn(MainDeck)
	removeCarriageReturn(SideDeck)
	
	return (MainDeck, SideDeck)
	
def main(argv):
	verbose = False
	if len(argv) > 0:
		if argv[1] == '-v': verbose = True
	
	for tournament in range(1,12):
		for deck in range(1,8):
			(MainDeck, SideDeck) = readDeckAndSideDeck(tournament, deck)
			#This is a list of cards with the number of that card in it.
			#Like, entry = '4 Godless Shrine'
			#The winning deck's first entry is 'W'
			
			#should you wish to view the cards
			viewing = False
			if viewing: print 'Here we go: ' + str(tournament) + ' and ' + str(deck)
			if viewing: print '\nMainDeck: ' + str(MainDeck)
			if viewing: print '\nSideDeck: ' + str(SideDeck)
	
if __name__ == '__main__':
	main(sys.argv)