
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
from .. import DataUtils

startCard=1
endCard=30000

def extractSetNames():
	#get the lines
	filename = 'CS229MTG/DatabaseDownloadTools/Sets.txt'
	try:
		with open(filename, 'r') as f:
			lines = f.readlines()
	except:
		print 'Must run ExtractSetStrings.py first.'
		exit(1)
	
	#extract
	justnames = []
	for line in lines:
		justnames.append(line.split('|')[0])
	filename = 'CS229MTG/DatabaseDownloadTools/SetNames.txt'
	with open(filename, 'w') as f:
		f.truncate()
		for line in justnames:
			f.write(line+'\n')
	

def main(argv):
	print 'Beginning to extract set names from sets...'
	
	extractSetNames()
	
	print 'Done!'
	
	
if __name__ == '__main__':
	main(sys.argv)
	
	