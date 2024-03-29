import sys
import re
import time

graphRE=re.compile("(\\d+)\\s(\\d+)")
edgeRE=re.compile("(\\d+)\\s(\\d+)\\s(\\d+)")

vertices=[]
edges=[]

def BellmanFord(G):
    #Setup pathPairs with distance to self = 0
    pathPairs=[[float("Inf") for i in range(len(G[0]))] for j in range(len(G[0]))]
    # pathPairs = []
    for i in range(len(G[0])):
        for j in range(len(G[0])):
            if i == j:
                pathPairs[i][j] = float(0);
    # print(pathPairs)
    # pathPairs[0][0] = 0
    # Fill in your Bellman-Ford algorithm here
    # The pathPairs list will contain the list of vertex pairs and their weights [((s,t),w),...]
    for a in range(1, len(G[0]) - 1):
        for b in range(len(G[0])):
            for c in range(len(G[0])):
                for d in range(len(G[0])):
                    if float(pathPairs[c][d]) > (float(pathPairs[b][c]) + float(G[1][c][d])) :
                        pathPairs[c][d] = float(pathPairs[b][c]) + float(G[1][c][d])
                        # print(float(pathPairs[b][c]) + float(G[1][c][d]))
    for b in range(len(G[0])):
        for c in range(len(G[0])):
            for d in range(len(G[0])):
                if float(pathPairs[c][d]) > (float(pathPairs[b][c]) + float(G[1][c][d])) :
                    # print("false")
                    return False
    # print("BellmanFord: ", pathPairs)
    return pathPairs

def FloydWarshall(G):
    # print(G)
    pathPairs=[[0 for i in range(len(G[0]))] for j in range(len(G[0]))]
    # Fill in your Floyd-Warshall algorithm here
    # The pathPairs list will contain the list of vertex pairs and their weights [((s,t),w),...]
    for i in range(len(G[0])):
        for j in range(len(G[0])):
            if i == j:
                pathPairs[i][j] = 0
            elif G[1][i][j] != float("Inf"):
                pathPairs[i][j] = float(G[1][i][j])
            else:
                pathPairs[i][j] = float("Inf")
    for i in range(len(G[0])):
        for j in range(len(G[0])):
            for k in range(len(G[0])):
                pathPairs[i][j] = min(float(pathPairs[i][j]), float(pathPairs[i][k]) + float(pathPairs[k][j]))

    # print("FloydWarshall: ", pathPairs)
    return pathPairs

def readFile(filename):
    global vertices
    global edges
    # File format:
    # <# vertices> <# edges>
    # <s> <t> <weight>
    # ...
    inFile=open(filename,'r')
    line1=inFile.readline()
    graphMatch=graphRE.match(line1)
    if not graphMatch:
        print(line1+" not properly formatted")
        quit(1)
    vertices=list(range(int(graphMatch.group(1))))
    edges=[]
    for i in range(len(vertices)):
        row=[]
        for j in range(len(vertices)):
            row.append(float("inf"))
        edges.append(row)
    for line in inFile.readlines():
        line = line.strip()
        edgeMatch=edgeRE.match(line)
        if edgeMatch:
            source=edgeMatch.group(1)
            sink=edgeMatch.group(2)
            if int(source) > len(vertices) or int(sink) > len(vertices):
                print("Attempting to insert an edge between "+source+" and "+sink+" in a graph with "+vertices+" vertices")
                quit(1)
            weight=edgeMatch.group(3)
            edges[int(source)-1][int(sink)-1]=weight
    #Debugging
    # for i in G:
    #     print(i)
    return (vertices,edges)

def main(filename,algorithm):
    algorithm=algorithm[1:]
    G=readFile(filename)
    # #Debugging
    # for i in G:
    #     print(i)
    # G is a tuple containing a list of the vertices, and a list of the edges
    # in the format ((source,sink),weight)
    if algorithm == 'b' or algorithm == 'B':
        BellmanFord(G)
    if algorithm == 'f' or algorithm == 'F':
        FloydWarshall(G)
    if algorithm == "both":
        start=time.clock()
        BellmanFord(G)
        end=time.clock()
        BFTime=end-start

        start=time.clock()
        FloydWarshall(G)
        end=time.clock()
        FWTime=end-start

        print("Bellman-Ford timing: "+str(BFTime))
        print("Floyd-Warshall timing: "+str(FWTime))

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("python assignment2.py -<f|b> <input_file>")
        quit(1)
    if len(sys.argv[1]) < 2:
        print('python assignment2.py -<f|b> <input_file>')
        quit(1)
    main(sys.argv[2],sys.argv[1])
