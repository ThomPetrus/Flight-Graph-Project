# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 13:39:45 2021

COSC320 - Analysis of Algorithms - UBCO

Implementation of Algorithm 1 from Milestone 1 for the Project.
An algorithm to determine the best non direct flight based on
flight cost, total flight time and wait time in airports.

@author: tpvan
"""
import sys

MINS_IN_DAY = 1440

class AlgoOne:
    """
    A Class that represenst the algorithm we came up with for Milestone 1
    
    Attributes:
    --------------------------------------------------------------------------------
        graph : FlightGraph
                Networkx graph created from a the dataset we generated from
                the data from the Bureau of Transportation Statistics.
        COST_WEIGHT : int
                The coefficient to multiply the flightCost parameter of a flight by
                when calculatin the cost of an edge.
        FLIGHT_TIME_WEIGHT : int
                The coefficient to multiply the elapsedTime parameter of a flight by
                when calculatin the cost of an edge.
        WAIT_TIME_WEIGHT : int
                The coefficient to multiply the wait time incurred in between flights by
                when calculating the cost of an edge.                .
    ---------------------------------------------------------------------------------
    """
    
    def __init__(self, graph, cost_weight, flight_time_weight, wait_time_weight): 
        """
        Constructs the necessary attributes for the algorithm to run.
        
        Parameters:
        ---------------------------------------------------------------------------------
            graph : FlightGraph
                A FlightGraph Object
            cost_weight : int
                The coefficient to multiply the flightCost parameter of a flight by
                when calculatin the cost of an edge
            flight_time_weight : int
                The coefficient to multiply the elapsedTime parameter of a flight by
                when calculatin the cost of an edge.
            wait_time_weight : int
                The coefficient to multiply the wait time incurred in between flights by
                when calculating the cost of an edge.
        ---------------------------------------------------------------------------------
        """
        self.graph              = graph
        self.COST_WEIGHT        = cost_weight;
        self.FLIGHT_TIME_WEIGHT = flight_time_weight
        self.WAIT_TIME_WEIGHT   = wait_time_weight
    
    def best_flight(self, start, dest):
        """
        Takes the airport codes for start and destination and start the algorithm.
        Then prints output
        
        Parameters:
        ---------------------------------------------------------------------------------
            start : str
                Airport code for start airport
            dest : str
                Airport code for destination airport
        ---------------------------------------------------------------------------------
        """
        self.start = start
        self.dest  = dest
        self.search(start, dest)
        path_list, path_message  = self.process_output()
        
        return path_list, path_message
        
        
    def process_output(self):
        """
        Print output after search is completed.
        """
        
        if self.graph.nodes[self.dest]['prev'] == None:
            print("Search was not completed.")
            return
        
        ptr = self.dest
        total_wait   = 0
        total_cost   = 0
        total_flight = 0
        path_list    = []
        path_message = ""
        
        print("----------------------------------------------------------------------------------------------------------------------------")
        print("Reverse Path : ")
        print("----------------------------------------------------------------------------------------------------------------------------")
        
        while ptr != self.start:
            airport     = list(self.graph.nodes[ptr]['prev'])[0]
            flight_num  = self.graph.nodes[ptr]['prev'][airport]
            flight_data = self.graph.get_edge_data(airport, ptr)[flight_num]
            
            print("From %s to %s : " % (airport, ptr))
            print(flight_data)

            total_wait   += self.graph.nodes[ptr]['wait_time']
            total_cost   += flight_data['flightCost']
            total_flight += flight_data['elapsedTime']
            
            path_list.append(ptr)
            ptr = airport
            
        path_list.append(self.start)
        path_message += "Total Airport Wait Time : {} minutes".format(int(total_wait))
        path_message += " - Total Flight Time : {} minutes".format(int(total_flight))
        path_message += " - Total Cost : ${}.00".format(int(total_cost))
        
        print("----------------------------------------------------------------------------------------------------------------------------")
        print("Total Airport Wait Time : ", total_wait)
        print("Total Flight Time : ", total_flight)
        print("Total Cost : ", total_cost)
        print("----------------------------------------------------------------------------------------------------------------------------")
        
        return path_list, path_message
            
    def get_wait_time(self, prev_airport, prev_flight, next_flight_data):
        """
        Determine the amount of time to wait in an airport based on the arrival time of previous flight
        taken to get to this airport and the departure time for next flight considered
        
        The departure and arrival times are in minutes elapsed since midnight.
        Parameters:
        ---------------------------------------------------------------------------------
            prev_airport : str
                Airport code for previous airport
            prev_flight : dict 
                Dictionary with prev airport code and associated flight_num representing
                the flight or edge
            next_flight_data : dict
                Dictionary presenting the next edge being considered
        
        Returns : int
            The calculated wait time
        ---------------------------------------------------------------------------------
        """
        # Only after more than one flight
        if prev_flight != None:
            
            # get previous flight info 
            prev_airport_name    = list(prev_flight.keys())[0]
            prev_flight_num = prev_flight[prev_airport_name]
            prev_flight_data = self.graph.get_edge_data(prev_airport_name, prev_airport)[prev_flight_num]
            
            # get arrival and departure times for previous flight and next flight respectively
            arr_time      = prev_flight_data['arrTime']
            next_dep_time = next_flight_data['departureTime']
            
            curr_wait_time = next_dep_time - arr_time 
            
            # if it is negative then arrival was after departure + 24 hours
            if curr_wait_time <= 0:
                curr_wait_time = MINS_IN_DAY - (-1) * curr_wait_time
                
            return curr_wait_time
        
        # only for first flight - i.e. arrive immediately when leaving
        return 0
    
    def get_cost(self, flight_data, wait_time):
        """
        Parameters:
        ---------------------------------------------------------------------------------
            flight_data : dict
                Dictionary representing the edge in the graph with all the information of the flight
            wait_time : int
                Wait time calculated in get_wait_time function.
        
        Returns: int 
            A weighted sum of the flight cost, flight duration and wait time incurred at airport.
        ---------------------------------------------------------------------------------            
        """
        return self.COST_WEIGHT * flight_data['flightCost'] + self.FLIGHT_TIME_WEIGHT * flight_data['elapsedTime'] + self.WAIT_TIME_WEIGHT * wait_time
        
        
    def search(self, start, dest):
        """
        Parameters:
        ---------------------------------------------------------------------------------
            start : str
                Airport code of the start airport
            dest : str
                Airport code of the destination airport
        ---------------------------------------------------------------------------------
        """
        # simple list as queue
        queue = []
        
        # add all nodes to queue and set previous to none
        for airport in self.graph.nodes():
            queue.append(airport)
            self.graph.nodes[airport]['prev']      = None
            self.graph.nodes[airport]['cost']      = sys.maxsize
            self.graph.nodes[airport]['wait_time'] = sys.maxsize
        
        # distance to start and wait time is 0
        self.graph.nodes[start]['cost']      = 0
        self.graph.nodes[start]['wait_time'] = 0
        
        # while queue not empty
        while queue:
            
            min_cost        = sys.maxsize
            min_airport     = queue[0]
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
            
        