import os
import re
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Libraries required for plotting field
import matplotlib.patches as patches
from matplotlib.patches import Arc
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import animation
from IPython.display import HTML

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
    rect = plt.Rectangle((-width/2, -width/2), width, width, ec="w", fc="None", lw=2)
    ax.add_patch(rect)
    ###################

    ###################
    # Plot the center of the square
    plt.plot(0, 0, marker="x", c="w", lw=2)
    ###################
    
    return fig, ax
 

 # Animate one play based on the provided data - Inspired by https://www.kaggle.com/code/werooring/nfl-big-data-bowl-basic-eda-for-beginner
def animatePlay_Generic(team1, team2, ball, area_drawn):

    """
    This function animates a play, based on the area provided.
    :param team1: Information about the offensive team
    :param team2: Information about the defensive team
    :param ball: Information about the ball
    :param area_drawn: Function that defines the area drawn
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

    return HTML(anim.to_html5_video())