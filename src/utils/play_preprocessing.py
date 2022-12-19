import os
import re
import sys
import math
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
            team1 = play_data.loc[play_data.team == team, ['frameId', 'team', 'nflId', 'playDirection', 'x', 'y', 's', 'a', 'dis', 'o', 'dir', 'event']]
        else:
            team2 = play_data.loc[play_data.team == team, ['frameId', 'team', 'nflId', 'playDirection', 'x', 'y', 's', 'a', 'dis', 'o', 'dir','event']]

    # Extract information about the ball
    ball = play_data.loc[play_data.team == "football", ['frameId', 'playDirection', 'x', 'y', 's', 'a', 'dis', 'event']]

    return team1, team2, ball

def preprocessPlay_refLineScrimmageInit(team1, team2, ball, delay_frame = 6, post_snap_time = 8, input_path = "../input/"):
    
    """
    Modify the play to have as reference the initial position of the scrimmage line
    Team 1 is always the offensive team, Team 2 is always the defensive
    :param team1: DataFrame with all info regarding team1
    :param team2: DataFrame with all info regarding team2
    :param ball: DataFrame with all info regarding the ball
    :param delay_frame: NOT REQUIRED - ADDED TO MAKE THIS FUNCTION A PARAMETER
    :param post_snap_time: NOT REQUIRED - ADDED TO MAKE THIS FUNCTION A PARAMETER
    :return team1: DataFrame with normalized info regarding team1, based on the initial position of the ball
    :return team2: DataFrame with normalized info regarding team2, based on the initial position of the ball
    :return ball: DataFrame with normalized info regarding the ball, based on the initial position of the ball
    """

    # Extract ball initial position
    initial_y = ball.loc[ball.frameId == 1, 'y'].values.flatten()
    if ball.playDirection.values[0] == "left":
        initial_x = ball.loc[ball.frameId == 1, 'x'].values.flatten() + 5
    else:
        initial_x = ball.loc[ball.frameId == 1, 'x'].values.flatten() - 5

    # All coordinates are now placed referenced to these coordinates
    elements = [team1, team2, ball]
    for element in elements:
        element['x'] = element.x - initial_x
        element['y'] = element.y - initial_y

    return team1, team2, ball

def preprocessPlay_refBallInit(team1, team2, ball, delay_frame = 6, post_snap_time = 8, input_path = "../input/"):
    
    """
    Modify the play to have as reference the initial position of the ball
    Team 1 is always the offensive team, Team 2 is always the defensive
    :param team1: DataFrame with all info regarding team1
    :param team2: DataFrame with all info regarding team2
    :param ball: DataFrame with all info regarding the ball
    :param delay_frame: NOT REQUIRED - ADDED TO MAKE THIS FUNCTION A PARAMETER
    :param post_snap_time: NOT REQUIRED - ADDED TO MAKE THIS FUNCTION A PARAMETER
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

def preprocessPlay_refQB(team1, team2, ball, delay_frame = 6, post_snap_time = 8, input_path = "../input/"):

    """
    Modify the play to have as reference the QB position during the play
    Team 1 is always the offensive team, Team 2 is always the defensive
    :param team1: DataFrame with all info regarding team1
    :param team2: DataFrame with all info regarding team2
    :param ball: DataFrame with all info regarding the ball
    :param delay_frame: NOT REQUIRED - ADDED TO MAKE THIS FUNCTION A PARAMETER
    :param post_snap_time: Number of frames from snap to QB definition
    :return team1: DataFrame with normalized info regarding team1, based on the QB positon
    :return team2: DataFrame with normalized info regarding team2, based on the QB positon
    :return ball: DataFrame with normalized info regarding the ball, based on the QB positon
    """

    # Extract which team from the offensive team is the QB
    # - Obtain list of players
    list_players = team1.nflId.unique().tolist()
    # - Extract QB ID
    qb_id = pd.read_csv(os.path.join(input_path, 'players.csv')).query("nflId == @list_players & officialPosition == 'QB'")
    # - Run certain checks - QB available and only one QB
    # - If an error is raised, we look for the QB
    if (qb_id.empty) | (len(qb_id) > 1):

        # - Determine the moment the ball was snapped
        frame_snap = ball.loc[ball.event == 'ball_snap', 'frameId'].values[0] + post_snap_time

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

    # All coordinates are now placed referenced to the QB coordinates
    elements = [team1, team2, ball]
    frameIds = ball.frameId.unique()
    for element in elements:
        for frameId in frameIds:
            ref_x, ref_y = qb_ref.loc[qb_ref.frameId == frameId, ['x', 'y']].values[0]
            element.loc[element.frameId == frameId, 'x'] = element.loc[element.frameId == frameId, 'x'] - ref_x
            element.loc[element.frameId == frameId, 'y'] = element.loc[element.frameId == frameId, 'y'] - ref_y
        
        # I tried to do this with GroupBy and it simply doesn't like it
        # element['y'] = element.groupby['nlfId'].apply(lambda player: player.y - qb_ref.y)

    return team1, team2, ball

def preprocessPlay_refQB_NFrames(team1, team2, ball, delay_frame = 6, post_snap_time = 8, input_path = "../input/"):

    """
    Modify the play to have as reference the QB position during the play, with a limit in the number of frames
    Team 1 is always the offensive team, Team 2 is always the defensive
    :param team1: DataFrame with all info regarding team1
    :param team2: DataFrame with all info regarding team2
    :param ball: DataFrame with all info regarding the ball
    :param delay_frame: Number of frames where the QB is used as reference
    :param post_snap_time: Number of frames from snap to QB definition
    :return team1: DataFrame with normalized info regarding team1, based on the QB positon
    :return team2: DataFrame with normalized info regarding team2, based on the QB positon
    :return ball: DataFrame with normalized info regarding the ball, based on the QB positon
    """
    # Extract which team from the offensive team is the QB
    # - Obtain list of players
    list_players = team1.nflId.unique().tolist()
    # - Extract QB ID
    qb_id = pd.read_csv(os.path.join(input_path, 'players.csv')).query("nflId == @list_players & officialPosition == 'QB'")
    # - Run certain checks - QB available and only one QB
    # - If an error is raised, we look for the QB
    if (qb_id.empty) | (len(qb_id) > 1):

        # - Determine the moment the ball was snapped
        frame_snap = ball.loc[ball.event == 'ball_snap', 'frameId'].values[0] + post_snap_time

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
    qb_ref_delay_frame = qb_ref.loc[qb_ref.frameId == delay_frame]
    frameIds = ball.frameId.unique()
    for frame in frameIds:
        if frame > delay_frame:
            qb_ref.loc[qb_ref.frameId == frame, 'x'] = qb_ref_delay_frame.x.values[0]
            qb_ref.loc[qb_ref.frameId == frame, 'y'] = qb_ref_delay_frame.y.values[0]

    # All coordinates are now placed referenced to the QB coordinates
    elements = [team1, team2, ball]
    for element in elements:
        for frame in frameIds:
            ref_x, ref_y = qb_ref.loc[qb_ref.frameId == frame, ['x', 'y']].values[0]
            element.loc[element.frameId == frame, 'x'] = element.loc[element.frameId == frame, 'x'] - ref_x
            element.loc[element.frameId == frame, 'y'] = element.loc[element.frameId == frame, 'y'] - ref_y
        
        # I tried to do this with GroupBy and it simply doesn't like it
        # element['y'] = element.groupby['nlfId'].apply(lambda player: player.y - qb_ref.y)

    return team1, team2, ball