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
import threading

startCard = 1
incrementCard = 1
endCard = 27482
numThreads = 20
thisverbose = True
lock = threading.Lock()

countDownLock = threading.Lock()

def callDownloadSinglePage(cardNumber):
    try:
        DownloadSinglePage.downloadSinglePage(str(cardNumber), False)
        with countDownLock:
            if thisverbose: print 'Got card number ' + str(cardNumber)
            #cardsLeft = cardsLeft - 1
    except:
        with lock:
            print 'FAILURE!!!! CARD NUMBER ' + str(cardNumber)
            f = open('FAILURES.txt','a')
            f.write(str(cardNumber)+'\n')
            f.close()

def main(argv):
    #indicate start
    print "Beginning download of every "+str(incrementCard)+'-th card'
    print 'in the range' +str(startCard)+'-'+str(endCard)
    
    #generate list of cards to spit out
    f = open('failuresTrue.txt', 'r')
    cardList = f.readlines()
    #x = startCard
    #while x<=endCard:
    #   cardList.append(x)
    #   x+=incrementCard
        
    #empty the failure file 
    f = open('FAILURES.txt','a')
    f.truncate()
    f.close()
    
    #thread operation
    p = Pool(numThreads)
    p.map(callDownloadSinglePage, cardList)
    
    
    print 'Done!'
    
if __name__ == '__main__':
    main(sys.argv)