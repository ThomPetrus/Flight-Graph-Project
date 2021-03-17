# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 13:33:58 2021

@author: tpvan
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 02:48:50 2021

Generates a vizualization of the flight graph data.

@author: tpvan
"""

from algorithmOne import AlgoOne
from flightGraph import flightGraph

def main():
    algo = AlgoOne()
    algo.printhi()
    fg = flightGraph()
    fg.create_graph()
    fg.plot_graph()
    fg.plot_map()
  
if __name__ == "__main__":
    main();







#print paths and costs

#for path in nx.all_simple_edge_paths(g, "MSP", "CLE") :
#      print(path)
