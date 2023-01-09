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
from src.utils.feature_extraction import extract_formation_features, extract_foul_features, extract_injury_features, extract_play_outcome_features, extract_game_features, extract_did_qb_stay_in_pocket, determine_pocket_outcome
from src.utils.scores_agg import agg_scores_by_match, agg_scores_by_season
from src.utils.evaluate_scores import evaluate_singleplay_scores, evaluate_match_scores, evaluate_season_scores, evaluate_time_series_score
from src.utils.player_influence import extract_play_players_influence, gaussian_player_influence_score
from src.utils.field_price_functions import calculate_field_price, gaussian_field_price
from src.utils.calculate_score import calculate_defense_score, calculate_qb_score

def run_short_pipeline(input_path, output_path, plays, config, timeseries_plots = True, runId = "generic"):
    """
    This function performs all operations required for the pipeline execution, limited to a provided plays. 
    All operations are parametrized through CONFIG
    This pipeline performs the following operations:
    1- Extract features
    2- Process provided plays and extract their pocket scores
    3- Correlate features with pocket score
    :param input_path: Input path to raw data
    :param plays: Dataframe of (weekId, gameId, playId) to analyze
    :param output_path: Path for processed datasets
    :param config: Run Parameters
    :param timeseries_plots: Boolean determining whether to plot the individual time series
    :param runId: ID to identify each run 
    """

    play_features_file = f"{output_path}/play_features_{runId}.csv"
    game_features_file = f"{output_path}/game_features_{runId}.csv"
    scores_and_features_file = f"{output_path}/play_scores_and_features_{runId}.csv"
    match_scores_file = f"{output_path}/match_scores_and_features_{runId}.csv"
    season_scores_file = f"{output_path}/season_scores_and_features_{runId}.csv"

    ##########################################
    # STEP 1 - CREATE FEATURE VECTOR         #
    ########################################## 
    # Load information regarding plays
    plays_data = pd.read_csv(os.path.join(input_path, 'plays.csv'))

    # Extract whether qb stayed in pocket for a single play
    plays_qb_in_pocket = pd.DataFrame()

    # Perform all play feature extractions
    plays_outcomes = extract_play_outcome_features(plays_data).set_index(['gameId', 'playId'])
    plays_formation = extract_formation_features(plays_data).set_index(['gameId', 'playId'])
    plays_fouls = extract_foul_features(plays_data).set_index(['gameId', 'playId'])
    plays_injury = extract_injury_features(plays_data).set_index(['gameId', 'playId'])

    # Merge all these tables into one single big table
    play_features = pd.concat([plays_outcomes, plays_formation, plays_fouls, plays_injury, plays_qb_in_pocket], axis=1)
    play_features.to_csv(play_features_file)

    # Load information regarding games
    games_data = pd.read_csv(os.path.join(input_path, 'games_enhanced.csv'))

    # Performing all game feature extractions
    games_features = extract_game_features(games_data)
    games_features.to_csv(game_features_file)
    ##########################################

    ##########################################
    # STEP 2 - PREPROCESS ALL PLAYS          #
    ##########################################
    # Load information regarding players -- for did_qb_stay_in_pocket
    player_data = pd.read_csv(os.path.join(input_path, 'players.csv'))

    scores=pd.DataFrame()

    for weekId, play_df in plays.groupby('weekId'):
        
        all_scores_info = []
        print(f"-> Processing {weekId}")
        
        # Load information for an entire week
        week_data = pd.read_csv(os.path.join(input_path, weekId))
        plays_qb_in_pocket= extract_did_qb_stay_in_pocket(week_data, player_data, config).set_index(['gameId', 'playId'])

        for weekId, gameId, playId in tqdm.tqdm(plays.query(f"weekId=='{weekId}'").values):
            #print([gameId])

            # Extract info from the play
            team1, team2, ball = extractPlay(week_data, gameId, playId)
            team1, team2, ball = config['preprocess_funct'](team1, team2, ball, delay_frame=config['hold_QB_ref'])

            ############################################################
            # Extract player influence
            players_influence = extract_play_players_influence(team2, infl_funct=config['player_infl_funct'], config=config)

            # Extract field price
            field_price = calculate_field_price(price_funct=config['field_price_funct'], config=config)

            # Calculate defensive scores
            defence_score = calculate_defense_score(players_influence, field_price)

            # Calculate QB score
            QB_OOP_Score = calculate_qb_score(team1, ball, config, input_path)

            # Adds both scores
            pocketScoreTimeSeries = defence_score + QB_OOP_Score

            # Calculate the final score
            pocketScore = np.max(pocketScoreTimeSeries)
            ############################################################

            all_scores_info.append({
                'gameId': gameId,
                'playId': playId,
                'offTeam': team1.team.drop_duplicates().values[0],
                'pocketScore': pocketScore,
                'pocketScoreTimeSeries': pocketScoreTimeSeries
            })
            
        scores = \
            pd.concat([scores,
                        pd.DataFrame(all_scores_info).set_index(['gameId', 'playId']).join(plays_qb_in_pocket).reset_index()], 
                        axis=0)

    # Merge scores with play features
    play_scores_and_features =  pd.concat([scores.set_index(['gameId', 'playId']), play_features], axis=1, join="inner")
    
    # Add additional features
    play_scores_and_features['have_linemen_failed'] = play_scores_and_features.apply(lambda x: True if ((x['was_qb_sacked']==True) | (x['did_qb_stay_in_pocket']==False)) else False, axis=1)
    play_scores_and_features['pocket_outcome'] = play_scores_and_features.apply(determine_pocket_outcome, axis=1)

    # Store DataFrame
    play_scores_and_features.to_csv(scores_and_features_file)
    ##########################################

    ##########################################
    # STEP 3 - ANALYZE THE RESULTS           #
    ########################################## 
    # Perform analysis by Single Play
    evaluate_singleplay_scores(scores_and_features_file)

    # Aggregate by match
    result = agg_scores_by_match(scores_and_features_file, game_features_file)
    result.to_csv(match_scores_file)

    # Perform analysis by Match
    evaluate_match_scores(match_scores_file)

    # Aggregate by season
    season_result = agg_scores_by_season(scores_and_features_file, game_features_file)
    season_result.to_csv(season_scores_file)

    # Perform analysis by Match
    evaluate_season_scores(season_scores_file)

    # Extract information regarding Score Time Series
    if timeseries_plots:
        evaluate_time_series_score(play_scores_and_features)
    ##########################################

