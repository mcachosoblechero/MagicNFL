import os
import re
import sys
import tqdm
import numpy as np
import pandas as pd
import scipy
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import random
import seaborn as sns

# Libraries required for plotting field
import matplotlib.patches as patches
from matplotlib.patches import Arc
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import animation
from IPython.display import HTML
from IPython import display

def gaussian_field_price(pixel_x, pixel_y, config):

    """
    Function implementing a Gaussian price to the field
    :param pixel_x: Mesh values on the pocket X coordinates 
    :param pixel_y: Mesh values on the pocket Y coordinates
    :param config: Run Parameters 
    :return: Price
    """

    # Calculate Gaussian Distribution
    R = np.sqrt(pixel_x**2 + pixel_y**2)
    Z = np.exp(-( (R-config['pocket_gaus_mu'])**2 / ( 2.0 * config['pocket_gaus_sigma']**2 ) ) )
    
    return Z

def linear_field_price(pixel_x, pixel_y, config):

    """
    Function implementing a Gaussian price to the field
    :param pixel_x: Mesh values on the pocket X coordinates 
    :param pixel_y: Mesh values on the pocket Y coordinates
    :param config: Run Parameters 
    :return: Price
    """

    # Calculate slope
    slope = (config['pocket_linear_max_value'] - 0) / (0 - (-config['pocket_len']/2))

    # Calculate Linear Distribution using the conic approach
    R = np.sqrt(pixel_x**2 + pixel_y**2)
    Z = 1 - slope * R

    # Eliminate negative values
    Z[Z<0] = 0

    return Z