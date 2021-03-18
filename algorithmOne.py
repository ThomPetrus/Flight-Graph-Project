# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 13:39:45 2021

@author: tpvan
"""
from queue import Queue

class AlgoOne:
    
    def __init__(self, graph): 
        self.graph = graph
    
    def best_flight(self, start, dest):
        #search
        self.search(start, dest)
        # get path
        
    def search(self, start, dest):
        distances   = {}
        path        = {}
        queue       = Queue()
    
        distances[start] = 0;
        path[start]      = start
        queue.put(start)
        
        #for node in list(self.graph.edges().data()):
        #    print(node)
        
        while not queue.empty():
            current_airport = queue.get()
            
            for edge in self.graph.edges([current_airport]):
                origin_airport  = edge[0]
                dest_airport    = edge[1]
                flights_data     = self.graph.get_edge_data(edge[0], edge[1])
                
                
                
            
            
        
        
        
    
    
        