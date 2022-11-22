import os
import re
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def extractPlay(week_data, gameId, playId, input_path = "../input/"):

    """
    Extract and pre-process a play data
    Team 1 is always the offensive team, Team 2 is always the defensive
    :param week_data: DataFrame containing all info about a week's games
    :param gameId: Game Id
    :param playId: Play Id
    :param input_path: Path to plays.csv
    :return team1: DataFrame with all info regarding team1
    :return team2: DataFrame with all info regarding team2
    :return ball: DataFrame with all info regarding the ball
    """

    # Extract information from gameId and playId
    play_data = week_data.query(f'gameId == {gameId} and playId == {playId}')

    # Determine which teams are playing
    teams = play_data.loc[play_data.team != "football", "team"].unique()

    # Extract information about what team is offensive
    plays_info = pd.read_csv(os.path.join(input_path, 'plays.csv')).query(f'gameId == {gameId} and playId == {playId}')
    off_team = plays_info.possessionTeam.values[0]

    # Extract information for each team
    for team in teams:
        if team == off_team:
            team1 = play_data.loc[play_data.team == teams[0], ['frameId', 'nflId', 'x', 'y', 's', 'a', 'dis', 'o', 'dir', 'event']]
        else:
            team2 = play_data.loc[play_data.team == teams[1], ['frameId', 'nflId', 'x', 'y', 's', 'a', 'dis', 'o', 'dir','event']]

    # Extract information about the ball
    ball = play_data.loc[play_data.team == "football", ['frameId', 'x', 'y', 's', 'a', 'dis', 'event']]

    return team1, team2, ball

def preprocessPlay_refBallInit(team1, team2, ball):
    
    """
    Modify the play to have as reference the initial position of the ball
    Team 1 is always the offensive team, Team 2 is always the defensive
    :param team1: DataFrame with all info regarding team1
    :param team2: DataFrame with all info regarding team2
    :param ball: DataFrame with all info regarding the ball
    :return team1: DataFrame with normalized info regarding team1, based on the initial position of the ball
    :return team2: DataFrame with normalized info regarding team2, based on the initial position of the ball
    :return ball: DataFrame with normalized info regarding the ball, based on the initial position of the ball
    """

    # Extract ball initial position
    initial_x, initial_y = ball.loc[ball.frameId == 1, ['x', 'y']].values.flatten()

    # All coordinates are now placed referenced to these coordinates
    elements = [team1, team2, ball]
    for element in elements:
        element['x'] = element.x - initial_x
        element['y'] = element.y - initial_y

    return team1, team2, ball

def preprocessPlay_refQB(team1, team2, ball, input_path = "../input/"):

    """
    Modify the play to have as reference the QB position during the play
    Team 1 is always the offensive team, Team 2 is always the defensive
    :param team1: DataFrame with all info regarding team1
    :param team2: DataFrame with all info regarding team2
    :param ball: DataFrame with all info regarding the ball
    :return team1: DataFrame with normalized info regarding team1, based on the QB positon
    :return team2: DataFrame with normalized info regarding team2, based on the QB positon
    :return ball: DataFrame with normalized info regarding the ball, based on the QB positon
    """

    # Extract which team from the offensive team is the QB
    # - Obtain list of players
    list_players = team1.nflId.unique().tolist()
    # - Extract QB ID
    qb_id = pd.read_csv(os.path.join(input_path, 'players.csv')).query("nflId == @list_players & officialPosition == 'QB'").nflId.values.flatten()[0]

    # Extract QB positions across the different frames
    qb_ref = team1.loc[team1.nflId == qb_id, ['frameId', 'x', 'y']].sort_values(['frameId']).set_index('frameId')

    # All coordinates are now placed referenced to the QB coordinates
    elements = [team1, team2, ball]
    num_frames = len(ball)
    for element in elements:
        for frame in range(num_frames):
            ref_x, ref_y = qb_ref.iloc[frame].values
            element.loc[element.frameId == frame, 'x'] = element.loc[element.frameId == frame, 'x'] - ref_x
            element.loc[element.frameId == frame, 'y'] = element.loc[element.frameId == frame, 'y'] - ref_y
        
        # I tried to do this with GroupBy and it simply doesn't like it
        # element['y'] = element.groupby['nlfId'].apply(lambda player: player.y - qb_ref.y)

    return team1, team2, ball