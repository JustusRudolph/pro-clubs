from static_data import valid_ranges

def check_game_values(input_dict):
    """
    Checks if the values of the given dictionary match the possible range for a game.
    The range is defined in the dictionary game_range_dict.
    If a value is not in the range it is set to -1.

    Parameters:
        input_dict(dict): the dictionary to check
    """
    for key in valid_ranges.game_exp_range_dict:
        pos_range = valid_ranges.game_exp_range_dict[key]
        value = input_dict[key]

        for i in range(2):
            if not (pos_range[0] <= value[i] <= pos_range[1]):
                input_dict[key][i] = -1


def check_player_values(input_dict):
    """
    Checks if the values of the given dictionary match the possible range for a player.
    The range is defined in the dictionary player_range_dict.
    If a value is not in the range it is set to -1.

    Parameters:
        input_dict(dict): the dictionary to check
    """
    for key in valid_ranges.player_exp_range_dict:
        pos_range = valid_ranges.player_exp_range_dict[key]
        value = input_dict[key]
        if not (pos_range[0] <= value <= pos_range[1]):
            input_dict[key] = -1
