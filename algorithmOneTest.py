# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 13:33:58 2021

@author: tpvan
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 02:48:50 2021

RUN THIS FILE

The test file to create the graph with our data set and run the algorithm

@author: tpvan
"""

from algorithmOne import AlgoOne
from flightGraph import FlightGraph
import time

# set weights here
COST_WEIGHT        = 0.25
FLIGHT_TIME_WEIGHT = 0.25
WAIT_TIME_WEIGHT   = 0.5

def main():
    
    fg = FlightGraph()
    graph = fg.create_graph()    
    start, dest = fg.get_input()
    
    start_time = time.time()
    algo = AlgoOne(graph, COST_WEIGHT, FLIGHT_TIME_WEIGHT, WAIT_TIME_WEIGHT)
    path_list, path_message = algo.best_flight(start, dest)
    print("--- %s seconds ---" % (time.time() - start_time))
    
    fg.print_path_map(path_list, False, path_message)
    
    
if __name__ == "__main__":
    main();

