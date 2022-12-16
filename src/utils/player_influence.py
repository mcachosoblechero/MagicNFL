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


def gaussian_player_influence_score(player_x, player_y, pixel_x, pixel_y, config):

    '''
    This function calculates the player influence using the gaussian function
    The thresholding function is the numpy implementation of MAX
    :param player_x: Player X coordinates 
    :param player_y: Player Y coordinates 
    :param pixel_x: Mesh values on the pocket X coordinates 
    :param pixel_y: Mesh values on the pocket Y coordinates 
    :param config: Run Parameters 
    :return: Player influence value
    '''

    # Determine the relative position of the pixel from the player
    X = player_x - pixel_x
    Y = player_y - pixel_y

    # Calculate Gaussian Distribution
    R = np.sqrt(X**2 + Y**2)
    Z = np.exp(-( (R-config['gaus_mu'])**2 / ( 2.0 * config['gaus_sigma']**2 ) ) )
    
    return Z

def extract_play_players_influence(team_def, infl_funct, config):

    '''
    This function calculates the player influence for a play
    :param team_def: DataFrame with defensive team information for this play
    :param infl_funct: Influence function to use
    :param config: Run Parameters 
    :return: Mesh values with player influence scores for all frames on this play
    '''

    # Create a mesh of values
    pocket_pos_start = -(config['pocket_len']/2)
    pocket_pos_end = (config['pocket_len']/2)
    x = np.arange(pocket_pos_start, pocket_pos_end, config['pocket_res'])
    y = np.arange(pocket_pos_start, pocket_pos_end, config['pocket_res'])
    x, y = np.meshgrid(x, y)

    # For all frames, calculate scores
    num_frames = team_def.frameId.max()
    array_dimension = x.shape
    scores = np.empty((num_frames, array_dimension[0], array_dimension[1]))
    for frame in range(num_frames):
        scores[frame, :, :] = calculate_grid_score(x, y, frame+1, team_def=team_def, infl_funct=infl_funct, config=config)

    return scores

def calculate_grid_score(pixel_x, pixel_y, frameId, team_def, infl_funct, config):

    '''
    This function calculates the grid scope for an specific frame, given a specific influence function
    The thresholding function is the numpy implementation of MAX
    :param pixel_x: Mesh values on the pocket X coordinates 
    :param pixel_y: Mesh values on the pocket Y coordinates 
    :param frameId: Value of the current frame
    :param team_def: DataFrame with defensive team information
    :param infl_funct: Influence function to use
    :param config: Run Parameters 
    :return: Mesh values with score results for frame frameId
    '''
 
    # Extract frame information
    defense = team_def.loc[team_def.frameId == frameId]
        
    # For each player, obtain the score
    dimensions = pixel_x.shape
    frame_scores = np.zeros((dimensions[0], dimensions[1], len(defense)))
    for idx,(_, def_player) in enumerate(defense.iterrows()):
        
        frame_scores[:,:,idx] = infl_funct(
            player_x=def_player.x,
            player_y=def_player.y,
            pixel_x=pixel_x,
            pixel_y=pixel_y,
            config=config
        )

    # At the end of this calculation, only maintain the maximum one
    return frame_scores.max(axis=2)