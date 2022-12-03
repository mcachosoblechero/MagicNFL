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


def evaluate_agg_scores(scores_file):

    """
    This function generates a set of analytic plots to correlate features and scores
    This function accepts aggregated data both at the match and season level
    :param scores_file: Path to the file with agg scores
    """

    # Load information based on the analysis provided
    analysis_results = pd.read_csv(scores_file)
    
    #################################################################
    # Run a set of analysis to explore the correlation between the score and the extracted features
    #################################################################
    # Play Outcome Analysis
    # Figure height and width
    width = 40
    height = 10
    plt.figure(figsize=(width,height))
    # Number of subplots
    rows = 1
    cols = 5
    # Analysis 1 - Score vs Cum Gained Yards
    plt.subplot(rows,cols,1)
    sns.scatterplot(data=analysis_results, y='avgPocketScore', x='cumGainedYards')
    plt.xlabel("Cumulative Gained yards")
    plt.ylabel("Average Pocket Score")
    plt.title("Score vs Cum Gained Yards")
    # Analysis 2 - Score vs Avg Gained Yards
    plt.subplot(rows,cols,2)
    sns.scatterplot(data=analysis_results, y='avgPocketScore', x='avgGainedYards')
    plt.xlabel("Average Gained yards")
    plt.ylabel("Average Pocket Score")
    plt.title("Score vs Avg Gained Yards")
    # Analysis 3 - Score vs Pass complete
    plt.subplot(rows,cols,3)
    sns.scatterplot(data=analysis_results, y='avgPocketScore', x='percPassComplete')
    plt.xlabel("Percentage Complete Passes")
    plt.ylabel("Average Pocket Score")
    plt.title("Score vs % Complete pass")
    # Analysis 4 - Score vs Pocket hold
    plt.subplot(rows,cols,4)
    sns.scatterplot(data=analysis_results, y='avgPocketScore', x='percPocketHold')
    plt.xlabel("Percentage Pocket hold")
    plt.ylabel("Average Pocket Score")
    plt.title("Score vs % Pocket hold")
    # Analysis 5 - Score vs Pocket hold
    plt.subplot(rows,cols,5)
    sns.scatterplot(data=analysis_results, y='avgPocketScore', x='percQBSacked')
    plt.xlabel("Percentage QB Sacked")
    plt.ylabel("Average Pocket Score")
    plt.title("Score vs % QB Sacked")

    #################################################################
    # Foul analysis
    # Figure height and width
    height = 10
    width = 20
    plt.figure(figsize=(width,height))
    # Number of subplots
    rows = 1
    cols = 2
    # Analysis 1 - Score vs Num Offensive Fouls
    plt.subplot(rows,cols,1)
    sns.scatterplot(data=analysis_results, y='avgPocketScore', x='numOffFouls')
    plt.xlabel("Number of Offensive Fouls")
    plt.ylabel("Average Pocket Score")
    plt.title("Score vs Off Fouls")
    # Analysis 2 - Score vs Num Defensive Fouls
    plt.subplot(rows,cols,2)
    sns.scatterplot(data=analysis_results, y='avgPocketScore', x='numDefFouls')
    plt.xlabel("Number of Defensive Fouls")
    plt.ylabel("Average Pocket Score")
    plt.title("Score vs Def Fouls")
    
    #################################################################
    # Injury analysis
    # Figure height and width
    height = 10
    width = 20
    plt.figure(figsize=(width,height))
    # Number of subplots
    rows = 1
    cols = 2
    # Analysis 1 - Score vs Num Offensive Injuries
    plt.subplot(rows,cols,1)
    sns.scatterplot(data=analysis_results, y='avgPocketScore', x='numOffInjuries')
    plt.xlabel("Number of Offensive Injuries")
    plt.ylabel("Average Pocket Score")
    plt.title("Score vs Off Injuries")
    # Analysis 2 - Score vs Num Defensive Injuries
    plt.subplot(rows,cols,2)
    sns.scatterplot(data=analysis_results, y='avgPocketScore', x='numDefInjuries')
    plt.xlabel("Number of Defensive Injuries")
    plt.ylabel("Average Pocket Score")
    plt.title("Score vs Def Injuries")


