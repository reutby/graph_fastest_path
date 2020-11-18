import heapq
import pandas as pd 
from pandas import DataFrame,read_csv


def create_graph(file_name):
    """generate dictinary of vertexs name containing a dictinery
    with all other node and the distances(weight) between them
    from adjency matrix 
    e - number of edges
    time complaxity O(e) 
    for exmple: 
        {a:{b:5,c:3,d:7,e:8,f:12},
         b:{a:3,c:6,d:9,e:4,f:11},
         c:{a:4,b:12,d:54,e:8,f:13},
         d:{a:1,b:3,c:12,e:33,f:3},
         e:{a:12,b:4,c:7,d:11,f:74},
         f:{a:4,b:7,c:12,d:11,e:12}
         }"""
    graph = {}
    df = pd.read_csv(file_name)
    adjacency_matrix = df.values.tolist()
    node_names = df["names"].tolist()

    for row in adjacency_matrix:
        for i in range(1,len(row)):
            
            if row[i]=='-':
                continue 
            if row[0] in graph:  
                graph[row[0]].update({node_names[i-1]:int(row[i])})
            else:
                graph[row[0]] = {node_names[i-1]:int(row[i])}
    return graph

def create_path_string(path,graph) :
    """generate the string path represent the shorthest path 
    from the src vertex to the dest vertex"""
    first = path.pop()
    allpath=""
    
    while(len(path)) :
        next =path.pop()
        allpath = allpath + first +"--("+ str(graph[first][next])+")-->"
        first = next
    allpath+=first
    return allpath

def reversed_path(predecessors,dest):
    """translate the shortest path from the predecessors dictinary
        going in the reverse direction from dest to src"""
    path = []
    pred=dest    
    #display the shortest path 
    while pred != None:
        path.append(pred)
        pred=predecessors.get(pred,None)
    return path

def sanity_checks(graph,src,dest):
    if src not in graph:
       print('The source node cannot be found in the graph')
       return False
    if dest not in graph:
        print('The target node cannot be found in the graph')    
        return False
    return True

def find_fastest_path(file_name,src,dest):
    """ calculates the fastest path from src vertex to dest vertex
        assuming all weight edges are positive.
        assuming the csv file is orgenized as adjency matrix
        v - number of vertex
        e - number of edges
        time complexity:  O((v+e)*log(n)) = O(e*logv)
    """    
    #initilized parameters
    visited=[]
    distances={}
    predecessors={}

    #create dic that represent the graph edges for each vertex
    graph = create_graph(file_name)
    
    #sanity checks
    if sanity_checks(graph,src,dest)==False:
        return

    #initial  run, initializes the cost of source node
    distances[src]=0
    pq = [(0, src)]   
    
    while len(pq) > 0:
        current_distance, current_vertex = heapq.heappop(pq) 
        if current_vertex == dest :
            break

        # visit the neighbors
        for neighbor, weight in graph[current_vertex].items():
            if neighbor not in visited: 
                new_distance = current_distance + int(weight)
                #check  if new distance are shorter then calculate before 
                if new_distance < distances.get(neighbor,float('inf')):
                    distances[neighbor] = new_distance   
                    predecessors[neighbor] = current_vertex    
                    heapq.heappush(pq, (new_distance, neighbor))       
        # mark as visited
        visited.append(current_vertex)
    
    path=reversed_path(predecessors,dest)
    readable =create_path_string(path,graph) 
    print("path: "+readable+",   cost="+str(distances[dest]))  
        
if __name__ == "__main__":
    test1_answer = ['f',2,'d',2,'c',4]
    test2_answer = ['e',8,'a',5,'f',13]
    test3_answer = ['a',6,'d',6]
    
    #negative tests
    #wrong src name
    print("\n-------------negative tests-----------\n")
    print("test1")
    find_fastest_path("exmple1.csv",'w','a')
    #wrong dest name
    print("test2:")
    find_fastest_path("exmple1.csv",'a','w')

    print("\n-------------positive tests-----------\n")
    #positive tests
    print("test1:")
    find_fastest_path("exmple1.csv",'f','c')
    print("test2:")
    find_fastest_path("exmple1.csv",'e','f')
    print("test3:")
    find_fastest_path("exmple1.csv",'a','d')
    print("test4:")
    find_fastest_path("exmple2.csv",'a','f')
