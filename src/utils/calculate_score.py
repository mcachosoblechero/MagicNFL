import os
import re
import sys
import tqdm
import math
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


def calculate_qb_score(team1, ball, input_path, config):
    """
    Calculate the additional score due to QB being outside the pocket
    This score adds penalty scores for every frame the QB is outside of the pocket
    :param team1: Information regarding team 1
    :param config: Run parameters
    :return: QB OOP Score
    """

    # Determine the pocket size
    pocket_pos_length = (config['pocket_len']/2)

    # Extract which team member from the offensive team is the QB
    # - Obtain list of players
    list_players = team1.nflId.unique().tolist()
    # - Extract QB ID
    qb_id = pd.read_csv(os.path.join(input_path, 'players.csv')).query("nflId == @list_players & officialPosition == 'QB'")

    # - Run certain checks - QB available and only one QB
    # - If an error is raised, we look for the QB
    if (qb_id.empty) | (len(qb_id) > 1):

        # - Determine the moment the ball was snapped
        frame_snap = ball.loc[ball.event == 'ball_snap', 'frameId'].values[0] + config['post_snap_time']

        # - Extract information regarding relative position of players from ball
        ball_pos = ball.loc[ball.frameId == frame_snap, ['x', 'y', 'event']]
        dist_players = team1.loc[team1.frameId == frame_snap, ['nflId', 'x', 'y']]

        # - Determine which player has the ball in frame frame_qb
        dist_players['abs_distance'] = dist_players.apply(lambda player: math.sqrt((player.x - ball_pos.x)**2 + (player.y - ball_pos.y)**2), axis=1)
        qb_id = dist_players.loc[dist_players.abs_distance == min(dist_players.abs_distance), 'nflId'].values[0]

    else:
        # If everything is ok, move on
        qb_id = qb_id.nflId.values.flatten()[0]

    # Extract QB positions across the different frames
    qb_ref = team1.loc[team1.nflId == qb_id, ['frameId', 'x', 'y']]

    # Determine whether QB is Out-of-Pocket (OOP)
    qb_oop_score = 0
    frameIds = ball.frameId.unique()
    for frameId in frameIds:
        ref_x, ref_y = qb_ref.loc[qb_ref.frameId == frameId, ['x', 'y']].values[0]
        dist_to_center = np.sqrt(ref_x**2 + ref_y**2)
        
        # If QB is OOP, add QB OOP score
        if (dist_to_center > pocket_pos_length):
            dist_outside_pocket = dist_to_center - pocket_pos_length
            qb_oop_score += config['qb_oop_infl_funct'](dist_outside_pocket, config)
    
    return qb_oop_score