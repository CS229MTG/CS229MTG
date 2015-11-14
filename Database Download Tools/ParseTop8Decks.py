
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
	else 
		return ''

def removeCarriageReturn(list):
    for idx, line in enumerate(list):
        list[idx] = line[:-1]
    
def readDeckAndSideDeck(tourNumber,DeckNumber):
    #open the file, get the lines
    filename = 'Top8Decks/RawData/'+ missing0s(tourNumber)+str(tourNumber) + '/Deck ('+str(DeckNumber)+").txt"
	if verbose: print 'Opening '+filename
	
	with open(filename, "r") as ins:
    array = []
    for line in ins:
        array.append(line)
		
	
	#removeCarriageReturn(lines)
	
	return lines
	#if verbose: print 'File not found.'
	#return None
    
def main(argv):
    if len(argv) > 1:
        if argv[1] == '-v': verbose = True
    priceList = parseIntoPriceOnlyList(cardNumber)
    
    if priceList == None: 
        print "file not found."
        exit(1)
    print priceList
    
if __name__ == '__main__':
    main(sys.argv)