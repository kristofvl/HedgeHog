#!/usr/bin/env python2.7

SectorSize = 512       # bytes
SectorsPerCluster = 64 # Sectors per cluster
NumberOfLogFiles = 15  # max is 15 (including config.txt)
scaleFactor = 10
FirstClusterOfFiles = 3
def printFAT():
    firstFileSize = 65 # Clusters in first file ~2.1MB
    i = 0
    fileSizeList = []
    nextFileSz = firstFileSize  # in Clusters
    totalSz = 0         # in Clusters
    numOfClustersInFile = 1
    for i in range(0, NumberOfLogFiles):
        totalSz = totalSz + nextFileSz
        fileSizeList.append(nextFileSz)
        numOfClustersInFile = nextFileSz/(SectorSize*SectorsPerCluster)
        nextFileSz = nextFileSz + (i) * firstFileSize
        
    print 'Total Size = ', totalSz, 'clusters'
    print fileSizeList

    startCluster = FirstClusterOfFiles;
    endClusterOfFile = 0
    startClusterList = []
    finalClusterList = []
    for i in range(0, NumberOfLogFiles):
        startClusterList.append(startCluster)
        endClusterOfFile = startCluster + fileSizeList[i] - 1
        finalClusterList.append(endClusterOfFile)
        startCluster = endClusterOfFile + 1
        
    print 'start', startClusterList
    print 'end', finalClusterList

    fileSizes = []
    for i in range(0, NumberOfLogFiles):
        fileSizes.append( fileSizeList[i] * SectorSize * SectorsPerCluster )
        
    f = open('array.txt', 'w')
    print f

    f.write('Files BEGIN at the following clusters:\n')
    for i in range(0, NumberOfLogFiles):
        f.write(str(startClusterList[i]))
        f.write(', ')
    f.write('\n\nFiles END at the following clusters:\n')
    for i in range(0, NumberOfLogFiles):
        f.write(str(finalClusterList[i]))
        f.write(', ')
    f.write('\n\nFiles Sizes in Bytes:\n')
    for i in range(0, NumberOfLogFiles):
        f.write(str(fileSizes[i]))
        f.write(', ')

    f.write('\n\n')

printer = printFAT()
