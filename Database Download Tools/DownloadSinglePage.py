
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

def downloadSinglePage(cardNumber, numberDays, verbose):
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
	dataList.reverse()
	justPricesDatalist = []
	for x in range(0,numberDays-1):
		if x < len(dataList):
			val = str(dataList[x][string.find(dataList[x],',')+1:])
			val = val.replace('.','')
			val = val.lstrip('0')
			justPricesDatalist.append(val)
		else:
			justPricesDatalist.append("null")
	justPricesDatalist.reverse()
	
	printstmt = '(' + cardName + ','
	for x in range(0,numberDays-1):
		printstmt = printstmt + justPricesDatalist[x]+','
	printstmt = printstmt[:-2] #remove last comma
	printstmt = printstmt + ')'
	
	#end message
	if verbose: print 'Successfully processed:' + cardName
	return printstmt

def main(argv):
	#handle inputs: enter a number 1-27482 to get that card.
	#error: no inputs
	if len(argv) < 3:
		print >> sys.stderr, 'Usage: enter a number 1-27482 and the number of days to go back to get a card in SQL. Put -v at the end for verbose.'
		sys.exit(1)
	numberDays = int(argv[2])
	verbose = False
	if len(argv) > 3:
		if argv[3] == '-v': verbose = True
	cardNumber = argv[1]
	print downloadSinglePage(cardNumber, numberDays, verbose)
	
if __name__ == '__main__':
	main(sys.argv)