#!/usr/bin/python
'''
plotData.py

Jared Moskowitz & Julia Rowe
05/07/15

This file contains code for creating two graphs. One is a histrogram
of the distances our labeled data (both signal and background) is from
the hyperplane (the defining weight vectors are at the top as global variables).
The second plot is the signal to noise ratio, which shows the significance of
the signal data we see.


USAGE: python plotData.py [SIGNAL_FILE_PATH] [BACKGROUND_FILE_PATH]

'''


import sys, io
from scipy.io.arff import loadarff
import scipy.spatial.distance as pyDistance
import random
import numpy as np
import pylab as plt
import math


#define bin sizes for histogram
bins = 100

#weight vectors - even machines 9 features
#mll                =     -13.5988
#mjj                =       2.9715
#met_phi_centrality =      -0.0794
#mt                 =     -12.3976
#DYjj               =       2.8055
#sumMlj             =       3.5845
#dphill             =      -1.1754
#contOLV            =      -1.1174
#ptTotal            =      -2.7679
#bias               =       -0.2625

#weight vetors - odd machines 9 features
#mll                = -12.6961
#mjj                = 2.9721
#met_phi_centrality = -0.3015
#mt                 = -10.3634
#DYjj               = 2.4768
#sumMlj             = 5.0838
#dphill             = -1.1921
#contOLV            = -1.1194
#ptTotal            = -4.3755
#bias               = -0.1084

#weight vectors - even machines 31 features
'''
MET                = -0.7428
MET_phi            =  0.0553
leadingLep_E       =  0.0854
leadingLep_px      =  0.193
leadingLep_pz      = -0.6703
subleadingLep_E    = -0.7327
subleadingLep_px   =  5.6579
subleadingLep_py   = -0.1106
subleadingLep_pz   =  0.6753
FW1                = -0.7999
FW2                = -0.028
FW3                = -0.2165
FW4                = -0.1318
FW5                =  0.4356
jet_et_total       =  1.2679
jet_energy_total   =  1.9876
jet_px             = -3.2809
jet_py             = -0.3206
jet_pz             =  0.1263
HT                 =  1.3328
EV2                =  0.1717
EV1                = -0.1017
mll                =-13.6651
mjj                =  2.0276
met_phi_centrality = -0.2628
mt                 =-10.276
DYjj               =  2.9932
sumMlj             = -0.6136
dphill             = -0.455
contOLV            = -0.9065
ptTotal            = -3.4452
bias               =  -0.3427
'''

#weight vectors - even machines 31 features

MET                = -0.2794 
MET_phi            = -0.0101 
leadingLep_E       = -0.1635 
leadingLep_px      =  0.473  
leadingLep_pz      = -0.3613 
subleadingLep_E    =  0.181  
subleadingLep_px   =  4.5234 
subleadingLep_py   = -0.0921 
subleadingLep_pz   =  0.1897 
FW1                = -0.8452 
FW2                =  0.089  
FW3                = -0.0922 
FW4                = -0.0913 
FW5                =  0.3698 
jet_et_total       =  0.822  
jet_energy_total   =  1.5511 
jet_px             = -3.3021 
jet_py             = -0.0634 
jet_pz             =  0.1501 
HT                 =  1.1329 
EV2                = -0.3154 
EV1                = -0.575  
mll                = -12.9512 
mjj                =  1.3728 
met_phi_centrality = -0.4484 
mt                 = -9.4879 
DYjj               =  3.259  
sumMlj             =  0.4025 
dphill             = -0.7328 
contOLV            = -0.8639 
ptTotal            = -3.3134 
bias               = -0.3737


def main():
        if len(sys.argv) < 2:
                print "Exception: Too few arguments"
                print "usage: python plotData.py [SIGNAL_FILE_PATH] [BACKGROUND_FILE_PATH]"
                exit(0)


        elif len(sys.argv) > 3:
                print "Exception: Too many arguments"
                print "usage: python plotData.py [SIGNAL_FILE_PATH] [BACKGROUND_FILE_PATH]"
                exit(0)

        else:
                #read in data
                signalData = read_arff(sys.argv[1])
                backgroundData = read_arff(sys.argv[2])

                #plot data
                plotData(signalData, backgroundData)

        exit(1)


