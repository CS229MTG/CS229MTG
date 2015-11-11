
import sys
import os
import urllib2
import string
import datetime
from bs4 import BeautifulSoup
from multiprocessing import Pool
import threading

numCardsToTry = -5
numThreads = 20
lock = threading.Lock()
verbose = False

def downloadSinglePage404(cardNumber):
	#missing 0's:
	missing0s = ''
	for x in xrange(1,6-len(cardNumber)):
		missing0s += '0'
	
	#download the card html/data, parse
	url = 'http://www.mtgstocks.com/cards/'+ missing0s + cardNumber
	if verbose: print 'Downloading from ' + url+'...'
	try: 
		response = urllib2.urlopen(url)
	except: 
		print 'OH NOES PAGE NOT FOUND :' + str(cardNumber)
		return
	html = response.read()
	soup = BeautifulSoup(html, 'html.parser')
	
	#search the html for 404 error
	setsoup = str(soup)
	indy = string.rfind(setsoup, '404 - File Not Found')
	if indy == -1: #not a 404! 
		with lock:
			f = open('failuresTrue.txt','a')
			f.write(str(cardNumber)+'\n')
			f.close()
	else:
		with lock2:
			f = open('failures404.txt','a')
			f.write(str(cardNumber)+'\n')
			f.close()
	
def main(argv):
	#handle inputs: enter a number 1-27482 to get that card.
	#error: no inputs
	if len(argv) < 2:
		print >> sys.stderr, 'Usage: enter a file with card numbers.'
		sys.exit(1)
	verbose = False
	if len(argv) > 2:
		if argv[2] == '-v': verbose = True
	failuresFile = argv[1]
	
	#get the lines
	cardNumbers = []
	with open(failuresFile) as f:
		content = f.readlines()
		x=0
		for line in content:
			if numCardsToTry > 0:
				if x > numCardsToTry: break
				x = x+1
			cardNumbers.append(line)
	
	p = Pool(numThreads)
	p.map(downloadSinglePage404, cardNumbers)
	
if __name__ == '__main__':
	main(sys.argv)