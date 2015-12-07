import sys
import DataUtils as DUtils
import DatabaseDownloadTools.JSONUtils as JUtils
import DatabaseDownloadTools.TopDecksUtils as TDUtils
import os
try:
    os.chdir('C:\Users\Emily\Documents\GitHub\CS229MTG')
except:pass

verbose = False

def getEntireVector(cardNumber, useRelevant, JSONCardDict, TopDeckDict):
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
    
    retVector = priceVector + JSONDescriptionVector + topDeckVector
    
    return retVector
    
def getJSONDescriptionDictionary():
    return JUtils.parseJsonIntoCardsDictionary()

def getTopDeckDictionary():
    return TDUtils.parseTopDecksIntoReadableData()


"""
CODE BELOW HERE IS IRRELEVANT TO CALLER 
"""



def getPriceVector(cardNumber,useRelevant):
    return DUtils.parseIntoPriceOnlyList(cardNumber,useRelevant)

def getJSONDescriptionVector(cardNumber, JSONCardDict, useRelevant):
    return JUtils.retrieveCardDataIntoVector(cardNumber, JSONCardDict, useRelevant)
    
def getTopDeckVector(cardNumber, TopDeckDict, useRelevant):
    return TDUtils.retrieveCardDataIntoVector(cardNumber, TopDeckDict, useRelevant)

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
    
    JSONCardDict = getJSONDescriptionDictionary()
    TopDeckDict= getTopDeckDictionary()
    
    vector = getEntireVector(inputCardNumber, False, JSONCardDict, TopDeckDict)
    if vector == None: 
        print 'Error retrieving card!'
        exit(1)
    print 'Vector created.'
    print vector
    
if __name__ == '__main__':
    main(sys.argv)