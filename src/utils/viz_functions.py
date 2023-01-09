import os
import re
import sys
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
from src.utils.player_influence import extract_play_players_influence, gaussian_player_influence_score
from src.utils.field_price_functions import calculate_field_price
from src.utils.calculate_score import calculate_defense_score, calculate_qb_score

# Figure visualization, inspired by https://www.kaggle.com/code/jaronmichal/tracking-data-visualization/notebook
# De-parametrized it, setting the field to 100 x 53.3 yards 
def drawPitch():

    """
    This function draws an entire pitch.
    This function is envisioned to be called inside "animatePlay_Generic", although it can be used independently
    :return: Figure object with pitch drawn on it
    """

    # Constant parameters
    width = 100
    height = 53.3
    color = "w"

    # Create figure object
    fig = plt.figure(figsize=(20, 16))
    ax = plt.axes(xlim=(-10, width + 30), ylim=(-15, height + 5))
    plt.axis('off')

    ###################
    # Create a rectangle - Entire field
    # xy = Anchor point
    # width = Length of the field (included side of the field, 10 yards)
    # height = Height of the field (included side of the field, 5 yards)
    rect = patches.Rectangle(
        xy = (-10, -5), 
        height = height + 10, 
        width = width + 40, 
        linewidth=1, 
        facecolor='#3f995b', 
        capstyle='round'
        )
    ax.add_patch(rect)
    ###################

    ###################
    # Create a rectangle - Playable pitch + 2 endzones (10 yards)
    rect = plt.Rectangle((0, 0), width + 20, height, ec=color, fc="None", lw=2)
    ax.add_patch(rect)
    ###################

    ###################
    # Create vertical lines every 5 yards
    for i in range(21):
        plt.plot([10 + 5 * i, 10 + 5 * i], [0, height], c="w", lw=2)
    ###################
        
    ###################
    # Create distance text - every 10 yards
    for yards in range(10, width, 10):
        yards_text = yards if yards <= width / 2 else width - yards
        # top markers
        plt.text(10 + yards - 2, height - 7.5, yards_text, size=20, c="w", weight="bold")
        # botoom markers
        plt.text(10 + yards - 2, 7.5, yards_text, size=20, c="w", weight="bold", rotation=180)
    ###################

    ###################
    # yards markers - every yard
    # bottom markers
    for x in range(20):
        for j in range(1, 5):
            plt.plot([10 + x * 5 + j, 10 + x * 5 + j], [1, 3], color="w", lw=3)

    # top markers
    for x in range(20):
        for j in range(1, 5):
            plt.plot([10 + x * 5 + j, 10 + x * 5 + j], [height - 1, height - 3], color="w", lw=3)

    # middle bottom markers
    y = (height - 18.5) / 2
    for x in range(20):
        for j in range(1, 5):
            plt.plot([10 + x * 5 + j, 10 + x * 5 + j], [y, y + 2], color="w", lw=3)

    # middle top markers
    for x in range(20):
        for j in range(1, 5):
            plt.plot([10 + x * 5 + j, 10 + x * 5 + j], [height - y, height - y - 2], color="w", lw=3)
    ###################

    ###################
    # Create Endzones Rectangles and Text
    # Home
    plt.text(2.5, (height - 10) / 2, "HOME", size=40, c="w", weight="bold", rotation=90)
    rect = plt.Rectangle((0, 0), 10, height, ec=color, fc="#0064dc", lw=2)
    ax.add_patch(rect)

    # Away    
    plt.text(112.5, (height - 10) / 2, "AWAY", size=40, c="w", weight="bold", rotation=-90)
    rect = plt.Rectangle((width + 10, 0), 10, height, ec=color, fc="#c80014", lw=2)
    ax.add_patch(rect)
    ###################
    
    ###################
    # Create Spot point
    # left
    y = (height - 3) / 2
    plt.plot([10 + 2, 10 + 2], [y, y + 3], c="w", lw=2)
    
    # right
    plt.plot([width + 10 - 2, width + 10 - 2], [y, y + 3], c="w", lw=2)
    ###################
    
    ###################
    # Create goalpost
    goal_width = 6 # yards
    y = (height - goal_width) / 2
    # left
    plt.plot([0, 0], [y, y + goal_width], "-", c="y", lw=10, ms=20)
    # right
    plt.plot([width + 20, width + 20], [y, y + goal_width], "-", c="y", lw=10, ms=20)
    ###################
    
    return fig, ax



