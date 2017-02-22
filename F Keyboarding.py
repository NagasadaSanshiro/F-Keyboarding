'''
Created on Dec 08, 2015

@author: Zhongyi Yan
'''
import os


def getpos( c ):
    positionTMP = []
    positionIndex = 0
    for i in range( 0, keyRow ):
        for j in range( 0, keyCol ):
            if(keyBoard[i][j] == c):
                positionIndex = keyCol * i + j
                positionTMP.append(positionIndex)
                dictTmp = { positionIndex:[i,j] }
                edgeIndexPos.update(dictTmp)       
    return (positionTMP)

def MakeGraph( ):
    for i in range( 0, len(inText) ):
        edgeIndexTMP = getpos( inText[i] )
        edgeIndex.append(edgeIndexTMP)
    if( edgeIndex[0] != [0] ):
        edgeIndex.insert( 0, [0] )
    

def upposition( i, j ):
    while( i > 0 ):
        if keyBoard[i-1][j] != keyBoard[i][j]:
            return( [i - 1, j] )
        i = i - 1
    return None

def downposition( i, j ):
    while( i < keyRow - 1 ):
        if keyBoard[i+1][j] != keyBoard[i][j]:
            return( [i + 1, j] )
        i = i + 1
    return None

def leftposition( i, j ):
    while( j > 0 ):
        if keyBoard[i][j-1] != keyBoard[i][j]:
            return( [i, j - 1] )
        j = j - 1
    return None

def rightposition( i, j ):
    while( j < keyCol - 1 ):
        if keyBoard[i][j+1] != keyBoard[i][j]:
            return( [i, j + 1] )
        j = j + 1
    return None

def getneibs(i,j):
    neibs = []
    up = upposition(i,j)
    down = downposition(i,j)
    left = leftposition(i,j)
    right = rightposition(i,j)
    if(up!= None):
        for k, v in keyDict.items():
            if v == up:
                neibs.append(k)
    if(down!= None):
        for k, v in keyDict.items():
            if v == down:
                neibs.append(k)
    if(left!= None):
        for k, v in keyDict.items():
            if v == left:
                neibs.append(k)    
    if(right!= None):
        for k, v in keyDict.items():
            if v == right:
                neibs.append(k)    
    return(neibs)    

def BuildKeyBoard():
    for i in range( 0, keyRow ):
        for j in range( 0, keyCol ):
            positionIndex = keyCol * i + j
            dictTmp = { positionIndex:[i,j] }
            keyDict.update( dictTmp )
    
def MakeConnection():
    for i in range( 0, keyRow ):
        for j in range( 0, keyCol ):
            neibs = getneibs(i,j)
            positionIndex = keyCol * i + j
            dictTmp = { positionIndex:neibs }
            keyBoardDict.update(dictTmp)
            keyDict.update( {positionIndex: [i,j] } )
    
            
def PathFind( nFrom, nTo ):
    distance = 0
    past.append(nFrom)
    v = keyBoardDict[nFrom]
    distance += 1
    disTMP = []
    #print(distance)
    for i in v:
        #print(disTMP)
        if( i not in past ):
            if i == nTo:
                past.pop()
                return distance
            else:
                disTMP.append((PathFind( i, nTo )))
        else:
            disTMP.append(9999)
    if len(disTMP) > 0:
        distance += min(disTMP)
    past.pop()
    return distance
            
def AddWeight():
    edgeLenF = len( edgeIndex )
    for i in range( 0, edgeLenF - 1 ):
        weightTmp = []
        for nFrom in edgeIndex[i]:
            for nTo in edgeIndex[i+1]:
                past = []
                thisWeight = PathFind( nFrom, nTo )
                #print(thisWeight)
                weightTmp.append([nFrom,nTo,thisWeight])
        weight.append(weightTmp)
    edgeIndex.append( [-1] )
    weightTail = []
    for i in range( 0, len(weight[-1]) ):
        fromTmp = weight[-1][i][1]
        weightTail.append([fromTmp, -1, 0])
    weight.append(weightTail)
    
def buildCost( cost, path, mark ):
    for i in range( 0 , len( edgeIndex) ):
        for j in range( 0, len( edgeIndex[i]) ):
            cost[edgeIndex[i][j]] = 9999
            path[edgeIndex[i][j]] = 0
            mark[edgeIndex[i][j]] = 0
    graphLen = len( graph[0] )
    cost[0] = 0
    mark[0] = 1
    for i in range ( 0, graphLen ):
        cost[graph[0][i][0]] = graph[0][i][1]

def dijsktra():
    cost = {}
    path = {}
    mark = {}
    buildCost( cost, path, mark )
    print(cost)
    print(path)
    print(mark)
    start = 0
    edgeIndexLen = len(edgeIndex)
    for u in range( 0, edgeIndexLen - 1 ):
        #edgeIndexLenU = len(edgeIndex[u])
        if len(edgeIndex[u]) == 1 and len(edgeIndex[u+1]) == 1:
            #print(edgeIndex[u+1][0])
            #print(edgeIndex[u][0])
            #print(cost[edgeIndex[u][0]])
            #print(graph[edgeIndex[u][0]][0][1])
            lengthTMP = cost[edgeIndex[u][0]] + graph[edgeIndex[u][0]][0][1]
            cost[edgeIndex[u+1][0]] = lengthTMP
            path[edgeIndex[u+1][0]] = u
        else:    
            for v in edgeIndex[u]:
                if v == -1:
                    break
                graphLen = len( graph[v] )
                for i in range ( 0, graphLen ):
                    newNode = graph[v][i][0]
                    if mark[newNode] == 1:
                        continue
                    lengthTMP = cost[v] + graph[v][i][1]
                    if lengthTMP < cost[newNode]:
                        cost[newNode] = lengthTMP
                        path[newNode] = v
                    print(cost)
                    print(path)
                    print(mark)   
            mark[v] = 1   
     
    return cost, path  
    
def BuildGraph():
    edgeLen = len( weight )
    for i in range( 0, edgeLen ):
        edgeColLen = len( weight[i] )
        pathTMp = []
        for j in range( 0, edgeColLen ):
            x = weight[i][j][0]
            y = weight[i][j][1]
            z = weight[i][j][2]
            pathTMp.append([y,z])
            graphTMP = { x: pathTMp }    
            if x in graph:
                if [y,z] not in graph[x]:
                    graph[x].append([y,z])
            else:
                graph.update(graphTMP) 
            pathTMp = []
        
if os.path.exists('input1.txt'):
    fileIn = open( 'input1.txt' , 'r' )
    fileOut = open( 'output1.txt', 'w+' )
    keyRow = 0
    keyCol = 0
    keyBoard = []
    edgeIndexPos = { }
    edgeIndex = []
    keyDict = {}
    keyBoardDict = {}
    weight = []
    graph = {}
    past = []
    line = fileIn.readline()
    keyRow, keyCol = line.split(' ')
    keyRow, keyCol = int(keyRow), int(keyCol)
    for i in range( 0, keyRow ):
        line = fileIn.readline()[:-1]
        keyBoard.append(line.split(' '))
    inText = fileIn.readline()
    inText += '*'
    inTextLen = len(inText)
    MakeGraph()
    print(edgeIndex)
    print(edgeIndexPos)
    BuildKeyBoard()
    print(keyDict)
    MakeConnection()
    print(keyBoardDict)
    AddWeight()
    print(weight)
    BuildGraph()
    print(graph)
    cost, path = dijsktra()
  
    distance = cost[-1] + inTextLen
    print(distance)
    fileOut.write('shortest path is {0:d} '.format(distance))