class Assist:

  def __init__(self, ID, goal_ID, player_name):
    """
    Parameters:
      ID(int): unique ID for the assist in the game
      goal_ID(int): unique ID for the goal associated with
                    this assist
      player_name(str): The player who made the assist
    """
    self.ID = ID
    self.goal_ID = goal_ID
    self.player_name = player_name


  def get_dict_struct(self):
    full_dict = {}
    # All current metadata for assists:
    full_dict["ID"] = self.ID
    full_dict["GOAL_ID"] = self.goal_ID
    full_dict["PLAYER_NAME"] = self.player_name

    return full_dict