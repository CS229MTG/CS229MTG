
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

currenttime = 1446879000000;
verbose = False


def convertUnixTimeToHuman(str):
    ans = (
        datetime.datetime.fromtimestamp(
            (int(str)/1000)
        ).strftime('%Y-%m-%d %H:%M:%S')
    )
    return ans
    
def missing0s(cardNumber):
    m0s = ''
    for x in xrange(1,6-len(cardNumber)):
        m0s += '0'
    return m0s
    

def removeCarriageReturn(list):
    for idx, line in enumerate(list):
        list[idx] = line[:-1]
    
def parseIntoHeaderDatePriceList(cardNumber):
    cardNumber = str(cardNumber)
    #missing 0's:
    mm0s = missing0s(cardNumber)
    
    #open the file, get the lines
    filename = 'DatabaseDownloadTools/cardPriceData/CardData'+ mm0s + cardNumber+".txt"
    try:
        f = open(filename,'r')
        lines = f.readlines(28000)
        removeCarriageReturn(lines)
        f.close()
        
        return lines
    except:
        if verbose: print 'File not found.'
        return None

def removeHeader(list):
    header = [list[0],list[1]]
    del list[0]
    del list[0]
    return header
    
def parseIntoPriceOnlyList(cardNumber):
    list = parseIntoHeaderDatePriceList(cardNumber)
    if list == None: return None
    
    removeHeader(list)
    
    priceList = []
    for x, line in enumerate(list):
        priceStr = line.split(',')[1]
        if priceStr=='': priceStr='-1'
        if priceStr=='-1':priceStr='0'
        priceList.append(int(priceStr))
    
    return priceList
    
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Do not run this from the command prompt unless testing. '
        sys.exit(1)
    if len(argv) > 2:
        if argv[2] == '-v': verbose = True
    cardNumber = argv[1]
    priceList = parseIntoPriceOnlyList(cardNumber)
    
    if priceList == None: 
        print "file not found."
        exit(1)
    print priceList
    
if __name__ == '__main__':
    main(sys.argv)