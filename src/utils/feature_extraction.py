import os
import re
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append('../')
from definitions.fouls_def import ignore_fouls

def extract_play_outcome_features(plays_data):

    '''
    Function to extract information regarding the outcome of the provided plays
    :param plays_data: DataFrame containing plays raw information 
    :return: DataFrame with information regarding plays outcome
    '''

    play_outcome = pd.DataFrame()

    # Play Identifiers
    play_outcome['gameId'] = plays_data.gameId
    play_outcome['playId'] = plays_data.playId
    # pass_complete - Self-explanatory
    play_outcome['pass_complete'] = plays_data.passResult.apply(lambda x : True if (x=='C') else False)
    # Has_pocket_hold - This feature answers the question, was the QB able to pass inside the pocket? 
    # This includes C, I and IN; as in all these plays the QB is able to pass the ball
    play_outcome['has_pocket_hold'] = plays_data.passResult.apply(lambda x : True if (x=='C')|(x=='I')|(x=='IN') else False)
    # was_qb_sacked - Self-explanatory 
    play_outcome['was_qb_sacked'] = plays_data.passResult.apply(lambda x : True if (x=='S') else False)
    # achieved_positive_yards - Self-explanatory, binary result
    play_outcome['achieved_pos_yards'] = plays_data.playResult.apply(lambda x: True if (x>0) else False)
    # gained_yards - Self-explanatory
    play_outcome['gained_yards'] = plays_data.playResult
    # touchdown - Self-explanatory
    play_outcome['touchdown'] = plays_data.playDescription.apply(lambda x: False if re.search('touchdown', x.lower()) == None else True)
    
    return play_outcome


def extract_formation_features(plays_data):

    '''
    Function to extract information regarding the initial formation of the provided plays
    :param plays_data: DataFrame containing plays raw information 
    :return: DataFrame with information regarding plays formation
    '''

    play_formation = pd.DataFrame()

    # Play Identifiers
    play_formation['gameId'] = plays_data.gameId
    play_formation['playId'] = plays_data.playId

    # Set of features describing the formation
    # num_XX - # of players on the position
    # Possible positions:
    # RB -> Running Back
    # QB -> Quarterback - Ignore for now, this is not relevant
    # WR -> ???? - Need to check
    # TE -> ???? - Need to check
    # OL -> Offensive Lineman? - Need to check
    num_wr = plays_data.personnelO.astype(str).apply(extract_number_players_regexp, pattern='\d WR')
    num_qb = plays_data.personnelO.astype(str).apply(extract_number_players_regexp, pattern='\d QB')
    play_formation['num_rb'] = plays_data.personnelO.astype(str).apply(extract_number_players_regexp, pattern='\d RB')
    play_formation['num_wr'] = num_wr
    play_formation['num_te'] = plays_data.personnelO.astype(str).apply(extract_number_players_regexp, pattern='\d TE')
    play_formation['num_qb'] = num_qb
    play_formation['num_ol'] = 11 - num_wr - num_qb
    # Note - Would we obtain the same result if we check the players position? 

    # Extract the offense formation used
    play_formation['formation'] = plays_data.offenseFormation

    return play_formation

def extract_foul_features(plays_data):

    '''
    Function to extract information regarding the fouls that happened in the provided plays
    :param plays_data: DataFrame containing plays raw information 
    :return: DataFrame with information regarding plays fouls, including side, type of foul and player
    '''

    play_foul = pd.DataFrame()

    # Play Identifiers
    play_foul['gameId'] = plays_data.gameId
    play_foul['playId'] = plays_data.playId

    # How to detect an offensive/defensive foul:
    # 1- The word "Penalty on XX" is found
    # 2- The "possesionTeam"/"defensiveTeam" is equal to XX
    # 3- The foul called should not be ignored
    foul_info = plays_data.apply(determine_foul_side, axis=1)

    # I hate this way of solving this, but I don;t have internet to get a better way
    off_foul = []
    off_penalty = []
    off_players = []
    def_foul = []
    def_penalty = []
    def_players = []
    for record in foul_info:
        off_foul.append(record[0])
        off_penalty.append(record[1])
        off_players.append(record[2])
        def_foul.append(record[3])
        def_penalty.append(record[4])
        def_players.append(record[5])

    # Assign to DataFrame
    play_foul['num_off_foul'] = off_foul
    play_foul['off_penalties'] = off_penalty
    play_foul['off_penalties_players'] = off_players
    play_foul['num_def_foul'] = def_foul 
    play_foul['def_penalties'] = def_penalty
    play_foul['def_penalties_players'] = def_players

    return play_foul

