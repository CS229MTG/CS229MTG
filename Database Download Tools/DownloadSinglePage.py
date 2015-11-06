
"""
FILE: DownloadSinglePage.py
------------------
Author: Emily Franklin

This is my attempt to download the data from 1 page. 
"""

import sys
import urllib2
import string
from bs4 import BeautifulSoup

def main(argv):
	#handle inputs: enter a number 1-27482 to get that card.
	if len(argv) < 2:
		print >> sys.stderr, 'Usage: enter a number 1-27482 to get a card in SQL.'
		sys.exit(1)
	verbose = False
	if len(argv) > 2:
		if argv[2] == '-v': verbose = True
	cardNumber = argv[1]
	#missing 0's:
	missing0s = ''
	for x in xrange(1,6-len(cardNumber)):
		missing0s += '0'
	
	#download the card html/data, parse
	url = 'http://www.mtgstocks.com/cards/'+ missing0s + cardNumber
	if verbose: print 'Downloading from ' + url+'...'
	response = urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html, 'html.parser')
	cardName = str(soup.title)[7:-24]
	if verbose: print 'Successfully downloaded ' + cardName+'! Parsing data...'
	
	#trim down html into 1 block of data (a string) to parse
	dataBlock = str(soup.find(id="financial"))
	startIndex = string.find(dataBlock,'Average')+21
	dataBlock = dataBlock[startIndex:]
	endIndex = string.find(dataBlock,'id') - 5
	dataBlock = dataBlock[:endIndex]
	
	#parse the data
	dataList = dataBlock.split(' ],[ ')
	if verbose: print dataList[0]
	if verbose: print dataList[1]
	
	#1339286400000 is the first day
	
	if verbose: print 'Successfully processed:' + cardName
	
if __name__ == '__main__':
	main(sys.argv)