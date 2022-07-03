# dictionary that defines the range for game data
game_range_dict = {
    "Possession": [10, 90],
    "Shots": [0, 30],
    "ExpectedGoals": [0, 20],
    "Passes": [0, 500],
    "Tackles": [0, 100],
    "TacklesWon": [0, 100],
    "Interceptions": [0, 100],
    "Saves": [0, 100],
    "FoulsCommitted": [0, 100],
    "Offsides": [0, 100],
    "Corners": [0, 100],
    "FreeKicks": [0, 100],
    "PenaltyKicks": [0, 10],
    "YellowCards": [0, 11],
    "RedCards": [0, 6],
    "DribbleSuccessRate": [0, 100],
    "ShotAccuracy": [0, 100],
    "PassAccuracy": [0, 100]
}

# dictionary that defines the range for player data
player_range_dict = {
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


def check_game_sanity(input_dict):
    """
    Checks if the values of the given dictionary match the possible range for a game.
    The range is defined in the dictionary game_range_dict.
    If a value is not in the range it is set to -1.

    Parameters:
        input_dict(dict): the dictionary to check
    """
    for key in game_range_dict:
        pos_range = game_range_dict[key]
        value = input_dict[key]

        for i in range(2):
            if not (pos_range[0] <= value[i] <= pos_range[1]):
                input_dict[key][i] = -1


def check_player_sanity(input_dict):
    """
    Checks if the values of the given dictionary match the possible range for a player.
    The range is defined in the dictionary player_range_dict.
    If a value is not in the range it is set to -1.

    Parameters:
        input_dict(dict): the dictionary to check
    """
    for key in player_range_dict:
        pos_range = player_range_dict[key]
        value = input_dict[key]
        if not (pos_range[0] <= value <= pos_range[1]):
            input_dict[key] = -1