def extract_injury_features(plays_data):

    '''
    Function to extract information regarding the injuries that happened in the provided plays
    :param plays_data: DataFrame containing plays raw information 
    :return: DataFrame with information regarding plays injuries, including side and player involved
    '''

    play_injury = pd.DataFrame()

    # Play Identifiers
    play_injury['gameId'] = plays_data.gameId
    play_injury['playId'] = plays_data.playId

    # How to detect an offensive/defensive injury:
    # 1- The word "XX-<Full Name> was injured during the play" is found
    # 2- The "possesionTeam"/"defensiveTeam" is equal to XX
    injury_info = plays_data.apply(determine_injury_side, axis=1)

    # I hate this way of solving this, but I don;t have internet to get a better way
    off_injury = []
    off_players = []
    def_injury = []
    def_players = []
    for record in injury_info:
        off_injury.append(record[0])
        off_players.append(record[1])
        def_injury.append(record[2])
        def_players.append(record[3])

    # Assign to DataFrame
    play_injury['num_off_injuries'] = off_injury
    play_injury['off_players_injured'] = off_players
    play_injury['num_def_injuries'] = def_injury 
    play_injury['def_players_injured'] = def_players

    return play_injury

def extract_game_features(games_data):
    '''
    Function to extract game features
    :param games_data: DataFrame containing games raw information
    :return: DataFrame with gameId and associated data
    '''

    return games_data.groupby(['gameId']).apply(process_game_record).reset_index(level=1, drop=True)

def extract_plays_features(input_path):
    """
    Function to extract features associated with the plays
    :param input_path: Path to raw data
    :return: DataFrame with gameId, playId and associated data
    """

    # Define number of weeks to analyize
    num_weeks = 8

    # Generate files names
    week_files = []
    for i in range(num_weeks):
        week_files.append(f'week{i+1}.csv')

    # For all weeks, extract scores
    all_plays_length = []
    for week_file in week_files:

        # Load information for an entire week
        week_data = pd.read_csv(os.path.join(input_path, week_file))

        # Obtain the play length information
        play_length = week_data.groupby(['gameId', 'playId']).apply(calculate_total_play_time)
        pass_time_length = week_data.groupby(['gameId', 'playId']).apply(calculate_time_to_pass)
        all_plays_length.append(pd.DataFrame({
            'play_length': play_length,
            'time_to_pass': pass_time_length
        }))

    return pd.concat(all_plays_length, axis=0)

def extract_did_qb_stay_in_pocket(week_data, player_data, config):
    qb_escape_data = \
        (player_data\
            .set_index("nflId")\
            .join(week_data.set_index("nflId"), how="right")\
            .query("(officialPosition == 'QB' or team == 'football')")\
            .groupby(['gameId', 'playId'])
            )


    gameId = []
    playId = []
    values = []

    for name, play_df in qb_escape_data:
        gameId.append(name[0])
        playId.append(name[1])
        values.append(did_qb_stay_in_pocket(play_df, config))

    data = \
        {'gameId': gameId,
        'playId': playId,
        'did_qb_stay_in_pocket': values}

    return(pd.DataFrame(data))

################################################################

################################################################
# AUX FUNCTIONS

def extract_number_players_regexp(x, pattern):

    '''
    Function supporting the extraction of formation features by performing RegExp
    :param x: Individual record of personnel (Usually personelO)
    :param pattern: Pattern to find, representing one of the positions
    :return: Number of players on the position associated with the pattern
    '''

    # Match pattern
    match = re.search(pattern, x)

    # If pattern not available, return 0
    if match == None:
        return 0
    # Else, return the number
    else:
        return int(match[0][0])

