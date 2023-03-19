import json
import os
import numpy as np
import platform

from . import goal as goal_class
from . import assist as assist_class

curr_dir = os.getcwd()
# get the path up until repo parent
pro_clubs_index = curr_dir.find("pro-clubs")
path_to_pro_clubs_root = curr_dir[:pro_clubs_index]
# set global variable for path to game_data file
DATA_PATH = (path_to_pro_clubs_root + "pro-clubs/src/data/")
FULL_GAME_DATA_PATH = DATA_PATH + "game_data.json"
FULL_PLAYER_DATA_PATH = DATA_PATH + "player_data/"

PLATFORM = platform.system()

if (PLATFORM == "Windows"):
  DATA_PATH = (path_to_pro_clubs_root + "pro-clubs\\src\\data\\")
  FULL_PLAYER_DATA_PATH = DATA_PATH + "player_data\\"


def read_json(path):
  """
  Read in json file from a given path and return the full struct

  Parameters:
    path(string): Absolute path from caller to json file

  Returns:
    full_data(dict): full structure of the json file
  """
  with open(path, "r") as file:
    full_data = json.load(file)
  return full_data


def write_json(full_data, path):
  """
  Write a given json struct(dict) into a file given the absolute path
  from the caller.

  Parameters:
    full_data(dict): Full data to be stored
    path(str): path to json file to write
  """
  data_to_write = json.dumps(full_data, indent=2)
  with open(path, "w") as file_to_write:
    file_to_write.write(data_to_write)


