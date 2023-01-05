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

def calculate_defense_score(players_influence, field_price):

    """
    Calculate score based on the players influence and field price.
    For now, I am making the average - this is not the only possible approach, we need to explore more
    :param players_influence: Players influence scores for all frames
    :param field_price: Field Price Array
    :return: Pocket Score
    """

    return np.sum(np.sum(np.multiply(players_influence, field_price), axis=2), axis=1)


def calculate_qb_score(team1, config):
    """
    Calculate the additional score due to QB being outside the pocket
    :param team1: Information regarding team 1
    :param config: Run parameters
    :return: QB OOP Score
    """

    return 0