def determine_foul_side(x):
    
    '''
    Function supporting the extraction of foul features by performing RegExp
    :param x: Individual play record 
    :return: Foul features associated with associated play
    '''

    # Define pattern - Acept teams with either 2 or 3 letters
    pattern = 'penalty on [a-z]{2,3}-[a-z]\.[a-z]*,'

    # Extract valuable fields
    descrip = x.playDescription.lower()
    offense = x.possessionTeam.lower()
    defense = x.defensiveTeam.lower() 

    # Create final variables
    off_foul = 0
    off_penalty = []
    off_players = []
    def_foul = 0
    def_penalty = []
    def_players = []

    matches = re.findall(pattern, descrip)
    if matches!=[]:
        for idx, match in enumerate(matches):
            # Extract team from string
            team = match.split(" ")[-1].split("-")[0]
            player = match.split(" ")[-1].split("-")[1].replace(",","")
            
            # Determine whether it is a valid foul
            foul_number = idx + 1
            foulCol = f"foulName{foul_number}"
            foulName = x[foulCol]
            if foulName in ignore_fouls:
                next

            # Determine which team has committed the foul & store the penalty  
            if team == offense:
                off_foul += 1
                off_penalty.append(x[foulCol])
                off_players.append(player)
            elif team == defense:
                def_foul += 1
                def_penalty.append(x[foulCol])
                def_players.append(player)

            else:
                assert False, "Foul to neither team??"

    return off_foul, off_penalty, off_players, def_foul, def_penalty, def_players

def determine_injury_side(x):
    
    '''
    Function supporting the extraction of injury features by performing RegExp
    :param x: Individual play record 
    :return: Injury features associated with associated play
    '''

    # Define pattern - Acept teams with either 2 or 3 letters
    pattern = '[a-z]{2,3}-[a-z]\.[\s\-a-z]* was injured'

    # Extract valuable fields
    descrip = x.playDescription.lower()
    offense = x.possessionTeam.lower()
    defense = x.defensiveTeam.lower() 

    # Create final variables
    off_injury = 0
    off_players = []
    def_injury = 0
    def_players = []

    matches = re.findall(pattern, descrip)
    
    if matches!=[]:
        for idx, match in enumerate(matches):

            # Extract team from string
            team = match.split("-")[0].split(" ")[-1]
            player = match.replace(" was injured", "").split("-", 1)[1]

            # Determine which team has an injured player
            if team == offense:
                off_injury += 1
                off_players.append(player)
            elif team == defense:
                def_injury += 1
                def_players.append(player)
            else:
                assert False, "Injury to neither team??"

    return off_injury, off_players, def_injury, def_players

def process_game_record(game):
    '''
    Function supporting the extraction of game features
    :param game: Individual game record
    :return: Game features
    '''
    
    teams = [game['homeTeamAbbr'].values[0], game['visitorTeamAbbr'].values[0]]
    scores = [game['homeScore'].values[0], game['visitorScore'].values[0]]
    hasWon = [False, False]

    if (game['whoWon'].values == game['homeTeamAbbr'].values):
        hasWon[0] = True
    else:
        hasWon[1] = True

    return pd.DataFrame({
        'team': teams,
        'gameScore': scores,
        'hasWon': hasWon
    })    

def calculate_total_play_time(play):
    '''
    Function supporting the extraction of play time
    :param game: Individual play record
    :return: Play time
    '''

    # Time to Play End
    time_to_end = max(play.frameId * 0.1)
    # Time to Play Snap
    time_to_snap = play.loc[play.event == "ball_snap", 'frameId']
    if time_to_snap.empty:
        time_to_snap = 0
    else:
        time_to_snap = time_to_snap.values[0] * 0.1

    return time_to_end - time_to_snap

