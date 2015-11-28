
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
from sklearn import svm
from sklearn import cross_validation as cv
from sklearn import metrics 



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
    #print 'trainingMatrix is ' 
    #print trainingMatrix
    #print 'y Vector is '
    #print yVector
    return (trainingMatrix,yVector)
        


def main(argv):
    # 1st arg: starting cardnumber, mandatory
    # 2nd arg: ending cardnumber, mandatory
    # 3rd arg: number of days ahead we're trying to predict, optional
    # 4th arg: 
    labelGap=1
    verbose=False 
    if len(argv) < 2:
        print >> sys.stderr, 'Do not run this from the command prompt unless testing. '
        sys.exit(1)
    if len(argv) < 3:
        print 'at least 2 args required'
        exit(1)
    if len(argv) >=4:
        labelGap=int(argv[3])
    if len(argv) >=5:
        verbose=True
    if len(argv) > 5:
        print "fewer args please"
        exit(1)
    startNumber = int(argv[1])
    endNumber=int(argv[2])
    #for x in xrange(startNumber, endNumber+1):
    #   print str(x) #basic testing
    (X,y)=constructTrainingMatrix(startNumber, endNumber, labelGap)
    #X is a matrix with n_examples rows and n_days columns, y is a n_examples long vector of what the prices were labelGap days in the future
    (X_train,X_test,y_train,y_test)=cv.train_test_split(X,y,test_size=0.4, random_state=0)
    if verbose:
        print 'size of whole example matrix \t' + str(X.shape) 
        print 'size of whole output vector \t' + str((np.array(y)).shape)
        print 'size of training example matrix ' + str(X_train.shape)
        print 'size of training output vector \t' + str((np.array(y_train)).shape)
        print 'size of test example matrix \t' + str(X_test.shape)
        print 'size of test output vector \t' + str((np.array(y_test)).shape)
    #svr= svm.SVR(kernel='rbf', C=1e3, gamma=0.1)
    svr = svm.SVR(kernel='linear', C=10)
    #svr = svm.SVR(kernel='poly', C=1e3, degree=2)
    svr= svr.fit(X_train, y_train)
    y_pred = svr.predict(X_test)
    #print 'y values for the test set ' + str(y_test)
    #print 'predicted y for test set using svr is ' + str(y_pred) 
    score=svr.score(X_test,y_test)
    print 'labelGap:score of estimator \n' + str(labelGap)+ ':'+str(score)
    #svr_poly= svr_poly.fit(X, y)
    
    
    
    
    
if __name__ == '__main__':
    main(sys.argv)