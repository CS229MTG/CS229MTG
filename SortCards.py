
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
import shutil
import DataUtils

startCard=27482
endCard=30000

def getFileNameFromCardNumber(c, src):
	cardNumber = str(c)
	#missing 0's:
	mm0s = DataUtils.missing0s(cardNumber)
	
	#open the file, get the lines
	filename = ''
	filename += 'DatabaseDownloadTools/'
	if src:
		filename += 'cardPriceData'
	else:
		filename += 'RelevantCardPriceData'
	filename += '/CardData'+ mm0s + cardNumber+".txt"
	return filename

def copyFileIfRelevant(cardNumber):
	#get the prices
	priceList = DataUtils.parseIntoPriceOnlyList(cardNumber, False)
	if priceList == None:
		return 0
		
	#if it's greater than 1 dollar
	curPrice = priceList[len(priceList)-1]
	if curPrice >= 100:
		shutil.copyfile(getFileNameFromCardNumber(cardNumber, True), getFileNameFromCardNumber(cardNumber, False))
		return 1
	else: return 0

def main(argv):
	print 'Beginning to sort cards...'
	numRelevant = 0
	for x in range(startCard,endCard):
		if x%500==0: print 'Sorted ' + str(x) + '...'
		numRelevant += copyFileIfRelevant(x)
	
	print 'Copied over ' + str(numRelevant)+' files. Done!'
	
	
if __name__ == '__main__':
	main(sys.argv)
	
	