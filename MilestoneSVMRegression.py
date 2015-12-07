
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
import VectorUtils
import numpy as np
from sklearn import svm
from sklearn import cross_validation as cv
from sklearn import metrics 
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn import pipeline
from sklearn import grid_search


lastDay = 1245
currenttime = 1446879000000;
    
def constructTrainingMatrix(startNumber,endNumber, labelGap, convertToSparse=False):
    listOfTrainingVectors=[]
    yVector=[]
    cardsUsed=[]
    #numDays=0
    #parse JSON data
    for x in xrange(startNumber, endNumber+1):
        priceVector=VectorUtils.getEntireVector(x, True)
        # card attributes vector=Utils.parseIntoAttributeList(x,parsedData)
        if not priceVector==None:
            #print 'var numDays=' + str(numDays)
            #print 'num Days for this one is '+ str(len(priceVector))
            #if numDays == 0:
            #    numDays=len(priceVector)
                #print 'updated numDays to ' +str(numDays)
            #elif not numDays==len(priceVector): 
            #    print 'day lengths not equal, sad times'
            #    return None
            cardsUsed.append(x)
            yVector.append(priceVector[lastDay])
            #trainingVec=pricVec+AttribVec
            listOfTrainingVectors.append(priceVector[0:-labelGap])
            #print 'traing vector was'+str(priceVector)+'; list is now:' + str(listOfpriceVectors)
    #numVectors=len(listOfpriceVectors)
    #listOfpriceVectors=[array(trainingVec) for trainingVec in listOfpriceVectors] #converts each vector to array form for next step; might change order, shouldn't matter
    #trainingMatrix=np.zeroes((numVectors,numDays), np.int16)
    trainingMatrix=np.matrix(listOfTrainingVectors, dtype=float)
    #print 'using card numbers' + str(cardsUsed)
    #print 'trainingMatrix is ' 
    #print trainingMatrix
    #print 'y Vector is '
    #print yVector
    return (trainingMatrix,yVector)

def SVMRegression(startNumber,endNumber,labelGap,verbose):
    (X,y)=constructTrainingMatrix(startNumber, endNumber, labelGap)
    #X is a matrix with n_examples rows and n_days columns, y is a n_examples long vector of what the prices were labelGap days in the future
    X_train, X_test, y_train, y_test =cv.train_test_split(
    X, y, test_size=0.3, random_state=0)
    
    #XVar_test, yVar_test=filterLargeDeltaCards(X_test,y_test)
    
    scaler=preprocessing.StandardScaler()
    pca=PCA(n_components=10) 
    svr=svm.SVR(kernel='linear', C=100)
    #pipe=pipeline.Pipeline([("scaler",scaler),("pca", pca)("svr",svr)]) # this version of the pipeline applies PCA
    pipe=pipeline.Pipeline([("scaler",scaler),("svr",svr)]) #this one does not 
    # this "pipeline" is an object which combines the tasks of scaling the data, running PCA, and then doing a Support Vector Regression
    # that allows us to automate parameter tuning  via Cross Validation in a fairly painless manner
    # the parameters for the pipeline are: n_components, C, epsilon, kernel, degree (poly kernel only), and gamma (rbf only)
    #param_grid=[{'svr__kernel': ['linear'], 'svr__C': [10, 80, 200]}
                    #,{'svr__kernel': ['poly'], 'svr__degree': [2,3,4],
                    #'svr__C': [.1,1, 10, 100]}
    #               ]
    param_grid=[{'svr__kernel': ['linear'], 'svr__C': [100]}
                    #,{'svr__kernel': ['poly'], 'svr__degree': [2,3,4],
                    #'svr__C': [.1,1, 10, 100]}
                    ]
                                    
    tunedPipe=grid_search.GridSearchCV(pipe, param_grid, cv=7)
    tunedPipe.fit(X_train,y_train)
    print("Best parameters set found on development set:")
    print()
    print(tunedPipe.best_params_)
    print()
    print("Grid scores on development set:")
    print()
    for params, mean_score, scores in tunedPipe.grid_scores_:
        print("%0.3f (+/-%0.03f) for %r"
              % (mean_score, scores.std() * 2, params))
    print()

    print("Detailed classification report:")
    print()
    print("The model is trained on the full development set.")
    print("The scores are computed on the full evaluation set.")
    print()
    tunedScore=tunedPipe.score(X_test,y_test)
    #jace_data=DataUtils.parseIntoPriceOnlyList(27037, True)
    #jace_data=jace_data[28:]
    #jace_pred=tunedPipe.predict(jace_data)
    #print 'predicted price for Jace' + str(jace_pred)
    print 'score on test set was ' + str(tunedScore)
    print()
    
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
    SVMRegression(startNumber,endNumber,labelGap,verbose)
    
if __name__ == '__main__':
    main(sys.argv)