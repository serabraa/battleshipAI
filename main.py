import numpy as np
import random
import matplotlib
matplotlib.use('TkAgg')  # Set the backend before importing pyplot

grid_size = 7;
ship_sizes = [5,3,2,2]
ships = [
    {'size': 3, 'hits': 0, 'placement': (0, 0, 'H')},
    {'size': 2, 'hits': 0, 'placement': (2, 2, 'V')},
    {'size': 2, 'hits': 0, 'placement': (4, 4, 'V')},
    {'size': 5, 'hits': 0, 'placement': (1, 6, 'V')},

]
num_test_simulations_efficient = 100000