def evaluate_singleplay_scores(scores_file):

    """
    This function generates a set of analytic plots to correlate features and scores.
    This function accepts single-play raw data
    :param scores_file: Path to the file with agg scores
    """

    # Load information based on the analysis provided
    analysis_results = pd.read_csv(scores_file)
    
    #################################################################
    # Run a set of analysis to explore the correlation between the score and the extracted features
    #################################################################
    # Play Outcome Analysis
    # Figure height and width
    width = 40
    height = 10
    plt.figure(figsize=(width,height))
    # Number of subplots
    rows = 1
    cols = 4
    # Analysis 1 - Score vs Gained Yards
    plt.subplot(rows,cols,1)
    sns.scatterplot(data=analysis_results, y='pocketScore', x='gained_yards')
    plt.xlabel("Gained yards")
    plt.ylabel("Pocket Score")
    plt.title("Score vs Gained Yards")
    # Analysis 2 - Score vs Pass complete
    plt.subplot(rows,cols,2)
    sns.violinplot(data=analysis_results, y='pocketScore', x='pass_complete')
    plt.xlabel("Was it a complete pass?")
    plt.ylabel("Pocket Score")
    plt.title("Score vs Complete pass")
    # Analysis 3 - Score vs Pocket hold
    plt.subplot(rows,cols,3)
    sns.violinplot(data=analysis_results, y='pocketScore', x='has_pocket_hold')
    plt.xlabel("Had pocket hold?")
    plt.ylabel("Pocket Score")
    plt.title("Score vs Pocket hold")
    # Analysis 4 - Score vs Pocket hold
    plt.subplot(rows,cols,4)
    sns.violinplot(data=analysis_results, y='pocketScore', x='was_qb_sacked')
    plt.xlabel("Was QB sacked?")
    plt.ylabel("Pocket Score")
    plt.title("Score vs QB Sacked")
    
    #################################################################
    # Formation analysis
    # Figure height and width
    height = 10
    width = 40
    plt.figure(figsize=(width,height))
    # Number of subplots
    rows = 1
    cols = 4
    # Analysis 1 - Score vs # RB
    plt.subplot(rows,cols,1)
    sns.scatterplot(data=analysis_results, y='pocketScore', x='num_rb')
    plt.xlabel("Number of RB")
    plt.ylabel("Pocket Score")
    plt.title("Score vs # RB")
    # Analysis 2 - Score vs # WR
    plt.subplot(rows,cols,2)
    sns.scatterplot(data=analysis_results, y='pocketScore', x='num_wr')
    plt.xlabel("Number of WR")
    plt.ylabel("Pocket Score")
    plt.title("Score vs # WR")
    # Analysis 3 - Score vs # TE
    plt.subplot(rows,cols,3)
    sns.scatterplot(data=analysis_results, y='pocketScore', x='num_te')
    plt.xlabel("Number of TE")
    plt.ylabel("Pocket Score")
    plt.title("Score vs # TE")
    # Analysis 4 - Score vs # OL
    plt.subplot(rows,cols,4)
    sns.scatterplot(data=analysis_results, y='pocketScore', x='num_ol')
    plt.xlabel("Number of OL")
    plt.ylabel("Pocket Score")
    plt.title("Score vs # OL")

    #################################################################
    # Foul analysis
    # Figure height and width
    height = 10
    width = 20
    plt.figure(figsize=(width,height))
    # Number of subplots
    rows = 1
    cols = 2
    # Analysis 1 - Score vs Num Offensive Fouls
    plt.subplot(rows,cols,1)
    sns.scatterplot(data=analysis_results, y='pocketScore', x='num_off_foul')
    plt.xlabel("Number of Offensive Fouls")
    plt.ylabel("Pocket Score")
    plt.title("Score vs Off Fouls")
    # Analysis 2 - Score vs Num Defensive Fouls
    plt.subplot(rows,cols,2)
    sns.scatterplot(data=analysis_results, y='pocketScore', x='num_def_foul')
    plt.xlabel("Number of Defensive Fouls")
    plt.ylabel("Pocket Score")
    plt.title("Score vs Def Fouls")
    
    #################################################################
    # Injury analysis
    # Figure height and width
    height = 10
    width = 20
    plt.figure(figsize=(width,height))
    # Number of subplots
    rows = 1
    cols = 2
    # Analysis 1 - Score vs Num Offensive Injuries
    plt.subplot(rows,cols,1)
    sns.scatterplot(data=analysis_results, y='pocketScore', x='num_off_injuries')
    plt.xlabel("Number of Offensive Injuries")
    plt.ylabel("Pocket Score")
    plt.title("Score vs Off Injuries")
    # Analysis 2 - Score vs Num Defensive Injuries
    plt.subplot(rows,cols,2)
    sns.scatterplot(data=analysis_results, y='pocketScore', x='num_def_injuries')
    plt.xlabel("Number of Defensive Injuries")
    plt.ylabel("Pocket Score")
    plt.title("Score vs Def Injuries")