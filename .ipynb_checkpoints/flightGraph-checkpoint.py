# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 02:48:50 2021

@author: tpvan
"""

import math
import json
import numpy as np
import pandas as pd
import networkx as nx
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from IPython.display import Image
%matplotlib inline
import os

routes = pd.read_csv(os.getcwd() + '\\Data\\processed\\flightData.csv')
edges = routes[['Origin', 'Dest']].values
g = nx.from_edgelist(edges)

fig, ax = plt.subplots(1, 1, figsize=(6, 6))
nx.draw_networkx(g, ax=ax, node_size=5,
                 font_size=6, alpha=.5,
                 width=.5)
ax.set_axis_off()