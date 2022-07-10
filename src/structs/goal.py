class Goal:

  def __init__(self, minute, score, stoppage_time=None, player_name=None,
               id=None, is_pen=False, og=None):
    """
    Parameters:
      minute(int): Minute in which the goal was scored
      score(tuple<2, int>): (home, away) score by scoring. For simplicity, goals for
                            are stored as home, goals against as away
      stoppage_time(int): the minute in stoppage time.
                          Only not None when minute is 45 or 90
      player_name(str): Name of player who scored the goal
      id(int): id of the goal for the game (eq. to index)
      is_pen(bool): If the goal is a penalty
      og(bool or str): If the goal is an own goal. If this is a goal against,
                       this will be a string holding the name of the player
    """
    self.minute = minute
    self.stoppage_time = stoppage_time
    self.score = score
    self.player_name = player_name
    self.is_pen = is_pen
    self.ID = id
    self.assist_ID = None

    if (og is not None):
      try:  # check if it is a boolean or already an int
        self.og = int(og)
      except ValueError:  # if string it isn't converted
        self.og = og

    else:
      self.og = None

  
  def __str__(self):
    """
    Writes the current goal into a string printable format
    """
    final_str = str(self.minute)
    if (self.stoppage_time is not None):
      final_str += "+" + str(self.stoppage_time) + "'"
    else:
      final_str += "'  "  # add two extra spaces to align

    final_str += f"  {self.score[0]}-{self.score[1]}"

    if (self.player_name is not None):
      final_str += "  " + self.player_name

    if (self.og == 1):  # it's an opponent's own goal
      final_str += "  OG"

    elif (isinstance(self.og, str)):  # og is string, so it's ours
      final_str += "  " + self.og + " (OG)"

    elif (self.is_pen):  # can't have penalty and own goal together
      final_str += " (P)"

    return final_str



  def add_assist(self, assist_ID):
    self.assist_ID = assist_ID

  def get_dict_struct(self):
    full_dict = {}
    # following are metadata for both our and opposition goals
    full_dict["MINUTE"] = self.minute

    if (self.stoppage_time is not None):
      full_dict["STOPPAGE_TIME"] = self.stoppage_time

    full_dict["SCORE"] = self.score
    full_dict["PENALTY"] = int(self.is_pen)
    
    if (self.og is not None):  # only write own goal if it has a value
      full_dict["OG"] = self.og

    if (self.player_name is not None):  # our goal data only
      full_dict["ID"] = self.ID
      # in case of an OG, there is no scorer and it's just ""
      if (self.player_name):
        full_dict["PLAYER_NAME"] = self.player_name
    
      if (self.assist_ID is None):
        full_dict["ASSIST_ID"] = "None"
      else:
        full_dict["ASSIST_ID"] = self.assist_ID

    return full_dict