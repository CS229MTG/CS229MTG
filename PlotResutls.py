
#import DatabaseDownloadTools.JSONUtils
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
#from boto.ec2.elb import listener

startValue = 1
incrementValue = 1
endValue = 30

def algor1(xaxis):
    ret = []
    for x in xaxis:
        output = 2#SVMScore(x)
        ret.append(output)
    return ret
    
def algor2(xaxis):
    ret = []
    for x in xaxis:
        output = 4#SVMScore(x)
        ret.append(output)
    return ret
    

def savePlot(list,filename):
    filename = './Results/' + filename + '.txt'
    try: os.remove(filename)
    except: pass
    
    f = open(filename,'w')
    for x in list:
        f.write(str(x) + '\n')
    f.close()
    
def loadPlot(filename):
    filename = './Results/' + filename + '.txt'
    ret = []
    with open(filename,'r') as f:
        lines = f.readlines()
        for line in lines:
            ret.append(float(line))
    return ret 

funcdict = {
  'algor1': algor1,
  'algor2': algor2
}

def plotAlgorithmOutputs():    
    xaxis  = []
    x = startValue
    while x < endValue:
        xaxis.append(x)
        x += incrementValue
        
    listToPlot1 = funcdict['algor1'](xaxis)
    listToPlot2 = funcdict['algor2'](xaxis)

    savePlot(listToPlot1,'listToPlot1')
    listToPlot1 = loadPlot('listToPlot1')
    
    plt.plot(xaxis,listToPlot1,'bs')
    plt.plot(xaxis,listToPlot2,'g^')
    plt.ylabel('some numbers')
    
    print 'Displaying plot: close plot to finish script.'
    plt.show()

def main(argv):    
    print 'Beginning plot script...'
    
    plotAlgorithmOutputs()
        
    print 'Done!'
if __name__ == '__main__':
    main(sys.argv)