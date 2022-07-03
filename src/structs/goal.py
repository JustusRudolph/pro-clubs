class Goal:

  def __init__(self, minute, score, player_name=None,
               id=None, is_pen=False):
    """
    Parameters:
      minute(int): Minute in which the goal was scored
      player_name(str): Name of player who scored the goal
      score(tuple<2, int>): (home, away) score by scoring. For simplicity, goals for
                            are stored as home, goals against as away
      id(int): id of the goal for the game (eq. to index)
    """
    self.minute = minute
    self.score = score
    self.player_name = player_name
    self.is_pen = is_pen
    self.ID = id
    self.assist_ID = None

  def add_assist(self, assist_ID):
    self.assist_ID = assist_ID

  def get_dict_struct(self):
    full_dict = {}
    # following are metadata for both our and opposition goals
    full_dict["MINUTE"] = self.minute
    full_dict["SCORE"] = self.score
    full_dict["PENALTY"] = int(self.is_pen)

    if (self.player_name is not None):  # our goal data only
      full_dict["ID"] = self.ID
      full_dict["PLAYER_NAME"] = self.player_name
    
      if (self.assist_ID is None):
        full_dict["ASSIST_ID"] = "None"
      else:
        full_dict["ASSIST_ID"] = self.assist_ID

    return full_dict