# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 13:39:45 2021

@author: tpvan
"""
import sys

class AlgoOne:
    
    def __init__(self, graph): 
        self.graph = graph
    
    def best_flight(self, start, dest):
        #search
        prev = self.search(start, dest)
        
        # get path    
        ptr = dest
        while ptr != start:
            airport     = list(prev[ptr].keys())[0]
            flight_num  = prev[ptr][airport]
            
            print("From %s to %s : " % (airport, ptr))
            print(self.graph.get_edge_data(airport, ptr)[flight_num])
    
            ptr = airport
        
    
    def get_cost(self, flight_data):
        #TODO: real cost function
        return flight_data['flightCost']
        
        
    def search(self, start, dest):
        
        prev        = {}
        queue       = []
        
        # add to queue
        for airport in self.graph.nodes():
            queue.append(airport)
            prev[airport] = None;
        
        # distance to start is 0
        self.graph.nodes[start]['cost'] = 0
        
        # while queue not empty
        while queue:
            
            min_cost        = sys.maxsize
            min_airport     = None
            current_airport = None
            
            # iterate over queue and get min cost node
            # will be start node on first iteration
            for i in range(len(queue)):
                current_airport = queue[i]
                current_airport_cost = self.graph.nodes[current_airport]['cost']
                if current_airport_cost < min_cost:
                    min_cost    = current_airport_cost
                    min_airport = current_airport

            # dequeue min element
            queue.remove(min_airport)        
            
            # for each of the neighgboring airports of dequeued element
            for neighbor in self.graph.adj[min_airport]:
                # if neighbor has not been visited 
                if neighbor in queue:
                    
                    # get all flights between airport and neighbor
                    flights = self.graph.get_edge_data(min_airport, neighbor)
                    flight_num = 0
                    
                    for flight in flights:
                        
                        # get flight data
                        flight_data = flights[flight]
                        
                        # check poth cost from current airport to neighbor with this flight
                        alt_path_cost = self.graph.nodes[min_airport]['cost'] + self.get_cost(flight_data)
                    
                        # if it is better then update neighbor cost and prev list
                        if alt_path_cost < self.graph.nodes[neighbor]['cost']:
                            self.graph.nodes[neighbor]['cost'] = alt_path_cost
                            prev[neighbor] = {min_airport:flight_num}
                        flight_num+=1
            
        
        return prev
                
                
        
                
                
                
                
             
        
        #for airports in self.graph.edges([current_airport]):
        
    
    
        