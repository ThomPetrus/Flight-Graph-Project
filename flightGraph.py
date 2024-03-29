# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 02:48:50 2021

Create the FlightGraph used in our algorithms
Can also generate a vizualization of the flight graph data on a map.

@author: tpvan
"""

import os
import sys
import numpy as np
import pandas as pd
import networkx as nx
import cartopy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

# Data Sets

# for algo test
FLIGHT_DATA     = '/Data/processed/multiFlightData_600k.csv'
LOCATIONS_DATA  = '/Data/processed/airportLocations_600k.csv'

# if you want to see a pretty map in reasonable time
FLIGHT_DATA_FOR_MAP     = '/Data/processed/multiFlightData_single_flight_for_map.csv'
LOCATIONS_DATA_FOR_MAP  = '/Data/processed/airportLocations_single_flight_for_map.csv'

# Columns in flight data set
COL_LIST = ['Origin', 'Dest', 'DepTime', 'DepDelay', 'ArrTime', 'ArrDelay', 'ActualElapsedTime', 'ItinFare']

class FlightGraph:
    """
    A class that creates a networkx graph given our flight data generated from
    the Bureau of Transportation Statistics
    
    Attributes:
    ---------------------------------------------------------------------------------
        routes : pandas dataframe 
            Contains the flight data generated with our notebooks
        locations : pandas dataframe
            Contains airport codes and their latitude and longitude
        flights : list
            The individual flights from the routes dataframe
        origin : list
            All the aiport codes from the origin column in the routes dataframe
        dest : list
            All the airports codes from the destination column in the routes dataframe
        airports : list
            All the origin and destination codes combined
    ---------------------------------------------------------------------------------            
    """
    
    def __init__(self): 
        """
        Initializes the class attributes used in the creation of the graph and
        calls the create graph function.
        
        Parameters: defined globally
        ---------------------------------------------------------------------------------
            FLIGHT_DATA : str
                Path to flight dataset csv. Generated by the MultiFlight dataset jupyter notebook
            LOCATIONS_DATA : str
                Path to locations dataset of airport codes and lattitude and longitudes
            COL_LIST : list
                List of all the columns in the flight dataset
        ---------------------------------------------------------------------------------
        """    
        self.routes      = pd.read_csv(os.getcwd() + FLIGHT_DATA)
        self.locations   = pd.read_csv(os.getcwd() + LOCATIONS_DATA)
        self.flights     = self.routes[COL_LIST].values
        self.origin      = self.routes['Origin'].tolist()
        self.dest        = self.routes['Dest'].tolist()
        self.airports    = np.unique(self.origin + self.dest)    
        self.create_graph()
    
    def create_graph(self):
        """
        Constructs the networkx graph from the data in our dataset.
        
        Returns: nx.MultiDiGraph
            Graph of flight data
        ---------------------------------------------------------------------------------            
        """
        self.G = nx.MultiDiGraph();
        for flight in self.flights:
            self.G.add_edge(
                    flight[0],      # u
                    flight[1],      # v
                    origin          = flight[0],
                    dest            = flight[1],
                    departureTime   = flight[2],
                    departureDelay  = flight[3],
                    arrTime         = flight[4],
                    arrDelay        = flight[5],
                    elapsedTime     = flight[6],
                    flightCost      = flight[7])
            
        for airport in self.G.nodes():
            self.G.nodes[airport]['prev']      = None
            self.G.nodes[airport]['cost']      = sys.maxsize
            self.G.nodes[airport]['wait_time'] = sys.maxsize
        
        return self.G
    
    def plot_graph(self):
        """
        Plot graph without context - just a mess of nodes and edges
        """
        fig, ax = plt.subplots(1, 1, figsize=(6, 6))
        nx.draw_networkx(self.G, ax=ax, with_labels=True, node_size=5, width=.5)
        ax.set_axis_off()
        
    def plot_map(self, full=False, all_labels=False):
        """
        Plot graph on map of United States.
        
        Parameters:
        ---------------------------------------------------------------------------------
            full : boolean
                Whether or not to print the full map or only the map representing majority of nodes.
        ---------------------------------------------------------------------------------
        """
        # create position dict - airport code : latitude, longitude 
        pos = {
           airport['Origin']: (airport['Long'], airport['Lat']) 
           for index, airport in self.locations.to_dict('index').items()
         }
    
        # size of nodes is proportional to the in-degree of the node
        deg = nx.degree(self.G)
        sizes = [deg[iata]/4 for iata in self.G.nodes]
        
        # only show labels on airports with in-degree greater than 5% of flights
        labels = {iata: iata if deg[iata] >= (len(self.flights) / 20) else ''
                  for iata in self.G.nodes}
        
        if all_labels:
            labels = {iata: iata 
                  for iata in self.G.nodes}
        
        # create map
        crs = ccrs.PlateCarree()
        fig, ax = plt.subplots(1, 1, figsize=(20, 20), subplot_kw=dict(projection=crs))   
        ax.add_feature(cartopy.feature.BORDERS, linestyle=':', alpha=1)
        ax.add_feature(cartopy.feature.OCEAN,facecolor=("lightblue"))
        ax.add_feature(cartopy.feature.LAND)
        ax.add_feature(cartopy.feature.LAKES)
        ax.coastlines()
        
        # whether or not to show full mape
        if full:
            # Full US -> include Hawaii
            ax.set_extent([-170, -62, 5, 50])
        else:
            # Extent of continental US
            ax.set_extent([-128, -62, 20, 50])
        
        # create graph on map
        nx.draw_networkx(self.G, ax=ax,
                         font_size=16,
                         alpha=.9,
                         width=.075,
                         pos=pos,
                         node_size=sizes,
                         labels=labels,
                         cmap=plt.cm.autumn)
        
    def print_locations(self):
        """
        Prints all the location airport codes
        """
        self.msg('Airports')
        count = 0
        for index, airport in self.locations['Origin'].sort_values().items():
            print(airport + ", ", end="", flush=True)
            count+=1
            if count > 24:
                count = 0
                print("\n")
        print("\n")
                
        
    def get_input(self):
        """
        Get start and destination airport codes from user.
        """
        self.print_locations();
        
        start = ""
        dest  = ""
        while start not in self.locations['Origin'].values:
            start = self.format_input("Enter Start Airport:")
        
        while dest not in self.locations['Origin'].values:
            dest = self.format_input("Enter Destination Airport:")
            
        return start, dest

    def print_path_map(self, path, full=False, path_message=""):
        
        path = list(reversed(path))
        print(path)
        
        # create position dict - airport code : latitude, longitude 
        pos = {
           airport['Origin']: (airport['Long'], airport['Lat']) 
           for index, airport in self.locations.to_dict('index').items()
         }
    
        # only show labels on airports with in-degree greater than 10% of flights
        labels = {iata: iata for iata in path}
        
        # create map
        crs = ccrs.PlateCarree()
        fig, ax = plt.subplots(1, 1, figsize=(20, 20), subplot_kw=dict(projection=crs))
        ax.add_feature(cartopy.feature.BORDERS, linestyle=':', alpha=1)
        ax.add_feature(cartopy.feature.OCEAN,facecolor=("lightblue"))
        ax.add_feature(cartopy.feature.LAND)
        ax.add_feature(cartopy.feature.LAKES)
        plt.annotate(path_message,(0, 0), (300, -20), xycoords='axes fraction', textcoords='offset points', va='top')
        ax.coastlines()
        
        # whether or not to show full mape
        if full:
            # Full US -> include Hawaii
            ax.set_extent([-170, -62, 5, 50])
        else:
            # Extent of continental US
            ax.set_extent([-128, -62, 20, 50])
        
        path_graph = nx.DiGraph()
        for i in range(len(path) - 1):
            path_graph.add_edge(path[i], path[i + 1])
        
        # create graph on map
        nx.draw_networkx(path_graph, ax=ax,
                         font_size=16,
                         alpha=.9,
                         width=2,
                         pos=pos,
                         node_size=500,
                         labels=labels,
                         cmap=plt.cm.autumn)

    def msg(self, msg):
        print("----------------------------------------------------------------------------------------------------------------------------")
        print(msg)
        print("----------------------------------------------------------------------------------------------------------------------------")
        
    def format_input(self, msg):
        print("----------------------------------------------------------------------------------------------------------------------------")
        ans = input(msg)
        return ans
        
def main():
    fg = FlightGraph()
    #fg.plot_graph()
    fg.plot_map(True, True)
  
if __name__ == "__main__":
    main();
    
    
    