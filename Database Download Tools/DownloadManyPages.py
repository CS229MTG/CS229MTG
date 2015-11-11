"""
FILE: DownloadSinglePage.py
------------------
Author: Emily Franklin

This is my attempt to download the data from 1 page. 
"""

import sys
import os
import DownloadSinglePage
from multiprocessing import Pool

startCard = 1
incrementCard = 1000
endCard = 27482
numThreads = 12
thisverbose = True

def callDownloadSinglePage(cardNumber):
	DownloadSinglePage.downloadSinglePage(str(cardNumber), False)
	if thisverbose: print 'Got card number ' + str(cardNumber)

def main(argv):
	#indicate start
	print "Beginning download of every "+str(incrementCard)+'-th card'
	print 'in the range' +str(startCard)+'-'+str(endCard)
	
	#generate list of cards to spit out
	cardList = []
	x = startCard
	while x<=endCard:
		cardList.append(x)
		x+=incrementCard
	
	#thread operation
	p = Pool(numThreads)
	p.map(callDownloadSinglePage, cardList)
	
	
	print 'Done!'
	
if __name__ == '__main__':
	main(sys.argv)