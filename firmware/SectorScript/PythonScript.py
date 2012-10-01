SectorSize = 512       # bytes
SectorsPerCluster = 64 # Sectors per cluster
NumberOfLogFiles = 15  # max is 15 (including config.txt)
scaleFactor = 100
FirstClusterOfFiles = 2
def printFAT():
    firstFileSize = 100*SectorSize*SectorsPerCluster # ~3.2MB
    i = 0
    fileSizeList = []
    nextFileSz = 0
    totalSz = 0
    numOfClustersInFile = 1
    for i in range(0, NumberOfLogFiles):
        nextFileSz = firstFileSize + nextFileSz + scaleFactor*i
        totalSz = totalSz + nextFileSz
        fileSizeList.append(nextFileSz)
        numOfClustersInFile = nextFileSz/(SectorSize*SectorsPerCluster)

        print totalSz

    ClustersPerFile = []
    temp = 0
    for i in range(0, NumberOfLogFiles):
        temp = fileSizeList[i]
        numOfClustersInFile = temp / (SectorSize *  SectorsPerCluster)
        ClustersPerFile.append(numOfClustersInFile)
#        print ClustersPerFile[i]

    StartCluster =  [FirstClusterOfFiles]
    EndingCluster = [FirstClusterOfFiles + ClustersPerFile[0]]
    for i in range(1, NumberOfLogFiles):
        StartCluster.append( EndingCluster[i-1]+1 )
        EndingCluster.append( EndingCluster[i-1] + ClustersPerFile[i] )
#        print ("*", EndingCluster[i])

    StartingSector = []
    EndingSector = []
    for i in range(0, NumberOfLogFiles):
        StartingSector.append( StartCluster[i] * SectorsPerCluster )
        EndingSector.append( EndingCluster[i]*SectorsPerCluster )
#        print("**", EndingSector[i])

    f = open('array.txt', 'w')
    print f

    f.write('Files BEGIN at the following sectors:\n')
    for i in range(0, NumberOfLogFiles):
        f.write(str(StartingSector[i]))
        f.write(',\n')
    f.write('Files END at the following sectors:\n')
    for i in range(0, NumberOfLogFiles):
        f.write(str(EndingSector[i]))
        f.write(',\n')
