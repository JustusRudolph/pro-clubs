MAX_VALUE = 1000000

# list with all attributes of the match facts screen
game_data_attr = ["Possession", "Shots", "ExpectedGoals", "Passes",
    "Tackles", "TacklesWon", "Interceptions"]

# dictionary that defines the expected range for game data
game_exp_range_dict = {
    "Possession": [20, 80],
    "Shots": [0, 30],
    "ExpectedGoals": [0, 20],
    "Passes": [0, 500],
    "Tackles": [0, 100],
    "TacklesWon": [0, 100],
    "Interceptions": [0, 100],
    "Saves": [0, 100],
    "FoulsCommitted": [0, 100],
    "Offsides": [0, 100],
    "Corners": [0, 50],
    "FreeKicks": [0, 50],
    "PenaltyKicks": [0, 10],
    "YellowCards": [0, 11],
    "RedCards": [0, 6],
    "DribbleSuccessRate": [0, 100],
    "ShotAccuracy": [0, 100],
    "PassAccuracy": [40, 90]
}

# dictionary that defines the expected range for player data
player_exp_range_dict = {
    "Rating": [0, 10],
    "Goals": [0, 10],
    "Assists": [0, 10],
    "Shots": [0, 20],
    "ShotAccuracy": [0, 100],
    "Passes": [0, 100],
    "PassAccuracy": [0, 100],
    "Dribbles": [0, 100],
    "DribbleSuccessRate": [0, 100],
    "Tackles": [0, 100],
    "TackleSuccessRate": [0, 100],
    "Offsides": [0, 100],
    "FoulsCommitted": [0, 100],
    "PossessionWon": [0, 100],
    "PossessionLost": [0, 100],
    "MinutesPlayed": [0, 100],
    "DistanceCovered": [0, 100],
    "DistanceSprinted": [0, 100],
    "YellowCard": [0, 1],
    "RedCard": [0, 1]
}

# dictionary that defines the valid range for game data
game_valid_range_dict = {
    "Possession": [0, 100],
    "Shots": [0, MAX_VALUE],
    "ExpectedGoals": [0, MAX_VALUE],
    "Passes": [0, MAX_VALUE],
    "Tackles": [0, MAX_VALUE],
    "TacklesWon": [0, MAX_VALUE],
    "Interceptions": [0, MAX_VALUE],
    "Saves": [0, MAX_VALUE],
    "FoulsCommitted": [0, MAX_VALUE],
    "Offsides": [0, MAX_VALUE],
    "Corners": [0, MAX_VALUE],
    "FreeKicks": [0, MAX_VALUE],
    "PenaltyKicks": [0, MAX_VALUE],
    "YellowCards": [0, 11],
    "RedCards": [0, 11],
    "DribbleSuccessRate": [0, 100],
    "ShotAccuracy": [0, 100],
    "PassAccuracy": [40, 100]
}

# dictionary that defines the valid range for player data
player_valid_range_dict = {
    "Rating": [0, 10],
    "Goals": [0, MAX_VALUE],
    "Assists": [0, MAX_VALUE],
    "Shots": [0, MAX_VALUE],
    "ShotAccuracy": [0, 100],
    "Passes": [0, MAX_VALUE],
    "PassAccuracy": [0, 100],
    "Dribbles": [0, MAX_VALUE],
    "DribbleSuccessRate": [0, 100],
    "Tackles": [0, MAX_VALUE],
    "TackleSuccessRate": [0, 100],
    "Offsides": [0, MAX_VALUE],
    "FoulsCommitted": [0, MAX_VALUE],
    "PossessionWon": [0, MAX_VALUE],
    "PossessionLost": [0, MAX_VALUE],
    "MinutesPlayed": [0, MAX_VALUE],
    "DistanceCovered": [0, MAX_VALUE],
    "DistanceSprinted": [0, MAX_VALUE],
    "YellowCard": [0, 1],
    "RedCard": [0, 1]
}