# This function will be later integrated with Bryce's pocket code
def drawPocket(width = 30):

    """
    This function draws a pocket.
    This function is envisioned to be called inside "animatePlay_Generic", although it can be used independently
    :return: Figure object with pocket drawn on it
    """

    # Create figure object
    fig = plt.figure(figsize=(15, 15))
    ax = plt.axes(xlim=(-10 - width/2, width/2 + 10), ylim=(-10 - width/2, width/2 + 10))
    plt.axis('off')

    ###################
    # Create rectangle - Entire field
    # xy = Anchor point
    # width = Length of the field (included side of the field, 10 yards)
    # height = Height of the field (included side of the field, 5 yards)
    rect = patches.Rectangle(
        xy = (-5 - width/2, -5 - width/2), 
        height = width + 10, 
        width = width + 10, 
        linewidth=1, 
        facecolor='#3f995b', 
        capstyle='round'
        )
    ax.add_patch(rect)
    ###################

    ###################
    # Create a set of rectangle - Playable pitch + 2 endzones (10 yards)
    # pocket = plt.Rectangle((-width/2, -width/2), width, width, ec="w", fc="None", lw=2)
    pocket = plt.Circle(xy=(0,0), radius=width/2,ec="w", fc="None", lw=2)
    ax.add_patch(pocket)
    ###################

    ###################
    # Plot the center of the square
    plt.plot(0, 0, marker="x", c="w", lw=2)
    ###################
    
    return fig, ax
 

 # Animate one play based on the provided data - Inspired by https://www.kaggle.com/code/werooring/nfl-big-data-bowl-basic-eda-for-beginner
def animatePlay_Generic(team1, team2, ball, area_drawn, store_path=""):

    """
    This function animates a play, based on the area provided.
    :param team1: Information about the offensive team
    :param team2: Information about the defensive team
    :param ball: Information about the ball
    :param area_drawn: Function that defines the area drawn
    :param store_path: If required, store the output video in this path
    :return: HTML animation
    """

    # Create the pitch object - Pass a function
    fig, ax = area_drawn
    
    # Set the plots to be drawn
    team_left, = ax.plot([], [], 'o', markersize=20, markerfacecolor="r", markeredgewidth=2, markeredgecolor="white", zorder=7)
    team_right, = ax.plot([], [], 'o', markersize=20, markerfacecolor="b", markeredgewidth=2, markeredgecolor="white", zorder=7)
    ball_draw, = ax.plot([], [], 'o', markersize=10, markerfacecolor="black", markeredgewidth=2, markeredgecolor="white", zorder=7)
    drawings = [team_left, team_right, ball_draw]

    # Initially, no data is plotted
    def init():
        team_left.set_data([], [])
        team_right.set_data([], [])
        ball_draw.set_data([], [])
        return drawings

    # On each frame, plot the information provided
    def draw_teams(i):
        
        # Empty list to be plotted - Team 1
        X = []
        Y = []

        # Extract frame information - Team 1
        for x, y in team1.loc[team1.frameId == i, ['x', 'y']].values:
            X.append(x)
            Y.append(y)
        team_left.set_data(X, Y)
        
        # Empty list to be plotted - Team 2
        X = []
        Y = []

        # Extract frame information - Team 2
        for x, y in team2.loc[team2.frameId == i, ['x', 'y']].values:
            X.append(x)
            Y.append(y)
        team_right.set_data(X, Y)

    def draw_ball(i):
        # Empty list to be plotted - Ball
        X = []
        Y = []

        # Extract frame information - Ball
        for x, y in ball.loc[ball.frameId == i, ['x', 'y']].values:
            X.append(x)
            Y.append(y)
        ball_draw.set_data(X, Y)

    def animate(i):
        draw_teams(i)
        draw_ball(i)
        return drawings
    
    # !May take a while!
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=len(ball), interval=100, blit=True)
    # Store if required
    if store_path != "":
        writer = animation.FFMpegWriter(fps=10, metadata=dict(artist='Me'), bitrate=1800)
        anim.save(store_path, writer=writer)

    return HTML(anim.to_html5_video())


def animateScores(scores, store_path=""):

    """
    This function animates the scores associated with a play.
    :param scores: Scores to plot. This needs to be a matrix
    :param store_path: If required, store the output video in this path
    :return: HTML animation
    """

    # Create the pitch object - Pass a function
    fig = plt.figure(figsize=(10,10))
    ax = plt.axes()

    # Set the plots to be drawn
    im_scores = ax.imshow(scores[0], cmap = matplotlib.cm.get_cmap('RdYlGn_r'))
    fig.colorbar(im_scores, orientation='vertical')
    drawings = [im_scores]

    # Initially, initial frame is plotted
    def init():
        im_scores.set_array(scores[0])
        return drawings

    def animate(i):
        im_scores.set_array(scores[i])
        return drawings
    
    # !May take a while!
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=len(scores), interval=100, blit=True)

    # Store if required
    if store_path != "":
        writer = animation.FFMpegWriter(fps=10, metadata=dict(artist='Me'), bitrate=1800)
        anim.save(store_path, writer=writer)

    return HTML(anim.to_html5_video())

