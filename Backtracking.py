#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 13:42:07 2021

@author: dashnyammendbayar
"""


import sys
import pandas as pd

driving=pd.read_csv("driving2.csv", delimiter=',')
parks=pd.read_csv("parks.csv", delimiter=',')
zones=pd.read_csv("zones.csv", delimiter=',')
statelist=driving['STATE'].values.tolist()      #holding the state labels here

def is_not_complete(assignment):
   
    res=not all(assignment.values())                #if not all none, return true
    return res
    
def select_unassigned_variable(assignment):
    for v in assignment:
        if assignment[v] is None:                #if the zone is not assigned return zone
          return v
      
    
def order_domain_values(state):                 #getting go to states 
    index = statelist.index(state)
    arr=driving.drop(labels='STATE', axis=1)            #removing the label to remove the index confusiton
    a=arr.loc[index]
    d=[]
    for state, value in a.items():                                #states that can travel from state X
            if value>0:                                           #has edge
                d.append(state)
    return d                                    #returnning state
                
def backtrack(initial, parks_visited, n_of_parks, assignment):
    
    if is_not_complete(assignment) is False:            #if assignment is complete                      
        if(parks_visited>= n_of_parks):               #constraint
            print('Number of national parks visited: ', parks_visited)   
            return assignment.values()
        else: 
            return False
    
    zone=select_unassigned_variable(assignment)      #getting next zone
    
   
    for state in order_domain_values(initial):                          #possible state from current state
            parks_visited=parks_visited+ parks[state].item()        #total number of park visited, park number added each zone changed
        
            assignment[zone]=state      #adding state value to its zone, so assignment is filled
       
            result=backtrack(state, parks_visited, n_of_parks, assignment)   #iterate umtil z12 anad constraint is met
            
            if(result is not False):                #get the final assignment result
                
                return result
           
            assignment[zone]=None                 #pop the value to get a new value
            parks_visited=parks_visited- parks[state].item()   #pop the visited state park
            
    return False

def main():
        
    a=len(sys.argv)

    if (a<3):
        print('Error: Not enough arguments')

    elif (a>3):
        print('Error: Too many input arguments')

    else:

        
        initial=str(sys.argv[1])
        no_of_parks=int(sys.argv[2])
        zone=zones[initial].item()          #getting the zone of initial state
        
        assignment={}                       #new dict
        assignment[zone]=initial            #giving initial value to the zone in the assignment
        for i in range(zone+1, 13):         #index number represents the zone number
            
                assignment[i]=None
        print
        print('Dashnyam, Mendbayar, A20444643:')
        print('Initial state: ', initial)
        print('Minimum number of parks: ', no_of_parks)
        result=backtrack(initial, parks[initial].item(), no_of_parks, assignment)
        
            
        if result is False:
            print('Solution path: FAILURE: NO PATH FOUND')
            print('Total number of states on a path: ', 0)
        else:
            print('Solution path:', list(result))
            print('Total number of states on a path: ', len(result))
          

if __name__ == "__main__": main()





