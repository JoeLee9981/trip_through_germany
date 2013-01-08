'''
Created on Oct 28, 2012

@author: Joseph Lee
'''

import heapq
from data_manager import Data_Manager
from collections import defaultdict

#Algorithm referenced from programmingpraxis.com/2010/04/09/minimum-spanning-tree-prims-algorithm
def prim( paths ):
    data = Data_Manager()
    conn = defaultdict( list )
        
    start = data.get_start()
    #don't  change (12, 16, 17, 21) starting cities
    for x in start:
        visited = []
        path = []
        visited.append(x)
        #append start city key
        connections = data.get_conn(x)
        #(weight, type, connect)
        heapq.heapify(connections)
        while connections:
            #(weight, type, Connection)
            cost, c1, c2 = heapq.heappop(connections)
            if c2 not in visited:
                visited.append(c2)
                path.append((c1, c2, cost))
        
                for x in data.get_conn(c2):
                        heapq.heappush(connections, x)
        paths.append(path)
    #for path in paths:
        #for x in path:
            #print(str.format("({0:3}, {1:3}, {2:5.4}), ", x[0], x[1], x[2]), end = "")
        #print()
    allPaths = []
    for x in paths:
        allPaths.append(_draw_paths(x))
    return allPaths
    #return paths

#split up the minimum spanning tree into optimal paths    
def _draw_paths(mst):
    prev = (-1,-1,-1) # invalid connection used to start the loop
    path_num = 0
    paths = []
    paths.append([])
    
    for curr in mst:
    # (city0, city1, path)
        if curr[0] != prev[1] and prev[1] != -1:
            path_num += 1
            paths.append([])
        prev = curr
        paths[path_num].append(curr)
    #for x in paths:
        #print(x)
    #[] or paths
    return _connect_paths(paths)

#use dijkstra's to connect each optimized path from the min span tree
#find the nearest connection (backtrack when reach a dead end)        
def _connect_paths(paths):
    #append the first path
    i = 0
    completed = paths.pop(i)
    while paths:
        #(weight, type, connection)
        #last position of first list
        start = completed[len(completed) -1][1]
        shortest = None
        next = None
        for x in paths:
            #find the next closest start point
            if shortest != None:
                #(x[0][0]) city0 in each path
                temp = dijkstra(start, x[0][0])
                #temp = (weight, type, connect) - no change needed
                if temp[0] < shortest[0]:
                    shortest = temp
                    next = x
            else:
                shortest = dijkstra(start, x[0][0])
                next = x
        if shortest[0] > 0:
            #(weight, connect)
            completed.append((shortest[1][0], shortest[1][len(shortest[1])-1], shortest[0]))        
        completed += next
        paths.remove(next)
    end = _end_path(completed[len(completed) - 1][1])
    completed.append(end)
    return completed

#return back to a city with an Airport
def _end_path(city):
    #get list of end cities
    short = (float('inf'), 0)
    data = Data_Manager()
    end = data.get_start()
    for c in end:
        path = dijkstra(city, c)
        if path[0] < short[0]:
            short = path
    dist = short[0]
    path = short[1]
    return (path[0], path[len(path) - 1], dist)
    #find nearest airport
    #append pathway
    
#algorithm referenced from:
#thomas.pelletier.im/2010/02/dijkstras-algorithm-python-implementation
def dijkstra(start, end):
    data = Data_Manager()
    cities = data.get_cities()
    D = {}
    P = {}
    for city in cities:
        D[city] = float('inf')
        P[city] = ""
        
    D[start] = 0
    remain_cities = cities
    
    while len(remain_cities) > 0:
        short = None
        city = ''
        for x in remain_cities:
            if short == None:
                short = D[x]
                city = x
            elif D[x] < short:
                short = D[x]
                city = x
        remain_cities.remove(city)
        connects = data.get_conn(city)

        for x in connects:
            #|||(weight, type, cost, time)
            if x[1] == city:
                if D[x[2]] == float('inf'):
                    D[x[2]] = D[city] + x[0]
                    P[x[2]] = city
                elif D[x[2]] > D[city] + x[0]:
                    D[x[2]] = D[city] + x[0]
                    P[x[2]] = city
                    
    path = []
    node = end
    while node != start:
        if path.count(node) == 0:
            path.insert(0, node)
            node = P[node]
        else:
            break
        
    path.insert(0, start)
    return (D[end], path)
