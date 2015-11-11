"""
FILE: DownloadSinglePage.py
------------------
Author: Emily Franklin

Get the number of days, based on either a specified card or card 1.
"""

import sys
import urllib2
import string
from bs4 import BeautifulSoup

def getNumberOfDays(cardNumber,verbose):
#missing 0's:
	missing0s = ''
	for x in xrange(1,6-len(str(cardNumber))):
		missing0s += '0'
	
	#download the card html/data, parse
	url = 'http://www.mtgstocks.com/cards/'+ missing0s + str(cardNumber)
	if verbose: print 'Downloading from ' + url+' to get number of days...'
	response = urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html, 'html.parser')
	cardName = str(soup.title)[7:-24]
	if verbose: print 'Successfully downloaded ' + cardName+'! Parsing data to get number of days...'
	
	#trim down html into 1 block of data (a string) to parse
	dataBlock = str(soup.find(id="financial"))
	startIndex = string.find(dataBlock,'Average')+21
	dataBlock = dataBlock[startIndex:]
	endIndex = string.find(dataBlock,'id') - 5
	dataBlock = dataBlock[:endIndex]
	if verbose: print 'First bit: ' + dataBlock[0]
	if verbose: print 'Next bit:  ' + dataBlock[1]
	if verbose: print 'Last bit:  ' + dataBlock[len(dataBlock)-2]
	if verbose: print 'Last bit:  ' + dataBlock[len(dataBlock)-1]
	
	#parse the data
	dataList = dataBlock.split(' ],[ ')
	if verbose: print 'First item: ' + dataList[0]
	if verbose: print 'Next item:  ' + dataList[1]
	if verbose: print 'Last item:  ' + dataList[len(dataList)-1]
	for x in range(0,len(dataList)):
		dataList[x] = dataList[x][:string.find(dataList[x],',')]
	if verbose: print 'First item: ' + dataList[0]
	if verbose: print 'Next item:  ' + dataList[1]
	if verbose: print 'Last item:  ' + dataList[len(dataList)-1]
	
	
	
	#1339286400000 is the first day
	
	#end message
	if verbose: print 'Successfully got number of days using ' + cardName
	
	#return length
	return len(dataList)

def main(argv):
	#handle inputs: verbose for debug.
	verbose = False
	cardNumber = 00001
	if len(argv) == 2:
		if argv[1] == '-v': verbose = True
		else: cardNumber = argv[1]
	if len(argv) == 3:
		if argv[1] == '-v': 
			verbose = True
			cardNumber = argv[2]
	print getNumberOfDays(cardNumber,verbose)
	
if __name__ == '__main__':
	main(sys.argv)