import PySimpleGUI as sg

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
    self.n_games_played = 0
    self.curr_points = 0
    self.acc_names = ["Timbo", "Jutte", "DJ", "Basti", "Tommus"]  # accepted names

    self.curr_state = "Start"  # TODO create list of accepted states to move between
    self.curr_event = ""  # these change each loop
    self.curr_values = {}


  def create_window(self):
    """
    Updates/Creates a window from the current layout
    """
    self.window = sg.Window("Pro Clubs Tracker", self.layout)


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




  def show(self):
    """
    Show the GUI window
    """
    while (True):

      self.curr_event, self.curr_values = self.window.read()
      #print(self.curr_event, type(self.curr_event), self.curr_values)
      
      if ((self.curr_event == sg.WIN_CLOSED) or (self.curr_event == "Exit")):
        break
      
      # Now run different options dependent on the state
      if (self.curr_state == "Start"):
        failed = self.run_startup_options()

        if (failed):  # running through startup options failed
          break

      elif (self.curr_state == "Session"):
        failed = self.run_session_creation_options()

      else:  # some unaccounted for case
        print("Exiting.")
        break

    self.window.close()

  def run_startup_options(self):
    """
    Current window is startup: Run through all options
    """
    if (self.curr_event == "New Session"):
      new_layout = self.create_session_layout()
      self.layout = new_layout
      self.create_window()  # update the window
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
      self.curr_div = self.curr_values["-DIV-"]
      self.n_games_played = self.curr_values["-DIV_GAME_NO-"]
      self.curr_points = self.curr_values["-POINTS-"]

      print(f"Starting new session with players: {self.players}.")
      print(f"Starting in division {self.curr_div} with {self.curr_points} "
           +f"points in {self.n_games_played} games played.")

      return 0

    else:  # unexpected value/event
      return 1