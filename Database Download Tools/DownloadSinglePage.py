
"""
FILE: DownloadSinglePage.py
------------------
Author: Emily Franklin

This is my attempt to download the data from 1 page. 
"""

import sys
import os
import urllib2
import string
import datetime
from bs4 import BeautifulSoup

currenttime = 1446879000000;#Yea yea yea I know it's dumb. So what.

def convertUnixTimeToHuman(str):
	ans = (
		datetime.datetime.fromtimestamp(
			(int(str)/1000)
		).strftime('%Y-%m-%d %H:%M:%S')
	)
	return ans

def downloadSinglePage(cardNumber, verbose):
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
	if verbose: print 'Successfully downloaded ' + cardName+'!'
	
	#trim down html into 1 block of data (a string) to parse
	if verbose: print 'Parsing data...'
	dataBlock = str(soup.find(id="financial"))
	startIndex = string.find(dataBlock,'Average')+21
	dataBlock = dataBlock[startIndex:]
	endIndex = string.find(dataBlock,'id') - 5
	dataBlock = dataBlock[:endIndex]
	
	#parse the data
	dataList = dataBlock.split(' ],[ ')
	if verbose: print 'Downloaded html parsed into '+ str(len(dataList))+' data points.'
	if verbose: print 'Parsing data points...'
	dataMap = {}
	for item in dataList:
		commaloc = string.find(item,',')
		key = str(item[:commaloc])
		val = str(item[commaloc+1:])
		decimalPlace = string.find(val, '.')
		if len(val)-decimalPlace < 3: 
			if verbose: print '\tPrice missing digit:'+ str(key) + '('+convertUnixTimeToHuman(key)+'), was'+str(val)
			val = val + '0'
		val = val.replace('.','')
		val = val.lstrip('0')
		if key in dataMap.keys():
			if verbose: print '\tDuplicate! '+ key + '('+convertUnixTimeToHuman(key)+') was '+dataMap[key] +' and is now '+val
		dataMap[key] = val
	if verbose: print 'Discovered '+str(len(dataMap)) + ' data points to be saved.'
	
	#save locally, putting in nulls where needed
	filename = 'CardData' + str(cardNumber)+'.txt'
	try: #delete if exists
		os.remove(filename)
	except OSError:
		pass
	f = open(filename,'w')
	f.write(cardName+'\n')
	entriesCount = 0;
	dataEntriesCount = 0;
	datetime = 1339286400000
	while datetime < currenttime:
		if not str(datetime) in dataMap.keys():
			if verbose: print '\tPrice for ' +str(datetime)+'('+convertUnixTimeToHuman(str(datetime))+') not in data!'
			f.write(str(datetime)+',-1\n')
		else:
			f.write(str(datetime)+','+dataMap[str(datetime)]+'\n')
			dataEntriesCount+=1
		datetime+=86400000
		entriesCount+=1
	f.close()
	if verbose: print 'Lines in file: ' +str(entriesCount)+'+1(cardname)'
	if verbose: print 'Actual data in file: '+str(dataEntriesCount)+' data points'
	
	#end message
	if verbose: print 'Successfully processed:' + cardName

def main(argv):
	#handle inputs: enter a number 1-27482 to get that card.
	#error: no inputs
	if len(argv) < 3:
		print >> sys.stderr, 'Usage: enter a number 1-27482. Put -v at the end for verbose.'
		sys.exit(1)
	verbose = False
	if len(argv) > 2:
		if argv[2] == '-v': verbose = True
	cardNumber = argv[1]
	print downloadSinglePage(cardNumber, verbose)
	
if __name__ == '__main__':
	main(sys.argv)