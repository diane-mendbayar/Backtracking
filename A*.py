#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 10:29:24 2021

@author: dashnyammendbayar
"""
# First creatigna an empty PriorityQueue


import sys
import pandas as pd
import timeit 
from queue import PriorityQueue
from collections import defaultdict
import numpy as np   
    
straightline=pd.read_csv("straightline.csv", delimiter=',') #reading from file by pd

    #inserting both files

    
driving=pd.read_csv("driving.csv", delimiter=',')

statelist=driving['STATE'].values.tolist()      #holding the state labels here
arr=driving.drop(labels='STATE', axis=1).to_numpy()     #had to drop the row names to map in dicitonary
d = defaultdict(lambda: defaultdict(int))       #initiating default nested dictiooonary
import itertools
class Node:
    def __init__(self, state, goal, parent, pathCost, heuristic, algorithm):
        self.STATE = state
        self.GOAL= goal
        self.PARENT = parent
        self.PATHCOST = pathCost
        self.heuristic=heuristic
        if algorithm == 'GBFS':
            self.EVAL = self.heuristic
            
        elif algorithm == 'ASTAR':
            self.EVAL = self.PATHCOST + self.heuristic
        
        
    def getState(self):
        return self.STATE
    
    def getGOAL(self):
        return self.GOAL

    def getParent(self):
        
        parent=[]
        parent.append(self.PARENT)
        return parent

    def getPathCost(self):
        return self.PATHCOST
    
    def getHeuristics(self):                    #the function that takes heuristic from straigline file
        
        return self.heuristic
    def getEval(self):
        return self.EVAL

    def __lt__(self, other):
        return self.getEval() < other.getEval()
    
          

class Problem:
     
    actions=dict()                                  #initiates dict to store possible states from current state/ vertices and edges/
    
    #need to think of a way to converrt s=node.state to int
    #so numpy array to dicitonary for a graph that holds vertices, edge with weight 
    for i in range(arr.shape[0]):         #2d np.array, so two loops needed 
        for j in range(arr.shape[1]):
            val = arr[i, j]
            if val > 0:                 #get edges
                d[i+1][j+1] = val            #dictionary that holds states,vertices, wegihts
          
    
    def __init__(self, initial, goal):    #setting up a problem
        
        #self.data=data
        self.initial=initial                    #start state
        self.goal=goal                          #goal state
        
    def actions(self, s):                      #get all possible edges from state s
        
        index = statelist.index(s)              #getting the index of list label
        index=index+1                           #messed up with index of the graph by one, so fixed it manually here
        # iterate through a nested dictionary to get actions for state s
        for vertex, edge in d.items():
   
            if index==vertex:           #getting driving states of s
                #print(index)
                return ([(k, edge[k]) for k in edge])   #every edges has its key, and value (in our case it is vertix, and weight)
                                                         
    
    #transtion model taht decide what the resulting state afte applying s funciton for action
    def result(self, action):               #enter parent and child state and change parent to child
       
        s=action[0]-1               #accessing first tupple in list, which is index
                                    #messed up with index of the graph by one, so fixed it manually here
        state=statelist[s]          #finding the state label from label list
        return state         #returning a state label converting from index
     
        
    #path cost to state with label s through resulting state
    def actioncost(self, action):   #driving distance between states, so in our case the weight of the edge
        return action[1]            #value
    
    def straight_distance(self, state): #state to goal state straight line distance, heuristics
        t=straightline['STATE']==state
        t=np.where(t)[0]        #strue values   #get all the heuristics to all states
   
        if self.goal in straightline:       #checking if path can be found
            distance=straightline[self.goal].iloc[t] 
            k=distance.values[0]
        else: 
            k=0     #path not found
        return k         #returning 0 or heuristic value
            
    
def bfs(initial, goal):     #followed the textbook
    #call problem and state initial and goal
    timeStart = timeit.default_timer()          #time start  
    problem=Problem(initial, goal)
    print('\nGreedy Best First Search:')
    print('Initial state: ', initial)
    print('Goal state: ', goal)
    a=problem.straight_distance(initial)    #getting heuristic
    if a!=0:                                #checking if the goal state exists
      
        node=Node(initial, goal, None, 0, a, 'GBFS')    #initial 
        #print(node.STATE)
        frontier=PriorityQueue()
        frontier.put(node, node.EVAL)
        reached={problem.initial: node}
    
        while frontier.empty()==False:
        
            node1=frontier.get()
        
            print(node1.PARENT)
            children_nodes=[]
            if problem.goal==node1.STATE:           #if we reached the goal
                print('Path cost: ', node1.PATHCOST)
                break
           # return node1
            for child in expand(problem, node1, 'GBFS'):
               children_nodes.append(child)
               s=child.STATE
               if s not in reached or child.PATHCOST<reached[s].PATHCOST:
            
                   reached[s]=child
                   frontier.put(child)
            
        #return 0
    else:
         print("Path: NOT FOUND")
        
        
    timeEnd= timeit.default_timer()             #finish time
    elapsedTimeInSec = timeEnd - timeStart
    print('Execution time: ', elapsedTimeInSec, '\n')  
  #  print()

def astar(initial, goal):
    #call problem and state initial and goal
            
    timeStart = timeit.default_timer()          #time start
    
    problem=Problem(initial, goal)
    print('A* Search:')
    print('Initial state: ', initial)
    print('Goal state: ', goal)
    
    a=problem.straight_distance(initial)    #getting heuristic
    if a!=0:                                #checking if the goal state exists
        anode=Node(initial, goal, None, 0, a, 'ASTAR')
   
    
        frontier=PriorityQueue()
        frontier.put(anode, anode.EVAL)
        reached={problem.initial: anode}
    
        while frontier.empty()==False:  
            node1=frontier.get()
            #parent=[]
            #print(node1.getParent())      #I'd like to print paths, but somewhow printing all states visited
            #parent.append(node1.PARENT)
            #node1.PARENT not in parent
            print (node1.PARENT)
       # print(node1.)
            if problem.goal==node1.STATE:
                print('Path cost: ', node1.PATHCOST)          #total path cost
                break
            
            for child in expand(problem, node1, 'ASTAR'):
                s=child.STATE
                if s not in reached or child.PATHCOST<reached[s].PATHCOST:
            #if s not in 
                    reached[s]=child
                    frontier.put(child)  
       
    else:    
        print("Path: NOT FOUND")
    timeEnd= timeit.default_timer()             #finish time
    elapsedTimeInSec = timeEnd - timeStart
       
    print('Execution time: ', elapsedTimeInSec, '\n')   
 
  
    #return 0
  #  print()    
def expand(problem1, node, check):
    #print(node.STATE)
    s=node.STATE
    for action in problem1.actions(s):           #each possible states from state s
        #print(action)
        new_s=problem1.result(action)         #getting the resulting state label
        #print(new_s)
        cost=node.PATHCOST+problem1.actioncost(action)
        a=problem1.straight_distance(new_s)      #here
        if check=='GBFS':
           
            yield Node(new_s, problem1.goal, s, cost, a, 'GBFS')
        else:
            
            yield Node(new_s, problem1.goal, s, cost, a, 'ASTAR')
        
def main():
        
    a=len(sys.argv)

    if (a<3):
        print('Error: Not enough arguments')

    elif (a>3):
        print('Error: Too many input arguments')

    else:
        
        initial_state=str(sys.argv[1])
        goal_state=str(sys.argv[2])
         
        bfs(initial_state, goal_state)
    
        astar(initial_state, goal_state)
          

if __name__ == "__main__": main()


