def visualize_play(week_data, gameId, playId, config, display_score = True):

    """
    This function visualize a single play, generating all perspectives.
    :param week_data: Week data for the play under study
    :param gameId: GameId to analyze
    :param playId: PlayId to analyze
    :param config: Run Parameters
    :param display_score: Set whether we should display the score viz
    """

    # Full Pitch Evaluation
    # Extract info from the play
    team1, team2, ball = extractPlay(week_data, gameId, playId)

    # Plot the play in Full Field
    fig_field = animatePlay_Generic(team1, team2, ball, drawPitch(), store_path=f"../videos/{gameId}_{playId}_fullPitch.gif")
    display.display(fig_field)
    plt.close()

    # Preprocess the play
    team1, team2, ball = config['preprocess_funct'](team1, team2, ball, delay_frame=config['hold_QB_ref'], post_snap_time=config['post_snap_time'])

    # Plot the play in the Pocket
    fig_field = animatePlay_Generic(team1, team2, ball, drawPocket(config['pocket_len']), store_path=f"../videos/{gameId}_{playId}_pocket.gif")
    display.display(fig_field)
    plt.close()

    # Analyze the position of the defensive players
    # Calculate players influence
    player_infl = extract_play_players_influence(
        team_def=team2,
        infl_funct=config['player_infl_funct'],
        config=config
    )

    # Plot the play
    fig_influence = animateScores(player_infl, store_path=f"../videos/{gameId}_{playId}_player_influence.gif")
    display.display(fig_influence)
    plt.close()

    if display_score:
        # Analyze the score timeline
        # Extract field price
        field_price = calculate_field_price(price_funct=config['field_price_funct'], config=config)

        # Calculate defensive scores
        pocketScoreTimeSeries = calculate_defense_score(player_infl, field_price)

        # Calculate QB score
        QB_OOP_Score = calculate_qb_score(team1, ball, config)

        # Plot frame scores
        plt.figure(figsize=(8,5))
        plt.plot(pocketScoreTimeSeries + QB_OOP_Score)
        plt.title("Score over time")
        plt.xlabel("Frames")
        plt.ylabel("Pocket Score")
        plt.show()

def visualize_plays_time_series(play_metadata, config):

    """
    This function visualize the time series of a set of plays, categorizing them based on their outcome.
    :param play_metadata: Metadata information for all the plays. This should contain week, gameId, playId and outcome
    :param config: Run Parameters
    :param display_score: Set whether we should display the score viz
    """

    # Extract time series information
    score_evolution = pd.DataFrame()
    score_evolution['Score_timeseries'] = play_metadata.apply(process_timeseries_play, config=config, axis=1)
    score_evolution['Outcome'] = play_metadata.outcome

    # Convert DataFrame to unrolled version for time series
    timeseries = []
    for play_score in score_evolution.iterrows():
        for idx, timepoint in enumerate(play_score[1].Score_timeseries):
            if idx <= 80:
                timeseries.append({
                    'frameId': idx,
                    'frameValue': timepoint,
                    'outcome': play_score[1].Outcome,
                })
    df_timeseries = pd.DataFrame(timeseries)

    # Pocket Type Time Series
    plt.figure(figsize=(8,6))
    sns.lineplot(data=df_timeseries, x='frameId', y='frameValue', hue='outcome')
    plt.ylabel("Pocket Score")
    plt.title("Pocket Score Analysis")
    plt.legend()
    plt.show()

def process_timeseries_play(x, config):

    # Extract info from the play
    team1, team2, ball = extractPlay(x.week_data, x.gameId, x.playId)

    # Preprocess the play
    team1, team2, ball = config['preprocess_funct'](team1, team2, ball, delay_frame=config['hold_QB_ref'], post_snap_time=config['post_snap_time'])

    # Analyze the position of the defensive players
    # Calculate players influence
    player_infl = extract_play_players_influence(
        team_def=team2,
        infl_funct=config['player_infl_funct'],
        config=config
    )

    # Analyze the score timeline
    # Extract field price
    field_price = calculate_field_price(price_funct=config['field_price_funct'], config=config)

    # Calculate defensive scores
    pocketScoreTimeSeries = calculate_defense_score(player_infl, field_price)

    # Calculate QB score
    QB_OOP_Score = calculate_qb_score(team1, ball, config)

    return pocketScoreTimeSeries + QB_OOP_Score