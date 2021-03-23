# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 02:48:50 2021

Generates a vizualization of the flight graph data.

@author: tpvan
"""

import os
import sys
import numpy as np
import pandas as pd
import networkx as nx
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from IPython.display import Image

FLIGHT_DATA     = '/Data/processed/multiFlightData.csv'
LOCATIONS_DATA  = '/Data/processed/airportLocations.csv'
EDGES = ['Origin', 'Dest', 'DepTime', 'DepDelay', 'ArrTime', 'ArrDelay', 'ActualElapsedTime', 'ItinFare']

class flightGraph:
    def __init__(self): 
        self.load_data()
    
    def load_data(self):
        self.routes      = pd.read_csv(os.getcwd() + FLIGHT_DATA)
        self.locations   = pd.read_csv(os.getcwd() + LOCATIONS_DATA)
        self.flights     = self.routes[EDGES].values
        self.origin      = self.routes['Origin'].tolist()
        self.dest        = self.routes['Dest'].tolist()
        self.airports    = np.unique(self.origin + self.dest)

    
    def create_graph(self):
        self.G = nx.MultiDiGraph();
        
        for flight in self.flights:
            self.G.add_edge(
                    flight[0],      # u
                    flight[1],      # v
                    departureTime   = flight[2],
                    departureDelay  = flight[3],
                    arrTime         = flight[4],
                    arrDelay        = flight[5],
                    elapsedTime     = flight[6],
                    flightCost      = flight[7])
            self.G.nodes[flight[0]]['cost'] = sys.maxsize
            self.G.nodes[flight[1]]['cost'] = sys.maxsize
        
        return self.G
    
    def plot_graph(self):
        fig, ax = plt.subplots(1, 1, figsize=(6, 6))
        nx.draw_networkx(self.G, ax=ax, with_labels=True, node_size=5, width=.5)
        ax.set_axis_off()
        
    def plot_map(self):
        
        pos = {
           airport['Origin']: (airport['Long'], airport['Lat']) 
           for index, airport in self.locations.to_dict('index').items()
         }
    
        deg = nx.degree(self.G)
        sizes = [deg[iata] for iata in self.G.nodes]
        
        labels = {iata: iata if deg[iata] >= 200 else ''
                  for iata in self.G.nodes}
        
        crs = ccrs.PlateCarree()
        fig, ax = plt.subplots(1, 1, figsize=(20, 20), subplot_kw=dict(projection=crs))
        ax.coastlines()
        
        # Extent of continental US.
        ax.set_extent([-128, -62, 20, 50])
        
        # Full US -> include Hawaii
        #ax.set_extent([-170, -62, 5, 50])
        
        nx.draw_networkx(self.G, ax=ax,
                         font_size=16,
                         alpha=.9,
                         width=.075,
                         pos=pos,
                         node_size=sizes,
                         labels=labels,
                         cmap=plt.cm.autumn)
        
    def print_locations(self):
        for index, airport in self.locations['Origin'].sort_values().items():
            print(airport)
        
    def get_input(self):
        #TODO: prettify print out of airports
        #print("Airports\n----------------")
        #self.print_locations();
        
        start = ""
        dest  = ""
        while start not in self.locations['Origin'].values:
            start = input("Enter Start Airport:")
        
        while dest not in self.locations['Origin'].values:
            dest = input("Enter Destination Airport:")
            
        return start, dest


def main():
    fg = flightGraph()
    fg.create_graph()
    fg.plot_graph()
    fg.plot_map()
  
if __name__ == "__main__":
    main();







#print paths and costs

#for path in nx.all_simple_edge_paths(g, "MSP", "CLE") :
#      print(path)
