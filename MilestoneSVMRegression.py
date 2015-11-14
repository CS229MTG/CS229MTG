
"""
FILE: MilestoneSVMRegression.py
------------------
Author: Cooper Frye

takes 2 arguments, a starting and ending card number to train the model on
"""

import sys
import os
import string
import datetime
import DataUtils
import numpy as np
import sklearn.svm


currenttime = 1446879000000;
    
def constructTrainingMatrix(startNumber,endNumber, convertToSparse=False):
    listOfTrainingVectors=[]
    yVector=[]
    numDays=0
    for x in xrange(startNumber, endNumber+1):
        trainingVector=DataUtils.parseIntoPriceOnlyList(x)
        if trainingVector is not None:
            #print 'var numDays=' + str(numDays)
            #print 'num Days for this one is '+ str(len(trainingVector))
            if numDays is 0:
                numDays=len(trainingVector)
                #print 'updated numDays to ' +str(numDays)
            elif not numDays==len(trainingVector): 
                print 'day lengths not equal, sad times'
                return None
            yVector.append(trainingVector[-1])
            listOfTrainingVectors.append(trainingVector[0:-1])
            #print 'traing vector was'+str(trainingVector)+'; list is now:' + str(listOfTrainingVectors)
    #numVectors=len(listOfTrainingVectors)
    #listOfTrainingVectors=[array(trainingVec) for trainingVec in listOfTrainingVectors] #converts each vector to array form for next step; might change order, shouldn't matter
    #trainingMatrix=np.zeroes((numVectors,numDays), np.int16)
    #trainingMatrix=np.matrix(listOfTrainingVectors)
    #print 'trainingMatrix is ' 
    #print trainingMatrix
    #print 'y Vector is '
    #print yVector
    return (trainingMatrix,yVector)
        


def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Do not run this from the command prompt unless testing. '
        sys.exit(1)
    if len(argv) > 3:
        print "fewer args please"
        exit(1)
    startNumber = int(argv[1])
    endNumber=int(argv[2])
    #for x in xrange(startNumber, endNumber+1):
    #   print str(x) #basic testing
    (trainingMatrix,yVector)=constructTrainingMatrix(startNumber, endNumber)
    
    
    
    
    
if __name__ == '__main__':
    main(sys.argv)