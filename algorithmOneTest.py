# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 13:33:58 2021

@author: tpvan
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 02:48:50 2021

@author: tpvan
"""

from algorithmOne import AlgoOne
from flightGraph import flightGraph

def main():
    fg = flightGraph()
    graph = fg.create_graph()    
    
    start, dest = fg.get_input()
    algo = AlgoOne(graph)
    algo.best_flight(start, dest)
    
  
if __name__ == "__main__":
    main();

