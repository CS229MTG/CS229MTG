import sys
if __name__ == '__main__': import VectorUtils as VU
import os

#=====================================
#  Call-Functions
#=====================================

def pullVectorsFromIndex():
    ret = {} #dict: card#->vector
    
    with open('vectorIndex.txt','r') as f:
        lines = f.readlines()
    
    for line in lines:
        if line == '\n': continue
        parts = line.strip().split('|')
        ret[parts[0]]= parts[1:]
        
    return ret
 
pricePart = 1246
JSONPart = 214
TopDeckPart = 60
SetNamePart = 145
 
def extractPriceComponent(vector):
    return vector[0:pricePart]
        
def extractJSONDescriptionComponent(vector):
    return vector[pricePart:pricePart+JSONPart]
        
def extractTopDeckComponent(vector):
    return vector[pricePart+JSONPart:pricePart+JSONPart+TopDeckPart]
        
def extractSetNameComponent(vector):
    return vector[pricePart+JSONPart+TopDeckPart:pricePart+JSONPart+TopDeckPart+SetNamePart]




#=====================================
#  CommandLine Functions
#=====================================


def writeVectorToFile(x,v,f):
    f.write(str(x))
    for e in v:
        f.write('|')
        f.write(str(e))

def makeIndex(useRelevant):
    filename = 'vectorIndex.txt'
    with open('vectorIndex.txt','w') as f:
        f.truncate()
        for x in range(0, 30000):
            if x%500 == 0: print 'Finished writing '+str(x)+' vectors...'
            v = VU.getEntireVector(x, useRelevant)
            if v != None:
                writeVectorToFile(x,v,f)
                f.write('\n')
        
    
def printUsage():
    print 'Usage: Call this with python and any of the following arguments:'
    print '\t--generate\t Create vector index.'
    print '\t--irrelevant\t Use the entire index, not just relevant.'
    exit(1);

def main(argv):
    if len(argv) < 2:
        printUsage()
    used = False
    if '--generate' in argv:
        used = True
        if '--irrelevant' in argv:
            makeIndex(False)
        else:
            makeIndex(True)
        
    if not used:
        printUsage()
    
if __name__ == '__main__':
    main(sys.argv)