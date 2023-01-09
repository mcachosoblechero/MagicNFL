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


def evaluate_season_scores(scores_file):

    """
    This function generates a set of analytic plots to correlate features and scores
    This function accepts aggregated data at the season level
    :param scores_file: Path to the file with agg scores
    """

    # Load information based on the analysis provided
    analysis_results = pd.read_csv(scores_file)
    
    #################################################################
    # Run a set of analysis to explore the correlation between the score and the extracted features
    #################################################################
    # Play Outcome Analysis
    # Figure height and width
    width = 20
    height = 20
    plt.figure(figsize=(width,height))
    # Number of subplots
    rows = 2
    cols = 2
    # Analysis 1 - Score vs % Off Linemen Fail
    plt.subplot(rows,cols,1)
    sns.scatterplot(data=analysis_results, y='avgPocketScore', x='percLinemenFail')
    plt.xlabel("Percentage Off Linemen Fail")
    plt.ylabel("Average Pocket Score")
    plt.title("Score vs % Off Linemen Failed")
    # Analysis 2 - Score vs % Complete Passes
    plt.subplot(rows,cols,2)
    sns.scatterplot(data=analysis_results, y='avgPocketScore', x='percPassComplete')
    plt.xlabel("Percentage Complete Passes")
    plt.ylabel("Average Pocket Score")
    plt.title("Score vs % Complete Pass")
    # Analysis 3 - Score vs QB Sacked
    plt.subplot(rows,cols,3)
    sns.scatterplot(data=analysis_results, y='avgPocketScore', x='percQBSacked')
    plt.xlabel("Percentage QB Sacked")
    plt.ylabel("Average Pocket Score")
    plt.title("Score vs % QB Sacked")
    # Analysis 4 - Score vs QB OOP
    plt.subplot(rows,cols,4)
    sns.scatterplot(data=analysis_results, y='avgPocketScore', x='percQBOOP')
    plt.xlabel("Percentage Out-of-Pocket")
    plt.ylabel("Average Pocket Score")
    plt.title("Score vs %  QB Out-of-Pocket Plays")

    #################################################################
    # Yardage Analysis
    # Figure height and width
    width = 20
    height = 10
    plt.figure(figsize=(width,height))
    # Number of subplots
    rows = 1
    cols = 2
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


    #################################################################
    # Game Analysis
    # Figure height and width
    width = 20
    height = 10
    plt.figure(figsize=(width,height))
    # Number of subplots
    rows = 1
    cols = 2
    # Analysis 1 - Avg Pocket Score vs Cum Score
    plt.subplot(rows,cols,1)
    sns.scatterplot(data=analysis_results, y='avgPocketScore', x='cumScore')
    plt.xlabel("Cumulative Season Score")
    plt.ylabel("Average Pocket Score")
    plt.title("Avg Pocket Score vs Cum Score")
    # Analysis 2 - Avg Pocket Score vs Avg Score
    plt.subplot(rows,cols,2)
    sns.scatterplot(data=analysis_results, y='avgPocketScore', x='avgScore')
    plt.xlabel("Average Season Score")
    plt.ylabel("Average Pocket Score")
    plt.title("Avg Pocket Score vs Avg Score")

    #################################################################
    # Season Analysis
    # Figure height and width
    width = 10
    height = 10
    plt.figure(figsize=(width,height))
    # Number of subplots
    rows = 1
    cols = 1
    # Analysis 3 - Avg Pocket Score vs Games Won
    plt.subplot(rows,cols,1)
    sns.violinplot(data=analysis_results, y='avgPocketScore', x='gamesWon')
    plt.xlabel("Games Won")
    plt.ylabel("Average Pocket Score")
    plt.title("Avg Pocket Score vs Games Won")

    # #################################################################
    # # Foul analysis
    # # Figure height and width
    # height = 10
    # width = 20
    # plt.figure(figsize=(width,height))
    # # Number of subplots
    # rows = 1
    # cols = 2
    # # Analysis 1 - Score vs Num Offensive Fouls
    # plt.subplot(rows,cols,1)
    # sns.scatterplot(data=analysis_results, y='avgPocketScore', x='numOffFouls')
    # plt.xlabel("Number of Offensive Fouls")
    # plt.ylabel("Average Pocket Score")
    # plt.title("Score vs Off Fouls")
    # # Analysis 2 - Score vs Num Defensive Fouls
    # plt.subplot(rows,cols,2)
    # sns.scatterplot(data=analysis_results, y='avgPocketScore', x='numDefFouls')
    # plt.xlabel("Number of Defensive Fouls")
    # plt.ylabel("Average Pocket Score")
    # plt.title("Score vs Def Fouls")
    
    # #################################################################
    # # Injury analysis
    # # Figure height and width
    # height = 10
    # width = 20
    # plt.figure(figsize=(width,height))
    # # Number of subplots
    # rows = 1
    # cols = 2
    # # Analysis 1 - Score vs Num Offensive Injuries
    # plt.subplot(rows,cols,1)
    # sns.scatterplot(data=analysis_results, y='avgPocketScore', x='numOffInjuries')
    # plt.xlabel("Number of Offensive Injuries")
    # plt.ylabel("Average Pocket Score")
    # plt.title("Score vs Off Injuries")
    # # Analysis 2 - Score vs Num Defensive Injuries
    # plt.subplot(rows,cols,2)
    # sns.scatterplot(data=analysis_results, y='avgPocketScore', x='numDefInjuries')
    # plt.xlabel("Number of Defensive Injuries")
    # plt.ylabel("Average Pocket Score")
    # plt.title("Score vs Def Injuries")


