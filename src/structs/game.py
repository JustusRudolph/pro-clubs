import json
import os

from numpy import full

from . import goal as goal_class
from . import assist as assist_class

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

  def __init__(self, ID, player_names, any="", home=True):
    self.player_names = player_names
    self.home = home
    self.score = [0, 0]
    
    # set the current IDs which are incremented at each goal
    self.curr_goal_ID = 0
    self.curr_assist_ID = 0

    self.dict_to_write = {}  # to write in json at the end

    self.dict_to_write["GAME_ID"] = ID
    self.dict_to_write["HOME"] = int(home)
    # put placeholders for 
    self.dict_to_write["RESULT"] = []
    self.dict_to_write["RESULT_TYPE"] = ""
    self.dict_to_write["ANY"] = any
    self.dict_to_write["GOALS_FOR"] = []  # empty instead of nonexistent
    self.dict_to_write["ASSISTS"] = []
    self.dict_to_write["GOALS_AGAINST"] = []


  def add_goal_against(self, minute, pen=False):
    """
    Add a goal to the opponents tally

    Parameters:
      minute(int): Minute in which the goal was scored
    """
    if (self.home):
      self.score[1] += 1
    else:
      self.score[0] += 1

    goal = goal_class.Goal(minute, tuple(self.score), is_pen=pen)
    # get the goal in neat dict form to write to json
    goal_dict = goal.get_dict_struct()
    self.dict_to_write["GOALS_AGAINST"].append(goal_dict)


  def add_goal_for(self, minute, player_name, assister=None, pen=False):
    """
    Simple function to add a goal to a player's tally
    and to the game in general

    Parameters:
      minute(int): Minute in which the goal was scored
      player_name(str): Name of player who scored the goal
      assister(str): Name of the player who assisted. If none then
                     no assist is written.
    """
    if (self.home):
      self.score[0] += 1
    else:
      self.score[1] += 1

    goal = goal_class.Goal(minute, self.score.copy(), player_name,
                           self.curr_goal_ID, is_pen=pen)

    if (assister is not None):
      goal.add_assist(self.curr_assist_ID)
      assist = assist_class.Assist(self.curr_assist_ID, self.curr_goal_ID,
                                   assister)
      # get the assist in neat dict form to write to json
      assist_dict = assist.get_dict_struct()
      self.dict_to_write["ASSISTS"].append(assist_dict)

      self.curr_assist_ID += 1  # move to next unique ID

    goal_dict = goal.get_dict_struct()
    self.dict_to_write["GOALS_FOR"].append(goal_dict)

    self.curr_goal_ID += 1


  def end_game(self):
    """
    This function is triggered when the game ends, sets the final score
    """
    self.dict_to_write["RESULTS"] = self.score.copy()
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

  
  def add_player_data(self, player_data):
    """
    Take data that has been read by the computer from the final
    stats screen, and pass it as a dictionary for each player name.

    Parameters:
      player_data(dict): Keys are player names, values are dicts of
                         data for several fields such as "shots".
    """
    
    for player_name in self.player_names:
      all_data = player_data[player_name]
      # The following is required since the structure isn't defined
      # yet for reading using vision. TODO This is very beta
      if ("NAME" not in all_data.keys()):
        all_data["NAME"] = player_name

      self.dict_to_write["PLAYER_DATA"].append(all_data)

  
  def write_all_data(self):
    """
    Write the entire game data to the game_data.json file using
    the dict_to_write field that has been set throughout
    """
    curr_dir = os.getcwd()
    # get the path up until repo parent
    pro_clubs_index = curr_dir.find("pro-clubs")
    path_to_pro_clubs_root = curr_dir[:pro_clubs_index]
    full_path = path_to_pro_clubs_root + "pro-clubs/src/data/game_data.json"
    
    curr_data = read_json(full_path)  # read game data before

    curr_data.append(self.dict_to_write)  # append this game's data

    write_json(curr_data, full_path)  # write back to original file