def calculate_time_to_pass(play):
    '''
    Function supporting the extraction of time to pass
    :param game: Individual play record
    :return: Time to Pass
    '''

    # Time to Play Pass
    time_to_pass = play.loc[play.event == "pass_forward", 'frameId']
    if time_to_pass.empty:
        return None
    else:
        time_to_pass = time_to_pass.values[0] * 0.1
    
    # Time to Play Snap
    time_to_snap = play.loc[play.event == "ball_snap", 'frameId']
    if time_to_snap.empty:
        time_to_snap = 0
    else:
        time_to_snap = time_to_snap.values[0] * 0.1
    return time_to_pass - time_to_snap

def find_pocket_limits(play_df, config):

    """ 
    Takes position-level dataframe and returns the limits for pockets
    Performs the following actions
    1 - Extract football location in first frame
    2 - calculates x-limits for pocket based on playDirection and pocket_len
    3 - calculates y-limits for pocket based on pocket_len
    :param play_df: dataframe for a single play containing position-level data
    :param config: parameterized pipeline inputs.  Specifically uses the pocket_len parameter 
    """


    football_info = play_df.loc[(play_df['frameId']==1) & (play_df['team']=='football'), ['x','y', 'playDirection']]
    

    if football_info['playDirection'].values[0]=="right":
        xlims=(football_info['x'].values[0]-config["pocket_len"], football_info['x'].values[0])
    else:
        xlims=(football_info['x'].values[0], football_info['x'].values[0]+config["pocket_len"])

    ylims=(football_info['y'].values[0]-config["pocket_len"]/2, football_info['y'].values[0]+config["pocket_len"]/2)

    return(xlims, ylims)

class pocket_limits:

    """ 
    Class to house pocket limits
    Contains the following functions
    1- is_inside_x: -> Bool 
            using the xlimits, tests whether a given x-value is inside or outside the range
    2- is_inside_y: -> Bool
            using the y-limits, tests whether a given y-value is inside or outside the range
    3- is_point_inside_pocket: -> Bool
            tests whether a given point is inside or outside of the square defined by xlims, ylims
    """

    def __init__(self, xlims, ylims):
        self.x_lower=xlims[0]
        self.x_upper=xlims[1]
        self.y_lower=ylims[0]
        self.y_upper=ylims[1]
    
    def is_inside_x(self, x_value):
        return(x_value<self.x_upper and x_value>self.x_lower)
        
    def is_inside_y(self, y_value):
        return(y_value<self.y_upper and y_value>self.y_lower)

    def is_point_inside_pocket(self, x_value, y_value):
        return(self.is_inside_x(x_value) and self.is_inside_y(y_value))

def did_qb_stay_in_pocket(play_df, config):

    """ 
    function that determines whether a quarterback stayed inside the pocket prior to throwing the football
    Performs the following operations
    1- calculate the pocket limits based on the value of the football in frame one (via find_pocket_limts)
        instantiate a play_pocket object to store the limits
    2- For each observation in play_df, determine whether the player was inside the pocket
        pocket size parameterized by config parameter
    3- finds frame where the pass was thrown
        - takes minimum frameId for event in [pass_forward, autoevent_passforward]
        - if no passforward event occurs, returns maximum frameId for play
    4- checks whether the QB was in the pocket for all pre-pass frames

    :param play_df: 
    :param config:parameterized pipeline inputs.  Specifically uses the pocket_len parameter 
    """

    ## Find Pocket Limits
    xlims, ylims=find_pocket_limits(play_df, config)
    play_pocket=pocket_limits(xlims, ylims)


    play_df['is_currently_in_pocket']=[play_pocket.is_point_inside_pocket(x,y) for x, y in zip(play_df["x"], play_df["y"])]

    ## Find Pass FrameId 
    prepass_frames = play_df.loc[play_df['event'].isin(["pass_forward", 'autoevent_passforward']), 'frameId']    

    if prepass_frames.shape[0]>0:
        frame_of_pass=min(prepass_frames)
    else:
        frame_of_pass=max(play_df['frameId'])


    # Check whether QB was always in pocket before pass was thrown
    qb_stayed_in_pocket = min(play_df.loc[(play_df['frameId']<=frame_of_pass) & (play_df['officialPosition']=='QB'), 'is_currently_in_pocket'])    
        
    
    return(qb_stayed_in_pocket)

################################################################