def evaluate_match_scores(scores_file):

    """
    This function generates a set of analytic plots to correlate features and scores
    This function accepts aggregated data at the match level
    :param scores_file: Path to the file with agg scores
    """

    # Load information based on the analysis provided
    analysis_results = pd.read_csv(scores_file)
    
    #################################################################
    # Run a set of analysis to explore the correlation between the score and the extracted features
    #################################################################
    # Play Outcome Analysis
    # Figure height and width
    width = 20
    height = 20
    plt.figure(figsize=(width,height))
    # Number of subplots
    rows = 2
    cols = 2
    # Analysis 1 - Score vs Off Linemen Failed
    plt.subplot(rows,cols,1)
    sns.scatterplot(data=analysis_results, y='avgPocketScore', x='percLinemenFail')
    plt.xlabel("Percentage Off Linemen Fail")
    plt.ylabel("Average Pocket Score")
    plt.title("Score vs % Off Linemen Failed")
    # Analysis 2 - Score vs % Pass complete
    plt.subplot(rows,cols,2)
    sns.scatterplot(data=analysis_results, y='avgPocketScore', x='percPassComplete')
    plt.xlabel("Percentage Complete Passes")
    plt.ylabel("Average Pocket Score")
    plt.title("Score vs % Complete pass")
    # Analysis 3 - Score vs QB sacked
    plt.subplot(rows,cols,3)
    sns.scatterplot(data=analysis_results, y='avgPocketScore', x='percQBSacked')
    plt.xlabel("Percentage QB Sacked")
    plt.ylabel("Average Pocket Score")
    plt.title("Score vs % QB Sacked")
    # Analysis 4 - Score vs OOP
    plt.subplot(rows,cols,4)
    sns.scatterplot(data=analysis_results, y='avgPocketScore', x='percQBOOP')
    plt.xlabel("Percentage Out-of-Pocket Plays")
    plt.ylabel("Average Pocket Score")
    plt.title("Score vs % Out-of-Pocket Plays")

    #################################################################
    # Match Yards Analysis
    # Figure height and width
    width = 20
    height = 10
    plt.figure(figsize=(width,height))
    # Number of subplots
    rows = 1
    cols = 2
    # Analysis 4 - Score vs Cum Gained Yards
    plt.subplot(rows,cols,1)
    sns.scatterplot(data=analysis_results, y='avgPocketScore', x='cumGainedYards')
    plt.xlabel("Cumulative Gained yards")
    plt.ylabel("Average Pocket Score")
    plt.title("Score vs Cum Gained Yards")
    # Analysis 5 - Score vs Avg Gained Yards
    plt.subplot(rows,cols,2)
    sns.scatterplot(data=analysis_results, y='avgPocketScore', x='avgGainedYards')
    plt.xlabel("Average Gained yards")
    plt.ylabel("Average Pocket Score")
    plt.title("Score vs Avg Gained Yards")

    #################################################################
    # Game Analysis
    # Figure height and width
    width = 8
    height = 6
    # We divide the Game Score analysis to the Game analysis
    # Game Score Analysis
    plt.figure(figsize=(width,height))
    # Number of subplots
    rows = 1
    cols = 1
    # Analysis 1 - Score vs Game Score
    plt.subplot(rows,cols,1)
    sns.scatterplot(data=analysis_results, y='avgPocketScore', x='gameScore')
    plt.xlabel("Game Score")
    plt.ylabel("Average Pocket Score")
    plt.title("Avg Pocket Score vs Game Score")

    plt.figure(figsize=(width,height))
    # Number of subplots
    rows = 1
    cols = 1
    # Analysis 2 - Score vs Did Team Win game?
    plt.subplot(rows,cols,1)
    sns.violinplot(data=analysis_results, y='avgPocketScore', x='wonGame', palette=['lightcoral', 'seagreen'])
    plt.xlabel("Did the team won the game?")
    plt.ylabel("Average Pocket Score")
    plt.title("Avg Pocket Score vs Game Result")

    # #################################################################
    # # Foul analysis
    # # Figure height and width
    # height = 10
    # width = 20
    # plt.figure(figsize=(width,height))
    # # Number of subplots
    # rows = 1
    # cols = 2
    # # Analysis 1 - Score vs Num Offensive Fouls
    # plt.subplot(rows,cols,1)
    # sns.scatterplot(data=analysis_results, y='avgPocketScore', x='numOffFouls')
    # plt.xlabel("Number of Offensive Fouls")
    # plt.ylabel("Average Pocket Score")
    # plt.title("Score vs Off Fouls")
    # # Analysis 2 - Score vs Num Defensive Fouls
    # plt.subplot(rows,cols,2)
    # sns.scatterplot(data=analysis_results, y='avgPocketScore', x='numDefFouls')
    # plt.xlabel("Number of Defensive Fouls")
    # plt.ylabel("Average Pocket Score")
    # plt.title("Score vs Def Fouls")
    
    # #################################################################
    # # Injury analysis
    # # Figure height and width
    # height = 10
    # width = 20
    # plt.figure(figsize=(width,height))
    # # Number of subplots
    # rows = 1
    # cols = 2
    # # Analysis 1 - Score vs Num Offensive Injuries
    # plt.subplot(rows,cols,1)
    # sns.scatterplot(data=analysis_results, y='avgPocketScore', x='numOffInjuries')
    # plt.xlabel("Number of Offensive Injuries")
    # plt.ylabel("Average Pocket Score")
    # plt.title("Score vs Off Injuries")
    # # Analysis 2 - Score vs Num Defensive Injuries
    # plt.subplot(rows,cols,2)
    # sns.scatterplot(data=analysis_results, y='avgPocketScore', x='numDefInjuries')
    # plt.xlabel("Number of Defensive Injuries")
    # plt.ylabel("Average Pocket Score")
    # plt.title("Score vs Def Injuries")


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
    width = 20
    height = 20
    plt.figure(figsize=(width,height))
    # Number of subplots
    rows = 2
    cols = 2
    # Analysis 1 - Score vs Have Linemen Failed?
    plt.subplot(rows,cols,1)
    sns.violinplot(data=analysis_results, y='pocketScore', x='have_linemen_failed', palette=['seagreen', 'lightcoral'])
    plt.xlabel("Have Off Linemen Failed?")
    plt.ylabel("Pocket Score")
    plt.title("Score vs Have Off Linemen Failed?")
    # Analysis 1 - Score vs Pass Complete
    plt.subplot(rows,cols,2)
    sns.violinplot(data=analysis_results, y='pocketScore', x='pass_complete', palette=['lightcoral', 'seagreen'])
    plt.xlabel("Was pass complete?")
    plt.ylabel("Pocket Score")
    plt.title("Score vs Was Pass Complete?")
    # Analysis 2 - Score vs Pocket hold
    plt.subplot(rows,cols,3)
    sns.violinplot(data=analysis_results, y='pocketScore', x='was_qb_sacked', palette=['seagreen', 'lightcoral'])
    plt.xlabel("Was QB sacked?")
    plt.ylabel("Pocket Score")
    plt.title("Score vs Was QB Sacked?")
    # Analysis 3 - Score vs QB Out of Pocket
    plt.subplot(rows,cols,4)
    sns.violinplot(data=analysis_results, y='pocketScore', x='did_qb_stay_in_pocket', palette=['lightcoral', 'seagreen'])
    plt.xlabel("Did QB stay in pocket?")
    plt.ylabel("Pocket Score")
    plt.title("Score vs Did QB Stay in Pocket?")
    
    # #################################################################
    # # Formation analysis
    # # Figure height and width
    # height = 10
    # width = 40
    # plt.figure(figsize=(width,height))
    # # Number of subplots
    # rows = 1
    # cols = 4
    # # Analysis 1 - Score vs # RB
    # plt.subplot(rows,cols,1)
    # sns.scatterplot(data=analysis_results, y='pocketScore', x='num_rb')
    # plt.xlabel("Number of RB")
    # plt.ylabel("Pocket Score")
    # plt.title("Score vs # RB")
    # # Analysis 2 - Score vs # WR
    # plt.subplot(rows,cols,2)
    # sns.scatterplot(data=analysis_results, y='pocketScore', x='num_wr')
    # plt.xlabel("Number of WR")
    # plt.ylabel("Pocket Score")
    # plt.title("Score vs # WR")
    # # Analysis 3 - Score vs # TE
    # plt.subplot(rows,cols,3)
    # sns.scatterplot(data=analysis_results, y='pocketScore', x='num_te')
    # plt.xlabel("Number of TE")
    # plt.ylabel("Pocket Score")
    # plt.title("Score vs # TE")
    # # Analysis 4 - Score vs # OL
    # plt.subplot(rows,cols,4)
    # sns.scatterplot(data=analysis_results, y='pocketScore', x='num_ol')
    # plt.xlabel("Number of OL")
    # plt.ylabel("Pocket Score")
    # plt.title("Score vs # OL")

    # #################################################################
    # # Foul analysis
    # # Figure height and width
    # height = 10
    # width = 20
    # plt.figure(figsize=(width,height))
    # # Number of subplots
    # rows = 1
    # cols = 2
    # # Analysis 1 - Score vs Num Offensive Fouls
    # plt.subplot(rows,cols,1)
    # sns.scatterplot(data=analysis_results, y='pocketScore', x='num_off_foul')
    # plt.xlabel("Number of Offensive Fouls")
    # plt.ylabel("Pocket Score")
    # plt.title("Score vs Off Fouls")
    # # Analysis 2 - Score vs Num Defensive Fouls
    # plt.subplot(rows,cols,2)
    # sns.scatterplot(data=analysis_results, y='pocketScore', x='num_def_foul')
    # plt.xlabel("Number of Defensive Fouls")
    # plt.ylabel("Pocket Score")
    # plt.title("Score vs Def Fouls")
    
    # #################################################################
    # # Injury analysis
    # # Figure height and width
    # height = 10
    # width = 20
    # plt.figure(figsize=(width,height))
    # # Number of subplots
    # rows = 1
    # cols = 2
    # # Analysis 1 - Score vs Num Offensive Injuries
    # plt.subplot(rows,cols,1)
    # sns.scatterplot(data=analysis_results, y='pocketScore', x='num_off_injuries')
    # plt.xlabel("Number of Offensive Injuries")
    # plt.ylabel("Pocket Score")
    # plt.title("Score vs Off Injuries")
    # # Analysis 2 - Score vs Num Defensive Injuries
    # plt.subplot(rows,cols,2)
    # sns.scatterplot(data=analysis_results, y='pocketScore', x='num_def_injuries')
    # plt.xlabel("Number of Defensive Injuries")
    # plt.ylabel("Pocket Score")
    # plt.title("Score vs Def Injuries")

