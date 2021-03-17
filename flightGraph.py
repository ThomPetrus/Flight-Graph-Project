# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 02:48:50 2021

Generates a vizualization of the flight graph data.

@author: tpvan
"""

import math
import json
import os
import numpy as np
import pandas as pd
import networkx as nx
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from IPython.display import Image

FLIGHT_DATA     = '/Data/processed/multiFlightData.csv'
LOCATIONS_DATA  = '/Data/processed/airportLocations.csv'
EDGES = ['Origin', 'Dest', 'ItinFare', 'DepTime', 'ArrTime', 'DepDelay', 'ArrDelay', 'ActualElapsedTime']

def load_data():
    routes      = pd.read_csv(os.getcwd() + FLIGHT_DATA)
    locations   = pd.read_csv(os.getcwd() + LOCATIONS_DATA)
    edges       = routes[EDGES].values
    return routes, locations, edges

def create_graph(nodes, routes, locations, edges):
    g = nx.DiGraph();
    for node in nodes:
        g.add_node(node)
    
    
    for edge in edges:
        g.add_edge(
                edge[0],
                edge[1],
                totalCost = edge[2],
                departureDelay = edge[3],
                arrivalDelay = edge[4],
                totalTime = edge[5])
    return g

def plot_graph(g):
    fig, ax = plt.subplots(1, 1, figsize=(6, 6))
    nx.draw_networkx(g, ax=ax, with_labels=True, node_size=5, width=.5)
    ax.set_axis_off()
    
def plot_map(g, locations):
    pos = {
       airport['Origin']: (airport['Long'], airport['Lat']) 
       for index, airport in locations.to_dict('index').items()
     }

    deg = nx.degree(g)
    sizes = [5 * deg[iata] for iata in g.nodes]
    
    labels = {iata: iata if deg[iata] >= 50 else ''
              for iata in g.nodes}
    
    crs = ccrs.PlateCarree()
    fig, ax = plt.subplots(1, 1, figsize=(20, 20), subplot_kw=dict(projection=crs))
    ax.coastlines()
    
    # Extent of continental US.
    ax.set_extent([-128, -62, 20, 50])
    
    # Full US -> include Hawaii
    #ax.set_extent([-170, -62, 5, 50])
    
    nx.draw_networkx(g, ax=ax,
                     font_size=16,
                     alpha=.9,
                     width=.075,
                     pos=pos,
                     node_size=sizes,
                     labels=labels,
                     cmap=plt.cm.autumn)


def main():
    routes, locations, edges = load_data()
    origin  = routes['Origin'].tolist()
    dest    = routes['Dest'].tolist()
    nodes   = np.unique(origin+dest)
    g = create_graph(nodes, routes, locations, edges)
    plot_graph(g)
    plot_map(g, locations)
  
if __name__ == "__main__":
    main();







#print paths and costs

#for path in nx.all_simple_edge_paths(g, "MSP", "CLE") :
#      print(path)