def run_full_pipeline(input_path, output_path, config, runId = "generic"):

    """
    This function performs all operations required for the pipeline execution. All operations are parametrized through CONFIG
    This pipeline performs the following operations:
    1- Extract features
    2- Process all plays and extract their pocket scores
    3- Correlate features with pocket score
    :param input_path: Input path to raw data
    :param output_path: Path for processed datasets
    :param config: Run Parameters
    :param runId: ID to identify each run 
    """

    play_features_file = f"{output_path}/play_features_{runId}.csv"
    game_features_file = f"{output_path}/game_features_{runId}.csv"
    scores_and_features_file = f"{output_path}/play_scores_and_features_{runId}.csv"
    match_scores_file = f"{output_path}/match_scores_and_features_{runId}.csv"
    season_scores_file = f"{output_path}/season_scores_and_features_{runId}.csv"

    ##########################################
    # STEP 1 - CREATE FEATURE VECTOR         #
    ########################################## 
    # Load information regarding plays
    plays_data = pd.read_csv(os.path.join(input_path, 'plays.csv'))

    # Perform all play feature extractions
    plays_outcomes = extract_play_outcome_features(plays_data).set_index(['gameId', 'playId'])
    plays_formation = extract_formation_features(plays_data).set_index(['gameId', 'playId'])
    plays_fouls = extract_foul_features(plays_data).set_index(['gameId', 'playId'])
    plays_injury = extract_injury_features(plays_data).set_index(['gameId', 'playId'])

    # Merge all these tables into one single big table
    play_features = pd.concat([plays_outcomes, plays_formation, plays_fouls, plays_injury], axis=1)
    play_features.to_csv(play_features_file)

    # Load information regarding games
    games_data = pd.read_csv(os.path.join(input_path, 'games_enhanced.csv'))

    # Performing all game feature extractions
    games_features = extract_game_features(games_data)
    games_features.to_csv(game_features_file)

    ##########################################
    # STEP 2 - PREPROCESS ALL PLAYS          #
    ########################################## 
    # Define number of weeks to analyize
    num_weeks = 8

    # Generate files names
    week_files = []
    for i in range(num_weeks):
        week_files.append(f'week{i+1}.csv')

    # Load information regarding players -- for did_qb_stay_in_pocket
    player_data = pd.read_csv(os.path.join(input_path, 'players.csv'))
    scores=pd.DataFrame()

    # For all weeks, extract scores
    all_scores_info = []
    for week_file in week_files:

        print(f"- Analyzing {week_file}")

        # Load information for an entire week
        week_data = pd.read_csv(os.path.join(input_path, week_file))
        plays_qb_in_pocket= extract_did_qb_stay_in_pocket(week_data, player_data, config).set_index(['gameId', 'playId'])

        # Extract information about the associated games and plays
        unique_ids = week_data[['gameId', 'playId']].drop_duplicates().values

        for gameId, playId in tqdm.tqdm(unique_ids):

            # Extract info from the play
            team1, team2, ball = extractPlay(week_data, gameId, playId)
            team1, team2, ball = config['preprocess_funct'](team1, team2, ball, delay_frame=config['hold_QB_ref'])

            ############################################################
            # Extract player influence
            players_influence = extract_play_players_influence(team2, infl_funct=config['player_infl_funct'], config=config)

            # Extract field price
            field_price = calculate_field_price(price_funct=config['field_price_funct'], config=config)

            # Calculate defensive scores
            defence_score = calculate_defense_score(players_influence, field_price)

            # Calculate QB score
            QB_OOP_Score = calculate_qb_score(team1, ball, config, input_path)

            # Adds both scores
            pocketScoreTimeSeries = defence_score + QB_OOP_Score

            # Calculate the final score
            pocketScore = np.max(pocketScoreTimeSeries)

            ############################################################
            # For now, we will include random values
            # pocketScore = random.uniform(0, 1)
            ############################################################

            all_scores_info.append({
                'gameId': gameId,
                'playId': playId,
                'offTeam': team1.team.drop_duplicates().values[0],
                'pocketScore': pocketScore,
                'pocketScoreTimeSeries': pocketScoreTimeSeries
            })
            
        scores = \
            pd.concat([scores,
                        pd.DataFrame(all_scores_info).set_index(['gameId', 'playId']).join(plays_qb_in_pocket).reset_index()], 
                        axis=0)

    # Merge scores with play features
    play_scores_and_features =  pd.concat([scores, plays_outcomes, plays_formation, plays_fouls, plays_injury], axis=1)

    # Add additional features
    play_scores_and_features['have_linemen_failed'] = play_scores_and_features.apply(lambda x: True if ((x['was_qb_sacked']==True) | (x['did_qb_stay_in_pocket']==False)) else False, axis=1)
    play_scores_and_features['pocket_outcome'] = play_scores_and_features.apply(determine_pocket_outcome, axis=1)

    # Store DataFrame
    play_scores_and_features.to_csv(scores_and_features_file)

    ##########################################
    # STEP 3 - ANALYZE THE RESULTS           #
    ########################################## 
    # Perform analysis by Single Play
    evaluate_singleplay_scores(scores_and_features_file)

    # Aggregate by match
    result = agg_scores_by_match(scores_and_features_file, game_features_file)
    result.to_csv(match_scores_file)

    # Perform analysis by Match
    evaluate_match_scores(match_scores_file)

    # Aggregate by season
    season_result = agg_scores_by_season(scores_and_features_file, game_features_file)
    season_result.to_csv(season_scores_file)

    # Perform analysis by Match
    evaluate_season_scores(season_scores_file)