import sys
import DataUtils as DUtils
import DatabaseDownloadTools.JSONUtils as JUtils
import DatabaseDownloadTools.TopDecksUtils as TDUtils
import SetUtils as SUtils
import os
try:
    os.chdir('C:\Users\Emily\Documents\GitHub\CS229MTG')
except:pass

verbose = False


def getEntireVector(cardNumber, useRelevant):
    #price vector
    if verbose: print 'Getting price vector...'
    priceVector = getPriceVector(cardNumber, useRelevant)
    if priceVector == None: 
        if verbose: print 'Price Vector unattainable.'
        return None
    
    if verbose: print 'Getting JSON description vector...'
    JSONDescriptionVector = getJSONDescriptionVector(cardNumber, JSONCardDict, useRelevant)
    if JSONDescriptionVector == None: 
        if verbose: print 'JSON Description Vector unattainable.'
        return None
    
    if verbose: print 'Getting top deck vector...'
    topDeckVector = getTopDeckVector(cardNumber, TopDeckDict, useRelevant)
    if topDeckVector == None: 
        if verbose: print 'Top Deck Vector unattainable.'
        return None
    
    if verbose: print 'Getting set name vector...'
    setNameVector = getSetNameVector(cardNumber, useRelevant)
    if setNameVector == None: 
        if verbose: print 'Set Name Vector unattainable.'
        return None
    
    retVector = priceVector + JSONDescriptionVector + topDeckVector + setNameVector
    
    return retVector

def describeEntireVector(vector):
	return describeVector(vector, getEntireVectorDescriptor())

def describeVector(vector,descriptor):
	ret = ''
	
	if len(vector) != len(descriptor):
		return 'ERROR DESCRIBING VECTOR: descriptor different length!'
	
	for i, v in enumerate(vector):
		ret += '{:<40}'.format(str(descriptor[i])) +str(v)
		ret += '\n'
		
	return ret
"""
Price Vector length: 1246
JSON description length: 214
Top decks vector: 60
SetName vector: 145
CODE BELOW HERE IS IRRELEVANT TO CALLER 
"""




def getJSONDescriptionDictionary():
    return JUtils.parseJsonIntoCardsDictionary()

def getTopDeckDictionary():
    return TDUtils.parseTopDecksIntoReadableData()

TopDeckDict = getTopDeckDictionary()
JSONCardDict = getJSONDescriptionDictionary()

#Actual getting vectors

def getPriceVector(cardNumber,useRelevant):
    return DUtils.parseIntoPriceOnlyList(cardNumber,useRelevant)

def getJSONDescriptionVector(cardNumber, JSONCardDict, useRelevant):
    return JUtils.retrieveCardDataIntoVector(cardNumber, JSONCardDict, useRelevant)
    
def getTopDeckVector(cardNumber, TopDeckDict, useRelevant):
    return TDUtils.retrieveCardDataIntoVector(cardNumber, TopDeckDict, useRelevant)
	
def getSetNameVector(cardNumber, useRelevant):
    return SUtils.getSetNameVector(cardNumber, useRelevant)

	
#get descriptors

def getEntireVectorDescriptor():
	list = []
	list += getPriceVectorDescriptor()
	list += getJSONDescriptionVectorDescriptor()
	list += getTopDeckVectorDescriptor()
	list += getSetNameVectorDescriptor()
	return list

def getPriceVectorDescriptor():
	return DUtils.getPVD()

def getJSONDescriptionVectorDescriptor():
	return JUtils.totalVectorNames

def getTopDeckVectorDescriptor():
	return TDUtils.getTopDeckVectorDescriptor()

def getSetNameVectorDescriptor():
	return SUtils.setNamesVector

#testing and such
	
def printUsage():
    print 'Usage: Import this file. Otherwise, enter a number to see the vector produced. '
    exit(1);

def main(argv):
    if len(argv) < 2:
        printUsage()
    
    try:
        inputCardNumber = int(argv[1]) 
    except: 
        printUsage()
    
    print 'Attempting to create vector for '+str(inputCardNumber)+'...'
    
    vector = getEntireVector(inputCardNumber, False)
    if vector == None: 
        print 'Error retrieving card!'
        exit(1)
    print 'Vector created.'
    print describeEntireVector(vector)
    
if __name__ == '__main__':
    main(sys.argv)