class Game:

  def __init__(self, div, div_n_game, points_before, player_names,
               any="", home=True):
    """
    Parameters:
      ID(int): unique game ID
      div(int): division of the game
      div_n_game(int): nth game of the division (valid range 1-10)
      points_before(int): Points before the game (needed in case not
                          all games are stored)
      player_names(list<str>): Names of all players in the game
      any(str): Name of the player who is the any
      home(bool): Whether or not the game is a home or away game
    """
    
    self.player_names = player_names
    self.home = home
    self.score = [0, 0]
    
    # set the current IDs which are incremented at each goal
    self.curr_goal_ID = 0
    self.curr_assist_ID = 0

    # list of all goals, good for printing goal info
    self.goal_list = []

    self.dict_to_write = {}  # to write in json at the end

    # get the most recent ID
    prev_ID = read_json(FULL_GAME_DATA_PATH)[-1]["GAME_ID"]

    self.dict_to_write["GAME_ID"] = prev_ID + 1
    self.dict_to_write["DIVISION"] = div
    self.dict_to_write["DIV_GAME_NO"] = div_n_game
    self.dict_to_write["POINTS_BEFORE"] = points_before
    # put placeholders for 
    self.dict_to_write["RESULT"] = []
    self.dict_to_write["RESULT_TYPE"] = ""
    # can set the following right away
    self.dict_to_write["ANY"] = any
    self.dict_to_write["HOME"] = int(home)
    # Empty lists is better than non-existent for analysing
    self.dict_to_write["GOALS_FOR"] = []
    self.dict_to_write["ASSISTS"] = []
    self.dict_to_write["GOALS_AGAINST"] = []
    self.dict_to_write["PLAYER_DATA"] = []


  def add_goal_against(self, minute, stoppage_time=None, pen=False, og=None):
    """
    Add a goal to the opponents tally

    Parameters:
      minute(int): Minute in which the goal was scored
      stoppage_time(int): the minute in stoppage time.
                          Only not None when minute is 45 or 90
      pen(bool): If the goal is a penalty
      og(str): If the goal is an own goal, this will be the name
                of the player who scored it
    """
    if (self.home):
      self.score[1] += 1
    else:
      self.score[0] += 1

    goal = goal_class.Goal(minute, tuple(self.score), stoppage_time=stoppage_time,
                           is_pen=pen, og=og)
    self.goal_list.append(goal)
    # get the goal in neat dict form to write to json
    goal_dict = goal.get_dict_struct()
    self.dict_to_write["GOALS_AGAINST"].append(goal_dict)


  def add_goal_for(self, minute, player_name="", assister="", stoppage_time=None,
                   pen=False, og=False):
    """
    Simple function to add a goal to a player's tally
    and to the game in general

    Parameters:
      minute(int): Minute in which the goal was scored
      player_name(str): Name of player who scored the goal
      assister(str): Name of the player who assisted. If none then
                     no assist is written.
      pen(bool): If the goal is a penalty
      og(bool): If the goal is an own goal
    """
    if (self.home):
      self.score[0] += 1
    else:
      self.score[1] += 1

    goal = goal_class.Goal(minute, self.score.copy(), stoppage_time=stoppage_time,
                           player_name=player_name, id=self.curr_goal_ID, is_pen=pen,
                           og=og)

    if (assister != ""):  # Empty means no assister
      goal.add_assist(self.curr_assist_ID)
      assist = assist_class.Assist(self.curr_assist_ID, self.curr_goal_ID,
                                   assister)
      # get the assist in neat dict form to write to json
      assist_dict = assist.get_dict_struct()
      self.dict_to_write["ASSISTS"].append(assist_dict)

      self.curr_assist_ID += 1  # move to next unique ID

    self.goal_list.append(goal)
    goal_dict = goal.get_dict_struct()
    self.dict_to_write["GOALS_FOR"].append(goal_dict)

    self.curr_goal_ID += 1


  def end_game(self):
    """
    This function is triggered when the game ends, sets the final score
    """
    self.dict_to_write["RESULT"] = self.score.copy()
    res_type = ""
      
    if(self.score[0] > self.score[1]):  # home win
      if (self.home):
        res_type = "W"
      else:
        res_type = "L"

    elif(self.score[0] == self.score[1]):  # draw
        res_type = "D"
    
    else:  # self.score[0] < self.score[1], away win
      if (self.home):
        res_type = "L"
      else:
        res_type = "W"

    self.dict_to_write["RESULT_TYPE"] = res_type

  
  def add_player_data(self, all_player_data):
    """
    Take data that has been read by the computer from the final
    stats screen, and pass it as a dictionary for each player name.

    This function can be called several times with each dict being
    a different player, or be called once with all the data right away.

    Parameters:
      all_player_data(list): List of dicts of fields such as "Goals" as keys
                             to values (e.g. 2)
    """
    for player_data in all_player_data:
        # the name of the player is a field in player_data
        self.dict_to_write["PLAYER_DATA"].append(player_data)


  
  def add_match_data(self, match_data):
    """
    Take data that has been read from the final match stats screen.

    Parameters:
      match_data(dict): Keys are the fields (such as "Goals") and the
                        values are length 2 lists, so the values for
                        home and away for the given attribute
    """
    fields = list(match_data.keys())
    values = np.array(list(match_data.values()))  # for slicing
    
    home_values = values[:, 0]
    away_values = values[:, 1]

    home_dict = dict(zip(fields, home_values))
    away_dict = dict(zip(fields, away_values))

    self.dict_to_write["HOME_MATCH_DATA"] = home_dict
    self.dict_to_write["AWAY_MATCH_DATA"] = away_dict


  
  def write_all_data(self):
    """
    Write the entire game data to the game_data.json file using
    the dict_to_write field that has been set throughout
    """
    curr_data = read_json(FULL_GAME_DATA_PATH)  # read game data before

    curr_data.append(self.dict_to_write)  # append this game's data

    write_json(curr_data, FULL_GAME_DATA_PATH)  # write back to original file

    # add the game ID to the player data of the players who were present
    for player in self.player_names:
      player_path = FULL_PLAYER_DATA_PATH + player + ".json"
      player_match_data = read_json(player_path)
      player_match_data["GAME_ID"].append(self.dict_to_write["GAME_ID"])
      write_json(player_match_data, player_path)