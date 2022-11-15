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
    play_formation['num_rb'] = plays_data.personnelO.astype(str).apply(extract_number_players_regexp, pattern='\d RB')
    play_formation['num_wr'] = plays_data.personnelO.astype(str).apply(extract_number_players_regexp, pattern='\d WR')
    play_formation['num_te'] = plays_data.personnelO.astype(str).apply(extract_number_players_regexp, pattern='\d TE')
    play_formation['num_ol'] = plays_data.personnelO.astype(str).apply(extract_number_players_regexp, pattern='\d OL')
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
    def_injury = []
    for record in injury_info:
        off_injury.append(record[0])
        def_injury.append(record[1])

    # Assign to DataFrame
    play_injury['num_off_injuries'] = off_injury
    play_injury['num_def_injuries'] = def_injury 

    return play_injury

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
    pattern = '\. [a-z]{2,3}-[a-z]\..* was injured'

    # Extract valuable fields
    descrip = x.playDescription.lower()
    offense = x.possessionTeam.lower()
    defense = x.defensiveTeam.lower() 

    # Create final variables
    off_injury = 0
    def_injury = 0

    matches = re.findall(pattern, descrip)
    if matches!=[]:
        for idx, match in enumerate(matches):
            # Extract team from string
            team = match.split("-")[0].split(" ")[-1]

            # Determine which team has an injured player
            if team == offense:
                off_injury += 1
            elif team == defense:
                def_injury += 1
            else:
                assert False, "Injury to neither team??"

    return off_injury, def_injury

################################################################