
#import DatabaseDownloadTools.JSONUtils
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np



def algor1(input1,input2,input3,input4,input5,input6):
    ret = []
    for x in input1:
        ret.append(2)
    return ret
    
def algor2(input1,input2,input3,input4,input5,input6):
    ret = []
    for x in input1:
        ret.append(4)
    return ret
    

funcdict = {
  'algor1': algor1,
  'algor2': algor2
}

def plotAlgorithmOutpus():    
    xaxis  = []
    for x in range(1,29):
        xaxis.append(x)
        
    listToPlot1 = funcdict['algor1'](xaxis,0,0,0,0,0)
    listToPlot2 = funcdict['algor2'](xaxis,0,0,0,0,0)

    
    
    plt.plot(xaxis,listToPlot1,'bs')
    plt.plot(xaxis,listToPlot2,'g^')
    plt.ylabel('some numbers')
    plt.show()

def main(argv):
    plotAlgorithmOutpus()
        
    print 'Done!'
if __name__ == '__main__':
    main(sys.argv)