'''
This plots two graphs. One is the distances our labeled data
(both signal and background) is from  the hyperplane (the defining weight
vectors are at the top as global variables). The second plot is the signal
to noise ratio, which shows the significance of the signal data we see.

'''
def plotData(signal, background):


        #obtain the distances from the hyperplane
        sigData = calculateDistances(signal)
        backData = calculateDistances(background)

        #plot histogram of distances from hyperplane
        myplt = plt.figure(1)
        plt1 = plt.subplot(211)
        plt1.set_ylabel('Frequency')
        signalHistInfo = plt.hist(sigData, bins, alpha=0.5, histtype='stepfilled', label='x')
        backgroundHistInfo = plt.hist(backData, bins, alpha=0.5, histtype='stepfilled', label='y')
        plt.axis([-2, 1, 0, 3000])

        plt.subplots_adjust(left=None, bottom=None, right=None, top=None,wspace=None, hspace=0.4)
        stackedHistBins, bin_edges, patches = plt.hist((sigData,backData), bins, alpha=0, label='x', histtype='barstacked')
        cutValues = getCutInfo(stackedHistBins)

        #plot significance graph
        plt2 = plt.subplot(212)
        plt2.set_ylabel('Signal / sqrt(background)')
        plt2.set_xlabel('Distance From SVM Hyperplane')

        bin_edges = np.delete(bin_edges, -1)
        plt.axis([-2, 1, 0, 55])
        plt.plot(bin_edges,cutValues)
        plt.savefig('slidePic.png')
        plt.show()


'''
For each data point in data, this function uses the weight vector
that defines the hyperplane in order to calculate each data point's distance
to the hyperplane.

output:
        list() - distances to hyperplane for each point
'''
def calculateDistances(data):

        x = list()
        newData = removeLabels(data)
        '''
        #for 9 features
        plane = (mll, mjj, met_phi_centrality, mt, DYjj, sumMlj, dphill,
                  contOLV, ptTotal)

        #for 31 features
        '''
        plane = (MET, MET_phi, leadingLep_E, leadingLep_px, leadingLep_pz,
                 subleadingLep_E, subleadingLep_px, subleadingLep_py,
                 subleadingLep_pz, FW1, FW2, FW3, FW4, FW5, jet_et_total,
                 jet_energy_total, jet_px, jet_py, jet_pz, HT, EV2, EV1, mll,
                 mjj, met_phi_centrality, mt, DYjj, sumMlj, dphill, contOLV,
                 ptTotal)
    

        for i in range(len(data)):
                v = np.array(plane)
                x.append(np.dot(newData[i], plane)/np.linalg.norm(v) - bias)

        return x

'''
Removes the unecsesary labels attached to the data read in.
'''
def removeLabels(data):
        newData = list()
        for point in data:
                newPoint = list()
                for i in range(0, (len(point) - 1)):
                        newPoint.append(point[i])
                newData.append(newPoint)
        return newData


'''
Takes in an array of size two that contains two arrays.
These correspond to the bins of signal and background for a
stacked histogram. What is returned is data in an array that is
s/b^(0.5)
'''
def getCutInfo(bins):
        signif = list()
        sigBins = bins[0].tolist()
        backBins = bins[1].tolist()

        #calculate cut for each bin
        for i in range(len(sigBins)):
                backSum = 0
                sigSum = 0
                #sum all bins past and including cut
                for j in range(i, len(sigBins)):
                        sigSum += sigBins[j]
                        backSum += backBins[j]
                signifNum = sigSum/math.sqrt(backSum)
                signif.append(signifNum)
        return signif


'''
This reads in and parses an arff file.

output:
        list(list()) - list of data points
'''
def read_arff(file):
        loadData, loadMeta = loadarff(file)
        attributes  = list(loadMeta)
        data  = list(loadData)

        return data


if __name__ == "__main__":
        exit(main())
