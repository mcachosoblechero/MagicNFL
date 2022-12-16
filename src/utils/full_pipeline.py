import os
import re
import sys
import tqdm
import random
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# Libraries required for plotting field
import matplotlib.patches as patches
from matplotlib.patches import Arc
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import animation
from IPython.display import HTML
from IPython import display

from src.utils.play_preprocessing import extractPlay, preprocessPlay_refQB_NFrames
from src.utils.feature_extraction import extract_formation_features, extract_foul_features, extract_injury_features, extract_play_outcome_features
from src.utils.scores_agg import agg_scores_by_match, agg_scores_by_season
from src.utils.evaluate_scores import evaluate_singleplay_scores, evaluate_agg_scores

def run_full_pipeline(input_path, output_path, config, score_funct):

    features_file = f"{output_path}/play_features.csv"
    scores_and_features_file = f"{output_path}/play_scores_and_features.csv"
    match_scores_file = f"{output_path}/match_scores_and_features.csv"
    season_scores_file = f"{output_path}/season_scores_and_features.csv"

    ##########################################
    # STEP 1 - CREATE FEATURE VECTOR         #
    ########################################## 
    # Load information regarding plays
    plays_data = pd.read_csv(os.path.join(input_path, 'plays.csv'))

    # Perform all feature extractions
    plays_outcomes = extract_play_outcome_features(plays_data).set_index(['gameId', 'playId'])
    plays_formation = extract_formation_features(plays_data).set_index(['gameId', 'playId'])
    plays_fouls = extract_foul_features(plays_data).set_index(['gameId', 'playId'])
    plays_injury = extract_injury_features(plays_data).set_index(['gameId', 'playId'])

    # Merge all these tables into one single big table
    play_features = pd.concat([plays_outcomes, plays_formation, plays_fouls, plays_injury], axis=1)
    play_features.to_csv(features_file)

    ##########################################
    # STEP 2 - PREPROCESS ALL PLAYS          #
    ########################################## 
    # Define number of weeks to analyize
    num_weeks = 8

    # Generate files names
    week_files = []
    for i in range(num_weeks):
        week_files.append(f'week{i+1}.csv')

    # For all weeks, extract scores
    all_scores_info = []
    for week_file in week_files:

        print(f"- Analyzing {week_file}")

        # Load information for an entire week
        week_data = pd.read_csv(os.path.join(input_path, week_file))

        # Extract information about the associated games and plays
        unique_ids = week_data[['gameId', 'playId']].drop_duplicates().values

        for gameId, playId in tqdm.tqdm(unique_ids):

            # Extract info from the play
            team1, team2, ball = extractPlay(week_data, gameId, playId)
            team1, team2, ball = preprocessPlay_refQB_NFrames(team1, team2, ball, delay_frame=config['hold_QB_ref'])

            # # Obtain the score based on the function
            # pocketScore = score_funct(team1, team2, ball)
            ############################################################
            # For now, we will include random values
            pocketScore = random.uniform(0, 1)
            ############################################################

            all_scores_info.append({
                'gameId': gameId,
                'playId': playId,
                'offTeam': team1.team.drop_duplicates().values[0],
                'pocketScore': pocketScore 
            })

    # Merge scores with play features
    scores = pd.DataFrame(all_scores_info).set_index(['gameId', 'playId'])
    play_scores_and_features =  pd.concat([scores, plays_outcomes, plays_formation, plays_fouls, plays_injury], axis=1)
    play_scores_and_features.to_csv(scores_and_features_file)

    ##########################################
    # STEP 3 - ANALYZE THE RESULTS           #
    ########################################## 
    # Perform analysis by Single Play
    evaluate_singleplay_scores(scores_and_features_file)

    # Aggregate by match
    result = agg_scores_by_match(scores_and_features_file)
    result.to_csv(match_scores_file)

    # Perform analysis by Match
    evaluate_agg_scores(match_scores_file)

    # Aggregate by season
    season_result = agg_scores_by_season(scores_and_features_file)
    season_result.to_csv(season_scores_file)

    # Perform analysis by Match
    evaluate_agg_scores(season_scores_file)