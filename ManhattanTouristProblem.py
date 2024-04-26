import os

#Grid size: rows x cols of nodes:
rows = 5
cols = 5


downsGridFile = os.getcwd() + "/manhattan downsGridFile.txt"
rightsGridFile = os.getcwd() + "/manhattan rightsGridFile.txt"
diagonalsGridFile = os.getcwd() + "/manhattan diagonalsGridFile.txt"

points = {}

#build the diagonalsGrid
with open(diagonalsGridFile,'r') as file: lines= file.readlines()
for i in range(len(lines)):
    lines[i] = lines[i].strip()
diagonalsGrid = [x.split(' ') for x in lines] #split into rows

#Add diagonalsGrid points to pointsGrid
for i in range(rows-1):
    for j in range(cols):
        inNode = i*cols+(j-1)+2
        if inNode != 0 and inNode%cols == 0:
            print('SKIP')
            continue
        key = str(inNode) + ':' + str(cols+inNode+1)
        points[key] = int(diagonalsGrid[i][j])
        print('i: ',i,'. j: ',j,'inNode: ',inNode,'. key: ', key,'. points: ',diagonalsGrid[i][j])
print('diagonalsGrid: \n',diagonalsGrid, '\n pointsGrid: \n ',points)

#build the rightsGrid
with open(rightsGridFile,'r') as file: lines= file.readlines()
for i in range(len(lines)):
    lines[i] = lines[i].strip()
rightsGrid = [x.split(' ') for x in lines] #split into rows

#Add rightsGrid points to pointsGrid
for i in range(rows):
    for j in range(cols):
        inNode = i*cols+(j-1)+2
        if inNode != 0 and inNode%cols == 0:
            print('SKIP')
            continue
        key = str(inNode) + ':' + str(inNode+1)
        points[key] = int(rightsGrid[i][j])
        print('i: ',i,'. j: ',j,'inNode: ',inNode,'. key: ', key,'. points: ',rightsGrid[i][j])
print('rightsGrid: \n',rightsGrid, '\n pointsGrid: \n ',points)

#build the downsGrid
with open(downsGridFile,'r') as file: lines= file.readlines()
for i in range(len(lines)):
    lines[i] = lines[i].strip()
downsGrid = [x.split(' ') for x in lines] #split into rows
print('downsGrid: \n',downsGrid)

#Add downsGrid points to pointsGrid
for i in range(rows-1):
    for j in range(cols):
        inNode = i*cols+(j-1)+2
        key = str(inNode) + ':' + str(inNode+cols)
        points[key] = int(downsGrid[i][j])
        print('i: ',i,'. j: ',j,'inNode: ',inNode,'. key: ', key,'. points: ',downsGrid[i][j])
print('downsGrid: \n',downsGrid, '\n pointsGrid: \n ',points)

        

def manhattanRecursive(rows,cols,points):
    pointGrid = {1:0}
    boundaries = {1:0}
    longestPaths= {}
    for node in range(rows*cols): longestPaths[node] = [1] #Initialize longestPaths for each node.
    print('longest paths: \n',longestPaths)
    
    for i in range(20): #A number long enough to ensure all edges are covered.
        newBoundaries= {}
        for node in boundaries:
            #print('\n expanding from node ',node)
            
            #expand pointGrid rightwards:
            if node%cols != 0:
                newRightNode = node+1
                addedPoints = points[str(node)+':'+str(newRightNode)]
                if newRightNode not in newBoundaries or newBoundaries[newRightNode] < pointGrid[node] + addedPoints:
                    newBoundaries[newRightNode] = pointGrid[node] + addedPoints
                if newRightNode not in pointGrid or pointGrid[newRightNode] < pointGrid[node] + addedPoints: #Only make it the Node's point value if it's greater than the current value.
                    pointGrid[newRightNode] = pointGrid[node] + addedPoints
                    longestPaths[newRightNode] = [x for x in longestPaths[node]]
                    longestPaths[newRightNode].append(newRightNode)   
                print('new right node: ',newRightNode,'. added points: ',addedPoints)
                         
            #expand pointGrid downwards:
            if node<= rows*cols-cols:
                newDownNode = node+cols
                addedPoints = points[str(node)+':'+str(newDownNode)]
                if newDownNode not in newBoundaries or newBoundaries[newDownNode] < pointGrid[node] + addedPoints:
                    newBoundaries[newDownNode] = pointGrid[node] + addedPoints
                if newDownNode not in pointGrid or pointGrid[newDownNode] < pointGrid[node] + addedPoints:
                    pointGrid[newDownNode] = pointGrid[node] + addedPoints
                    longestPaths[newDownNode] = [x for x in longestPaths[node]]
                    longestPaths[newDownNode].append(newDownNode)
                #print('new down node: ',newDownNode,'. added points: ',addedPoints)
                    
            #expand pointGrid diagonally:
            if node%cols != 0 and node <= rows*cols-cols:
                newDiagonalNode = node+cols+1
                addedPoints = points[str(node)+':'+str(newDiagonalNode)]
                if newDiagonalNode not in newBoundaries or newBoundaries[newDiagonalNode] < pointGrid[node] + addedPoints:
                    newBoundaries[newDiagonalNode] = pointGrid[node] + addedPoints
                if newDiagonalNode not in pointGrid or pointGrid[newDiagonalNode] < pointGrid[node] + addedPoints:
                    pointGrid[newDiagonalNode] = pointGrid[node] + addedPoints
                    longestPaths[newDiagonalNode] = [x for x in longestPaths[node]]
                    longestPaths[newDiagonalNode].append(newDiagonalNode)
                print('new diagonal node: ',newDiagonalNode,'. added points: ',addedPoints)
                
            
        boundaries= newBoundaries
        keys= list(pointGrid.keys()).sort()
        #sortedPointGrid = {i: pointGrid[i] for i in keys}
        #print('sorted Grid: ',sortedPointGrid)
        print('\n pointGrid: ',pointGrid,'\n boundaries: ',boundaries,'\n len(grid); ',len(pointGrid),'\n longestPaths:\n',longestPaths)
        
    print('\n most points: ',pointGrid[rows*cols],'\n longest paths: ',longestPaths[rows*cols])
    return longestPaths[rows*cols]
    

print(manhattanRecursive(rows,cols,points))

#1 7 12 13 18 23 24 25 <--Correct answer
        


