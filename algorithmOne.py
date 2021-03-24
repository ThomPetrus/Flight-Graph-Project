# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 13:39:45 2021

@author: tpvan
"""
import sys

class AlgoOne:
    
    def __init__(self, graph): 
        self.graph              = graph
        self.COST_WEIGHT        = 0.25
        self.FLIGHT_TIME_WEIGHT = 0.25
        self.WAIT_TIME_WEIGHT   = 0.5
    
    def best_flight(self, start, dest):
        # if search successful
        self.search(start, dest)
       
        ptr = dest
        total_wait   = 0
        total_cost   = 0
        total_flight = 0
    
        print("-----------------------------------------------")
        print("Reverse Path : ")
        print("-----------------------------------------------")
        # get path    
        while ptr != start:
            airport     = list(self.graph.nodes[ptr]['prev'])[0]
            flight_num  = self.graph.nodes[ptr]['prev'][airport]
            flight_data = self.graph.get_edge_data(airport, ptr)[flight_num]
            
            print("From %s to %s : " % (airport, ptr))
            print(flight_data)

            total_wait   += self.graph.nodes[ptr]['wait_time']
            total_cost   += flight_data['flightCost']
            total_flight += flight_data['elapsedTime']
            ptr = airport
            print("-----------------------------------------------")
        
        print("Total Airport Wait Time : ", total_wait)
        print("Total Flight Time : ", total_flight)
        print("Total Cost : ", total_cost)
        print("-----------------------------------------------")
            
    def get_wait_time(self, prev_airport, prev_flight, next_flight_data):
        
        # Only after more than one flight
        #print(prev_flight) # uncomment to see
        if prev_flight != None:
            
            # get previous flight info 
            prev_airport_name    = list(prev_flight.keys())[0]
            prev_flight_num = prev_flight[prev_airport_name]
            prev_flight_data = self.graph.get_edge_data(prev_airport_name, prev_airport)[prev_flight_num]
    
            # toxic print out tracing all flights
            #print('Previous Flight')
            #print(prev_flight_data)
            #print('Current Flight')
            #print(next_flight_data)
            
            # get arrival and departure times for previous flight and next flight respectively
            arr_time      = prev_flight_data['arrTime']
            next_dep_time = next_flight_data['departureTime']
            curr_wait_time = next_dep_time - arr_time 
            
            # if it is negative then arrival was after departure + 24 hours
            if curr_wait_time < 0:
                curr_wait_time = 2400 - (-1) * curr_wait_time
                
            return curr_wait_time
        
        # only for first flight - i.e. arrive when leaving
        return 0
    
    
    def get_cost(self, flight_data, wait_time):
        """
        Parameters:
            TODO:docs
        Returns:
            int:a weighted sum of the flight cost, flight duration and wait time incurred at airport.
        """
        return self.COST_WEIGHT * flight_data['flightCost'] + self.FLIGHT_TIME_WEIGHT * flight_data['elapsedTime'] + self.WAIT_TIME_WEIGHT * wait_time
        
        
    def search(self, start, dest):
        
        # simple list as queue
        queue = []
        
        # add all nodes to queue and set previous to none
        for airport in self.graph.nodes():
            queue.append(airport)
            self.graph.nodes[airport]['prev']   = None;
        
        # distance to start and wait time is 0
        self.graph.nodes[start]['cost']      = 0
        self.graph.nodes[start]['wait_time'] = 0
        
        # while queue not empty
        while queue:
            
            min_cost        = sys.maxsize
            min_airport     = None
            current_airport = None
            
            # iterate over queue and get min cost node
            # will be start node on first iteration
            for i in range(len(queue)):
                current_airport      = queue[i]
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
                    
                    # get all flights between airport and neighbor - MultiDiGraph - multiple edges
                    flights = self.graph.get_edge_data(min_airport, neighbor)
                    flight_num = 0
                    
                    # for each flight
                    for flight in flights:
                        
                        # don't add direct flights
                        if min_airport == start and neighbor == dest: 
                            continue
                        
                        # get flight data
                        flight_data = flights[flight]
                        
                        # check wait time for this flight considering flight taken to get here
                        alt_path_wait_time = self.graph.nodes[min_airport]['wait_time'] + self.get_wait_time(min_airport, self.graph.nodes[min_airport]['prev'], flight_data)
                        
                        # check poth cost from current airport to neighbor with this flight also considering wait time
                        alt_path_cost = self.graph.nodes[min_airport]['cost'] + self.get_cost(flight_data, alt_path_wait_time)
                        
                        # if it is better then update neighbor cost and prev list
                        if alt_path_cost < self.graph.nodes[neighbor]['cost']:
                            self.graph.nodes[neighbor]['cost'] = alt_path_cost
                            self.graph.nodes[neighbor]['wait_time'] = alt_path_wait_time
                            self.graph.nodes[neighbor]['prev'] = {min_airport:flight_num}
                            
                        flight_num+=1
            
        