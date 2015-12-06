
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
from sklearn import preprocessing




currenttime = 1446879000000;
    
def constructTrainingMatrix(startNumber,endNumber, labelGap, convertToSparse=False):
    listOfTrainingVectors=[]
    yVector=[]
    cardsUsed=[]
    #numDays=0
    #parse JSON data
    for x in xrange(startNumber, endNumber+1):
        priceVector=DataUtils.parseIntoPriceOnlyList(x)
        # card attributes vector=Utils.parseIntoAttributeList(x,parsedData)
        if not priceVector==None:
            if priceVector[-1]<100:
                continue
            #print 'var numDays=' + str(numDays)
            #print 'num Days for this one is '+ str(len(priceVector))
            #if numDays == 0:
            #    numDays=len(priceVector)
                #print 'updated numDays to ' +str(numDays)
            #elif not numDays==len(priceVector): 
            #    print 'day lengths not equal, sad times'
            #    return None
            cardsUsed.append(x)
            yVector.append(priceVector[-1])
            #trainingVec=pricVec+AttribVec
            listOfTrainingVectors.append(priceVector[0:-labelGap])
            #print 'traing vector was'+str(priceVector)+'; list is now:' + str(listOfpriceVectors)
    #numVectors=len(listOfpriceVectors)
    #listOfpriceVectors=[array(trainingVec) for trainingVec in listOfpriceVectors] #converts each vector to array form for next step; might change order, shouldn't matter
    #trainingMatrix=np.zeroes((numVectors,numDays), np.int16)
    trainingMatrix=np.matrix(listOfTrainingVectors, dtype=float)
    print 'using card numbers' + str(cardsUsed)
    #print 'trainingMatrix is ' 
    #print trainingMatrix
    #print 'y Vector is '
    #print yVector
    return (trainingMatrix,yVector)
    
def trainEstimator(X, y,):
    (X_train,X_test,y_train,y_test)=cv.train_test_split(X,y,test_size=0.4, random_state=0)
    #if verbose:
    #    print 'size of whole example matrix \t' + str(X.shape) 
    #    print 'size of whole output vector \t' + str((np.array(y)).shape)
    #    print 'size of training example matrix ' + str(X_train.shape)
    #    print 'size of training output vector \t' + str((np.array(y_train)).shape)
    #    print 'size of test example matrix \t' + str(X_test.shape)
    #    print 'size of test output vector \t' + str((np.array(y_test)).shape)
    #svr= svm.SVR(kernel='rbf', C=1e3, gamma=0.1)
    svr = svm.SVR(kernel='linear', C=10)
    #svr = svm.SVR(kernel='poly', C=1e3, degree=2)
    svr= svr.fit(X_train, y_train)
    y_pred = svr.predict(X_test)
    #print 'y values for the test set ' + str(y_test)
    #print 'predicted y for test set using svr is ' + str(y_pred) 
    score=svr.score(X_test,y_test)
    
    #svr_poly= svr_poly.fit(X, y)
   
        


def main(argv):
    # 1st arg: starting cardnumber, mandatory
    # 2nd arg: ending cardnumber, mandatory
    # 3rd arg: number of days ahead we're trying to predict, optional
    # 4th arg: whether verbose
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
    
    (X,y)=constructTrainingMatrix(startNumber, endNumber, labelGap)
    
    scaler=preprocessing.StandardScaler().fit(X)
    X_scaled=scaler.transform(X)
    
    #X_scaled=preprocessing.scale(X)
    if verbose:
        print scaler
        print scaler.mean_
        print 'the mean of the scaled data is ' + str(X_scaled.mean(axis=0))
        print 'the std of the scaled data is ' + str(X_scaled.std(axis=0))
        print 'here is the data'+ str(X)
        print 'here is the scaled data'+ str(X_scaled)
    #X is a matrix with n_examples rows and n_days columns, y is a n_examples long vector of what the prices were labelGap days in the future
    
    #score=trainEstimator(X,y)
    #print 'labelGap:score without scaling \n' + str(labelGap)+ ':'+str(score)
    (X_train,X_test,y_train,y_test)=cv.train_test_split(X_scaled,y,test_size=0.4, random_state=0)
    #if verbose:
    #    print 'size of whole example matrix \t' + str(X.shape) 
    #    print 'size of whole output vector \t' + str((np.array(y)).shape)
    #    print 'size of training example matrix ' + str(X_train.shape)
    #    print 'size of training output vector \t' + str((np.array(y_train)).shape)
    #    print 'size of test example matrix \t' + str(X_test.shape)
    #    print 'size of test output vector \t' + str((np.array(y_test)).shape)
    #svr= svm.SVR(kernel='rbf', C=1e3, gamma=0.1)
    svr = svm.SVR(kernel='linear', C=10)
    #svr = svm.SVR(kernel='poly', C=1e3, degree=2)
    svr= svr.fit(X_train, y_train)
    y_pred = svr.predict(X_test)
    #print 'y values for the test set ' + str(y_test)
    #print 'predicted y for test set using svr is ' + str(y_pred) 
    score=svr.score(X_test,y_test)
    
    #svr_poly= svr_poly.fit(X, y)
    print 'labelGap:score with scaling \n' + str(labelGap)+ ':'+str(score)
    
    
    
    
if __name__ == '__main__':
    main(sys.argv)