def evaluate_time_series_score(play_scores_and_features):

    """
    Generate a set of plots describing the time series evolution of a pocket score
    :param play_scores_and_features: Information extracted from Pocket analysis
    """

    # Convert DataFrame to unrolled version for time series
    timeseries = []
    for play_score in play_scores_and_features.iterrows():
        for idx, timepoint in enumerate(play_score[1].pocketScoreTimeSeries):
            if idx <= 80:
                timeseries.append({
                    'frameId': idx,
                    'frameValue': timepoint,
                    'achieved_pos_yards': play_score[1].achieved_pos_yards,
                    "was_qb_sacked": play_score[1].was_qb_sacked,
                    "did_qb_stay_in_pocket": play_score[1].did_qb_stay_in_pocket,
                    "have_linemen_failed": play_score[1].have_linemen_failed,
                    "pocket_outcome": play_score[1].pocket_outcome,
                    "pass_complete": play_score[1].pass_complete,
                })

    df_timeseries = pd.DataFrame(timeseries)

    # Pocket Type Time Series
    plt.figure(figsize=(8,6))
    sns.lineplot(data=df_timeseries, x='frameId', y='frameValue', hue='pocket_outcome', ci=95)
    plt.ylabel("Pocket Score")
    plt.title("Pocket Score Analysis - Pocket Outcome")
    plt.legend()
    plt.show()

    # Have Linemen Failed? Time Series
    plt.figure(figsize=(8,6))
    sns.lineplot(data=df_timeseries, x='frameId', y='frameValue', hue='have_linemen_failed', ci=95)
    plt.ylabel("Pocket Score")
    plt.title("Pocket Score Analysis - Have Linemen Failed?")
    plt.legend()
    plt.show()

    # Did QB stay in pocket? Time Series
    plt.figure(figsize=(8,6))
    sns.lineplot(data=df_timeseries, x='frameId', y='frameValue', hue='did_qb_stay_in_pocket', ci=95)
    plt.ylabel("Pocket Score")
    plt.title("Pocket Score Analysis - Did QB stay in pocket?")
    plt.legend()
    plt.show()

    # Was QB Sacked? Time Series
    plt.figure(figsize=(8,6))
    sns.lineplot(data=df_timeseries, x='frameId', y='frameValue', hue='was_qb_sacked', ci=95)
    plt.ylabel("Pocket Score")
    plt.title("Pocket Score Analysis - Was QB sacked?")
    plt.legend()
    plt.show()

    # Achieved Pos Yards Time Series
    plt.figure(figsize=(8,6))
    sns.lineplot(data=df_timeseries, x='frameId', y='frameValue', hue='pass_complete', ci=95)
    plt.ylabel("Pocket Score")
    plt.title("Pocket Score Analysis - Was pass completed?")
    plt.legend()
    plt.show()

    # # Display score time series 
    # # Analyze - Raw Pocket Score
    # plt.figure(figsize=(8,6))
    # legend_labels = []
    # for play_score in play_scores_and_features.iterrows():
    #     plt.plot(play_score[1].pocketScoreTimeSeries)
    #     legend_labels.append(str(play_score[0][0]) + ' - ' + str(play_score[0][1]))

    # plt.xlabel("FrameId")
    # plt.ylabel("Pocket Score")
    # plt.title("Raw Pocket Score Analysis")
    # plt.legend(legend_labels)
    # plt.show()

    # # Analyze - Pocket Score vs Pass Complete
    # plt.figure(figsize=(8,6))
    # legend_labels = []
    # for play_score in play_scores_and_features.iterrows():
    #     if play_score[1].pass_complete == True:
    #         colour = "seagreen"
    #     else:
    #         colour = "lightcoral"
    #     plt.plot(play_score[1].pocketScoreTimeSeries, c=colour)
    #     legend_labels.append(str(play_score[0][0]) + ' - ' + str(play_score[0][1]))

    # plt.xlabel("FrameId")
    # plt.ylabel("Pocket Score")
    # plt.title("Pass Complete Analysis")
    # plt.legend(legend_labels)
    # plt.show()

    # # Analyze - Pocket Score vs Has Pocket Hold
    # plt.figure(figsize=(8,6))
    # for play_score in play_scores_and_features.iterrows():
    #     if play_score[1].has_pocket_hold == True:
    #         colour = "seagreen"
    #     else:
    #         colour = "lightcoral"
    #     plt.plot(play_score[1].pocketScoreTimeSeries, c=colour)
    #     legend_labels.append(str(play_score[0][0]) + ' - ' + str(play_score[0][1]))

    # plt.xlabel("FrameId")
    # plt.ylabel("Pocket Score")
    # plt.title("Has Pocket Hold? Analysis")
    # plt.legend(legend_labels)
    # plt.show()

    # # Analyze - Pocket Score vs Has Pocket Hold
    # plt.figure(figsize=(8,6))
    # for play_score in play_scores_and_features.iterrows():
    #     if play_score[1].was_qb_sacked == False:
    #         colour = "seagreen"
    #     else:
    #         colour = "lightcoral"
    #     plt.plot(play_score[1].pocketScoreTimeSeries, c=colour)
    #     legend_labels.append(str(play_score[0][0]) + ' - ' + str(play_score[0][1]))


    # plt.xlabel("FrameId")
    # plt.ylabel("Pocket Score")
    # plt.title("Was QB sacked? Analysis")
    # plt.legend(legend_labels)
    # plt.show()

    # # Analyze - Pocket Score vs Has QB remained in Pocket
    # plt.figure(figsize=(8,6))
    # for play_score in play_scores_and_features.iterrows():
    #     if play_score[1].did_qb_stay_in_pocket == True:
    #         colour = "seagreen"
    #     else:
    #         colour = "lightcoral"
    #     plt.plot(play_score[1].pocketScoreTimeSeries, c=colour)
    #     legend_labels.append(str(play_score[0][0]) + ' - ' + str(play_score[0][1]))


    # plt.xlabel("FrameId")
    # plt.ylabel("Pocket Score")
    # plt.title("Did QB Remain in Pocket? Analysis")
    # plt.legend(legend_labels)
    # plt.show()