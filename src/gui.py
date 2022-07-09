import PySimpleGUI as sg

from structs import game
from static_data import static_game_data as sgd

class GUI:
  
  def __init__(self):
    self.layout = [
      [sg.Text("This is the Pro Clubs game tracker. "
              +"Press the button below to start a new session.")],
      [sg.Button("New Session")],
      [sg.Button("Exit")]
    ]
    self.players = []
    self.curr_div = 0
    self.n_games_played = 0  # number of games played in the division
    self.curr_points = 0
    self.curr_n_game = 1  # 1st game, "index" from 1
    self.game = 0  # empty for now
    self.acc_names = ["Timbo",
                      "Jutte",
                      "DJ",
                      "Basti",
                      "Tommus"]  # accepted names

    self.states = ["Start",
                   "Session",
                   "Pre-Game",
                   "PlayerChange",
                   "In-Game-unset",
                   "In-Game-set",
                   "Post-Game"]
    self.curr_state = self.states[0]
    self.curr_event = ""  # these change each loop
    self.curr_values = {}

    # Set the following three for in game screen
    self.game_set = False  # for any and home
    self.add_goal_for = False
    self.add_goal_against = False


  ############################
  ##### WINDOW FUNCTIONS #####
  ######################################################################
  ### These are related to obtaining windows from the current layout ###
  ######################################################################
  def create_window(self):
    """
    Creates a new window from the current layout
    """
    self.window = sg.Window("Pro Clubs Tracker", self.layout)

  def update_window(self):
    """
    Deletes the current window and creates a new window with the
    current layout
    """
    self.window.close()
    self.create_window()


  ############################
  ##### LAYOUT FUNCTIONS #####
  #########################################################
  ### These define the layouts for the different states ###
  #########################################################
  def create_session_layout(self):
    layout = [
      [sg.Text("Who is playing? Pressing the button is toggling player on/off. Default is off.")],
      [
        sg.Button(name) for name in self.acc_names  # generalise
      ],
      [sg.Text("Division: "), sg.Input(key="-DIV-")],
      [sg.Text("Number of Games played: "), sg.Input(key="-DIV_GAME_NO-")],
      [sg.Text("Current points: "), sg.Input(key="-POINTS-")],
      [sg.Button("Complete")],
      [sg.Button("Exit")]
    ]
    return layout


  def create_pre_game_layout(self):
    """
    Creates the GUI layout for pre-game screen where the user can start
    a new game.
    """
    curr_players_str = ""  # create nice print of players
    for i in range(len(self.players)):
      plr = self.players[i]
      if (i == (len(self.players)-1)):  # add full stop in the end
        curr_players_str += " and " + plr + "."
      elif (i==0):  # don't add comma before the first player
        curr_players_str += plr
      else:  # add comma and then the name of the next player
        curr_players_str += ", " + plr
    
    # create string for current status of session
    curr_status_str = f"In division {self.curr_div} with"
    curr_status_str += f" {self.curr_points} points from"
    curr_status_str += f" {self.n_games_played} games played."
    
    layout = [
      [sg.Text("Current players: " + curr_players_str)],
      [sg.Text("Current Status: " + curr_status_str)],
      [sg.Button("Start new game"), sg.Button("Change players")],
      [sg.Button("Exit")]
    ]
    return layout


  def create_player_change_layout(self):
    layout = [
      [sg.Text("Please tick who is playing in the game.")],
      [sg.Checkbox(name, key=name) for name in self.acc_names],
      [sg.Button("Done")],
      [sg.Button("Exit")]
    ]
    return layout

  def create_game_layout(self):
    layout = [  # baseline is just the title
      [sg.Text(f"Currently in Game {self.curr_n_game} of this session. "
               +"Add data below.")],
    ]
    if (self.game_set): # have created an any, show goal screen
      layout.append([sg.Text("ADD CURRENT SCORE/GAME DATA HERE MAYBE?")])

      # Only be able to add another goal if we are not currently adding one
      if not(self.add_goal_against or self.add_goal_for):
        layout.append([sg.Button("Add Goal For"), sg.Button("Add Goal Against")])
        layout.append([sg.Button("Finish Game")])
    else:
      layout.append([sg.Text("Who is any:")] + 
                    [sg.Combo(self.players + ["AI"], key="any")])  # either a player or AI
      layout.append([sg.Checkbox("Home:", key="home")])
      layout.append([sg.Button("Done")])  # signal to programme that the above two are set
    
    if (self.add_goal_for):
      layout.append([sg.Text("Minute: "), sg.Input(key="minute"),
                     sg.Text("Stoppage Time: "), sg.Input(key="stoppage")])
      layout.append([sg.Text("Scorer: "), sg.Combo(self.players + ["AI"], key="scorer")])
      layout.append([sg.Text("Assist: "), sg.Combo(self.players + ["AI"], key="assist")])
      layout.append([sg.Checkbox("Penalty: ", default=False, key="pen")])
      layout.append([sg.Checkbox("Own Goal: ", default=False, key="og")])
      layout.append([sg.Button("Done")])

    elif (self.add_goal_against):
      layout.append([sg.Text("Minute: "), sg.Input(key="minute"),
                     sg.Text("Stoppage Time: "), sg.Input(key="stoppage")])
      layout.append([sg.Checkbox("Penalty: ", default=False, key="pen")])
      layout.append([sg.Text("Own Goal"), sg.Combo(self.players + ["AI"], key="og")])
      layout.append([sg.Button("Done")])

    return layout

  def create_post_game_layout(self):
    layout = [
      [sg.Text("Game Completed - WONLOSTHERE")],
      [sg.Button("Add match facts")],
      [sg.Text("Add match data for: ")] +
      [sg.Button(name) for name in self.players],
      [sg.Button("Done")]
    ]

    return layout


  ###################################
  ##### OPTION/VISUAL FUNCTIONS #####
  ###############################################################
  ### These check the inputs from the gui in different states ###
  ###############################################################
  def run_startup_options(self):
    """
    Current window is startup: Run through all options
    """
    if (self.curr_event == "New Session"):
      new_layout = self.create_session_layout()
      self.layout = new_layout
      self.update_window()  # update the window
      self.curr_state = "Session"
      return 0  # as expected

    else:
      return 1  # something went wrong


  def run_session_creation_options(self):
    """
    One of many show functions which assumes that the current window
    is setting up the session.
    """
    if (self.curr_event in self.acc_names):  # a name button was pressed
      name = self.curr_event

      if (name in self.players):  # player already set -> unset
        print(f"Removing player: {name}.")
        self.players.remove(name)
      else:  # player not set, -> set them
        print(f"Adding player: {name}.")
        self.players.append(name)

      return 0

    elif (self.curr_event == "Complete"):  # division, game and points set
      self.curr_div = int(self.curr_values["-DIV-"])
      self.n_games_played = int(self.curr_values["-DIV_GAME_NO-"])
      self.curr_points = int(self.curr_values["-POINTS-"])

      new_layout = self.create_pre_game_layout()
      self.layout = new_layout
      self.update_window()  # update the window
      self.curr_state = "Pre-Game"

      print(f"Starting new session with players: {self.players}.")
      print(f"Starting in division {self.curr_div} with {self.curr_points} "
           +f"points in {self.n_games_played} games played.")

      return 0

    else:  # unexpected value/event
      return 1

  def run_pre_game_options(self):
    """
    Run through all options during pre-game
    """
    if (self.curr_event == "Start new game"):
      new_layout = self.create_game_layout()
      self.layout = new_layout
      self.update_window()  # update the window
      self.curr_state = "In-Game-unset"
      
      return 0

    elif (self.curr_event == "Change players"):
      new_layout = self.create_player_change_layout()
      self.layout = new_layout
      self.update_window()  # update the window
      self.curr_state = "PlayerChange"

      return 0

    else:
      return 1  # unexpected result

  def run_player_change_options(self):
    if (self.curr_event == "Done"):
      self.players = []  # reset
      for name in self.curr_values.keys():  # names: 0/1 are the curr_values
        if (self.curr_values[name]):  # if the box is ticked, player is present
          self.players.append(name)

      new_layout = self.create_pre_game_layout()
      self.layout = new_layout
      self.update_window()  # update the window
      self.curr_state = "Pre-Game"

      return 0

    else:
      return 1  # unexpected curr_event

  def run_in_game_options(self):
    """
    Run through all options for being in game. This includes more complexity
    than the other ones because it depends on whether a goal is requested to
    be set and if we have set the any and home fields.
    """
    
    if ((self.curr_event == "Done") and (not self.game_set)):  # any & home unset
      any_player = self.curr_values["any"]
      home = int(self.curr_values["home"])
      # create game instance to write to
      self.game = game.Game(self.curr_div, self.curr_n_game,
                            self.curr_points, self.players,
                            any=any_player, home=home)

      self.game_set = True
      # need to update the state after setting
      self.curr_state = "In-Game-set"
      new_layout = self.create_game_layout()

    elif (self.curr_event == "Add Goal For"):
      # go into adding goal for us screen
      self.add_goal_for = True
      new_layout = self.create_game_layout()

    elif (self.curr_event == "Add Goal Against"):
      # go into adding goal for opponent screen
      self.add_goal_against = True
      new_layout = self.create_game_layout()

    elif ((self.curr_event == "Done") and self.add_goal_for):
      self.add_goal_for = False  # unset after finishing
      minute = int(self.curr_values["minute"])
      # don't convert stoppage time to int yet, need to check if it exists
      try:
        stoppage_time = int(self.curr_values["stoppage"])
      except ValueError:
        stoppage_time = None  # if not an int, we reset to nonexistent
      
      scorer = self.curr_values["scorer"]
      assist = self.curr_values["assist"]
      pen = self.curr_values["pen"]
      og = self.curr_values["og"]

      self.game.add_goal_for(minute, player_name=scorer, assister=assist, pen=pen,
                             stoppage_time=stoppage_time, og=og)

      new_layout = self.create_game_layout()


    elif ((self.curr_event == "Done") and self.add_goal_against):
      self.add_goal_against = False  # unset after finishing
      minute = int(self.curr_values["minute"])
      # don't convert stoppage time to int yet, need to check if it exists
      try:
        stoppage_time = int(self.curr_values["stoppage"])
      except ValueError:
        stoppage_time = None  # if not an int, we reset to nonexistent
      pen = self.curr_values["pen"]
      og = self.curr_values["og"]  # this will hold a string now

      if (not og):  # if own goal assister is "", aka it's not an own goal
        self.game.add_goal_against(minute, stoppage_time=stoppage_time, pen=pen)
      else:  # there is an own goal assister, so definitely not a pen
        self.game.add_goal_against(minute, stoppage_time=stoppage_time, og=og)

      new_layout = self.create_game_layout()

    elif (self.curr_event == "Finish Game"):
      # Game is over, need to set several things now
      self.curr_state = "Post-Game"
      self.game.end_game()  # write to game_data.json with the game object
      self.end_game()  # update internal data for next game such as division
      # only time we create a post game window is in this case
      new_layout = self.create_post_game_layout()

    else:
      return 1

    # reset window in all cases except for failure (else return 1)
    self.layout = new_layout
    self.update_window()
    
    return 0


  def run_post_game_options(self):
    if (self.curr_event == "Add match facts"):
      #TODO TAKE SCREENSHOT HERE AND PASS TO GAME
      pass
      return 0
    
    elif (self.curr_event in self.players):
      # this means the event is a player name, i.e. add player data
      # TODO TAKE SCREENSHOT FOR PLAYERS HERE AND PASS TO GAME
      dummy_player_data = {self.curr_event: {}}
      self.game.add_player_data(dummy_player_data)
      
      return 0

    elif (self.curr_event == "Done"):  # end match
      self.game.write_all_data()
      self.curr_state = "Pre-Game"
      new_layout = self.create_pre_game_layout()  # go back to pregame
      self.layout = new_layout
      self.update_window()
    
      return 0

    else:
      return 1  # unexpected
      
  ###################################
  ##### DATA AMENDING FUNCTIONS #####
  ##########################################################################
  ### These functions do not affect the GUI but change values internally ###
  ##########################################################################
  def end_game(self):
    """
    Changes the current points and games played. If a division is changed
    subsequently then that is changed too.

    Accesses the won/lost field in the Game object, thus must be called
    after game.end_game()
    """
    # unset the game so the next game instance can overwrite the current one
    self.game_set = False

    game_res = self.game.dict_to_write["RESULT_TYPE"]
    
    if (game_res == "W"):
      self.curr_points += 3
    elif (game_res == "D"):
      self.curr_points += 1

    self.curr_n_game += 1  # number of games played in this session
    self.n_games_played += 1  # number of games played in current division

    # now get the number of points required for relegation/promo/title
    division_data = sgd.DIVISION_DATA[self.curr_div]
    title_points = division_data["TITLE"]
    promotion_points = division_data["PROMOTION"]
    relegation_points = division_data["RELEGATION"]

    if (self.curr_points >= title_points):
      self.curr_points = 0  # reset points
      self.n_games_played = 0
      if (self.curr_div != 1):
        self.curr_div -= 1  # move up the divisions

      return  # no need to keep checking

    if (self.n_games_played == 10):
      # if all 10 games are played in a division that's not 1, check outcome

      # promotion
      try:  # will get type error in comparing int with None for div 1 promo
        if (self.curr_points >= promotion_points):
          self.n_games_played = 0
          self.curr_points = 0
          self.curr_div -= 1
          return  # no need to keep checking

      except TypeError:  # we're in div 1 so just reset points and games played
        self.n_games_played = 0
        self.curr_points = 0
        return  # no need to keep checking

      # relegation
      try:  # will get type error in comparing int with None for div 10 releg
        if (self.curr_points < relegation_points):
          self.n_games_played = 0
          self.curr_points = 0
          self.curr_div += 1
          return  # no need to keep checking

      except TypeError:  # we're in div 10, so can't relegate
        self.n_games_played = 0
        self.curr_points = 0
        return  # no need to keep checking

      # Neither relegation nor promotion -> Keep division
      self.n_games_played = 0
      self.curr_points = 0

    # Check for relegation before the 10th game is played

    # NOTE: THERE IS NO TITLE CHECK BEFORE 10 GAMES BECAUSE ALL PROMO POINTS ARE
    # WITHIN 3 POINTS OF TITLE, SO CAN BE DONE IN ONE GAME
    games_remaining = 10 - self.n_games_played
    try:
      points_needed_to_stay_in_div = relegation_points - self.curr_points
      if (points_needed_to_stay_in_div > games_remaining*3):
        # more points needed to stay in div than can still be obtained -> relegate
        self.curr_points = 0
        self.curr_div += 1
        self.n_games_played = 0
        return  # no need to keep checking

    except TypeError:  # subtracting from None: Can't get relegated from div 10
      pass

    # Check if promotion is out of range
    try:
      points_needed_to_promote = promotion_points - self.curr_points
      if (points_needed_to_promote > games_remaining*3):
        # more points needed to promote than can still be obtained -> keep div
        self.curr_points = 0
        self.n_games_played = 0
        return  # no need to keep checking

    except TypeError:  # subtracting from None: Can't get promoted from div 1
      pass


  #########################
  ##### SHOW FUNCTION #####
  #########################
  def show(self):
    """
    Show the GUI window in the current state. Dependent on the state check
    """
    while (True):

      self.curr_event, self.curr_values = self.window.read()
      print(self.curr_event, type(self.curr_event), self.curr_values)
      
      if ((self.curr_event == sg.WIN_CLOSED) or (self.curr_event == "Exit")):
        break
      
      # Now run different options dependent on the state
      if (self.curr_state == "Start"):
        failed = self.run_startup_options()

      elif (self.curr_state == "Session"):
        failed = self.run_session_creation_options()

      elif (self.curr_state == "Pre-Game"):
        failed = self.run_pre_game_options()

      elif (self.curr_state == "PlayerChange"):
        failed = self.run_player_change_options()

      elif ((self.curr_state == "In-Game-unset") or
            (self.curr_state == "In-Game-set")):
        failed = self.run_in_game_options()

      elif (self.curr_state == "Post-Game"):
        failed = self.run_post_game_options()

      else:  # some unaccounted for case
        print("Exiting.")
        break

      if (failed):  # running through startup options failed
        break

    self.window.close()