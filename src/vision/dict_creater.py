import os
import sys

cwd = os.getcwd()
parent = os.path.dirname(cwd)
sys.path.insert(0, parent) 

from static_data import vision_static_data as vst


def get_game_dict(data) :
    game_dict = {}
    misreads = []

    for i in range(len(vst.game_data_attr)):
        key = vst.game_data_attr[i]

        exp_range = vst.game_exp_range_dict[key]
        value_home = data[i]
        value_away = data[i + len(vst.game_data_attr)]

        if not (exp_range[0] <= value_home <= exp_range[1]):
            value_home = -1

        if not (exp_range[0] <= value_away <= exp_range[1]):
            print(value_away)
            value_away = -1

        if value_home == -1:
            misreads.append((0, key))
        if value_away == -1:
            misreads.append((1, key))

        game_dict[key] = [value_home, value_away]

    return game_dict, misreads

def get_player_dict(data, name):
    player_dict = {"NAME": name}
    misreads = []

    for i in range(len(vst.player_data_attr)):
        key = vst.player_data_attr[i]

        exp_range = vst.player_exp_range_dict[key]
        value = data[i]

        if not (exp_range[0] <= value <= exp_range[1]):
            value = -1

        if value == -1:
            misreads.append((name, key))

        player_dict[key] = value

    return player_dict, misreads