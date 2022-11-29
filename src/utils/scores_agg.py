import os
import re
import sys
import tqdm
import numpy as np
import pandas as pd
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

def agg_scores_by_match(scores_file):
    """
    This function performs the aggregation of scores and features at the match level, by team
    :param scores_file: Path to file with raw results from scoring function, along with associated features
    :return: Aggregated scoring and features by match and team
    """
    # Load information based on the analysis provided
    analysis_results = pd.read_csv(scores_file)
    # Group all records by team and by match - This is not the right way of doing this
    match_performance_analysis = analysis_results.groupby(['gameId', 'offTeam']).apply(process_team_perf_match).reset_index(drop=True)
    # Return the analysis result  
    return match_performance_analysis

def agg_scores_by_season(scores_file):
    """
    This function performs the aggregation of scores and features at the season level, by team
    :param scores_file: Path to file with raw results from scoring function, along with associated features
    :return: Aggregated scoring and features by team
    """
    # Load information based on the analysis provided
    analysis_results = pd.read_csv(scores_file)
    # Group all records by team and by match - This is not the right way of doing this
    season_performance_analysis = analysis_results.groupby(['offTeam']).apply(process_team_perf_season).reset_index(drop=True)
    # Return the analysis result  
    return season_performance_analysis

##################################################################################################
# Support functions
def process_team_perf_match(records):
    """
    This function aggregates the features from one single match.
    :param records: Records from one match
    :return: Aggregated scoring and features for this match
    """
    # Create a set of features for each match
    team_match_perf = {
        'gameId': records.gameId,
        'offTeam': records.offTeam,
        'avgPocketScore': records.pocketScore.mean(),
        'cumGainedYards': records.gained_yards.sum(),
        'avgGainedYards': records.gained_yards.mean(),
        'numPassComplete': records.pass_complete.sum(),
        'percPassComplete': (records.pass_complete.sum() / len(records)) * 100.0,
        'numPocketHold': records.has_pocket_hold.sum(),
        'percPocketHold': (records.has_pocket_hold.sum() / len(records)) * 100.0,
        'numQBSacked': records.was_qb_sacked.sum(),
        'percQBSacked': (records.was_qb_sacked.sum() / len(records)) * 100.0,
        'numTouchdowns': records.touchdown.sum(),
        'numOffFouls': records.num_off_foul.sum(),
        'numDefFouls': records.num_def_foul.sum(),
        'numOffInjuries': records.num_off_injuries.sum(),
        'numDefInjuries': records.num_def_injuries.sum()
    }
    performance = pd.DataFrame(team_match_perf).drop_duplicates()
    return performance


def process_team_perf_season(records):
    """
    This function aggregates the features from one season.
    :param records: Records from an entire team's season
    :return: Aggregated scoring and features for this season
    """
    # Create a set of features for each match
    team_match_perf = {
        'offTeam': records.offTeam,
        'avgPocketScore': records.pocketScore.mean(),
        'cumGainedYards': records.gained_yards.sum(),
        'avgGainedYards': records.gained_yards.mean(),
        'numPassComplete': records.pass_complete.sum(),
        'percPassComplete': (records.pass_complete.sum() / len(records)) * 100.0,
        'numPocketHold': records.has_pocket_hold.sum(),
        'percPocketHold': (records.has_pocket_hold.sum() / len(records)) * 100.0,
        'numQBSacked': records.was_qb_sacked.sum(),
        'percQBSacked': (records.was_qb_sacked.sum() / len(records)) * 100.0,
        'numTouchdowns': records.touchdown.sum(),
        'numOffFouls': records.num_off_foul.sum(),
        'numDefFouls': records.num_def_foul.sum(),
        'numOffInjuries': records.num_off_injuries.sum(),
        'numDefInjuries': records.num_def_injuries.sum()
    }
    performance = pd.DataFrame(team_match_perf).drop_duplicates()
    return performance