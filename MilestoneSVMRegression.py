
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
    
def constructTrainingMatrix(startNumber,endNumber, labelGap, convertToSparse=False):
    listOfTrainingVectors=[]
    yVector=[]
    numDays=0
    for x in xrange(startNumber, endNumber+1):
        trainingVector=DataUtils.parseIntoPriceOnlyList(x)
        if not trainingVector==None:
            if trainingVector[-1]<100:
                continue
            #print 'var numDays=' + str(numDays)
            #print 'num Days for this one is '+ str(len(trainingVector))
            if numDays == 0:
                numDays=len(trainingVector)
                #print 'updated numDays to ' +str(numDays)
            elif not numDays==len(trainingVector): 
                print 'day lengths not equal, sad times'
                return None
            yVector.append(trainingVector[-1])
            listOfTrainingVectors.append(trainingVector[0:-labelGap])
            #print 'traing vector was'+str(trainingVector)+'; list is now:' + str(listOfTrainingVectors)
    #numVectors=len(listOfTrainingVectors)
    #listOfTrainingVectors=[array(trainingVec) for trainingVec in listOfTrainingVectors] #converts each vector to array form for next step; might change order, shouldn't matter
    #trainingMatrix=np.zeroes((numVectors,numDays), np.int16)
    trainingMatrix=np.matrix(listOfTrainingVectors)
    print 'trainingMatrix is ' 
    print trainingMatrix
    print 'y Vector is '
    print yVector
    return (trainingMatrix,yVector)
        


def main(argv):
    # 1st arg: starting cardnumber, mandatory
    # 2nd arg: ending cardnumber, mandatory
    # 3rd arg: number of days ahead we're trying to predict, optional
    labelGap=1
    if len(argv) < 2:
        print >> sys.stderr, 'Do not run this from the command prompt unless testing. '
        sys.exit(1)
    elif len(argv) < 3:
        print 'at least 2 args required'
        exit(1)
    elif len(argv)==4:
        labelGap=int(argv[3])
    elif len(argv) > 4:
        print "fewer args please"
        exit(1)
    startNumber = int(argv[1])
    endNumber=int(argv[2])
    #for x in xrange(startNumber, endNumber+1):
    #   print str(x) #basic testing
    (X,y)=constructTrainingMatrix(startNumber, endNumber, labelGap)
    #svr_rbf = sklearn.svm.SVR(kernel='rbf', C=1e3, gamma=0.1)
    svr_lin = sklearn.svm.SVR(kernel='linear', C=1e3)
    #svr_poly = sklearn.svm.SVR(kernel='poly', C=1e3, degree=2)
    #svr_rbf= svr_rbf.fit(X, y)
    svr_lin= svr_lin.fit(X, y)
    y_lin = svr_lin.predict(X)
    print 'predicted y using svr_lin is ' + str(y_lin) 
    #svr_poly= svr_poly.fit(X, y)
    
    
    
    
    
if __name__ == '__main__':
    main(sys.argv)