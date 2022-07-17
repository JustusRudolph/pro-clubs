def check_if_int(inp):
  """
  This function checks if the input can be cast to an integer
  """
  try:
    out = int(inp)
    return True
  except ValueError:
    return False

def is_valid_division(div):
  return (div >= 1) and (div <= 10)

def is_valid_n_games(n_games):
  # before a game, can't have already played 10 games
  return (n_games >= 0) and (n_games <= 9)

def is_valid_points(n_points, n_games):
  """
  From a certain number of games, check if a given
  number of points is possible.
  """
  if (n_points < 0):  # first check out of bounds below
    return False

  # e.g. for below:
  # 8 points gives 2 max wins, 2 min draws
  # 13 points gives 4 max wins, 1 draw
  # Minimum number of games to get that is by just winning and drawing
  # to get to the remainder not divisible by three
  n_min_draws = n_points % 3
  n_max_wins = n_points // 3

  n_min_games_played = n_max_wins + n_min_draws
  print(f"Min games: {n_min_games_played}. Games played: {n_games}")

  # must have played at least n_min_games_played
  return n_min_games_played <= n_games


def check_session_setup(div, n_games, n_points):
  """
  Checks if all the values received during session setup
  are valid so we can call less in the gui.
  
  Parameters:
    div(str/int): Current division
    n_games(str/int): Number of games played in the division
    n_points(str/int): Number of points in the the division

  Returns:
    is_valid(tuple): First value is just the boolean. second is a list
                     of invalid values as strings. "div", "n_games",
                     "n_points" are the options.
  
  """
  invalid_inputs = []  # all fields that are invalid
  div_valid = check_if_int(div)
  if (div_valid):  # only check validity of number if it's a number
    div_valid &= is_valid_division(int(div))  # can cast

  if (not div_valid):
    invalid_inputs.append("div")
  
  n_games_valid = check_if_int(n_games)
  if (n_games_valid):  # only check validity of number if it's a number
    n_games_valid &= is_valid_n_games(int(n_games))
  
  if (not n_games_valid):
    invalid_inputs.append("n_games")
  
  n_points_valid = check_if_int(n_points)
  if (n_points_valid):  # only check validity of number if it's a number
    n_points_valid &= is_valid_points(int(n_points), int(n_games))

  if (not n_points_valid):
    invalid_inputs.append("n_points")

  all_valid = div_valid and n_games_valid and n_points_valid

  return all_valid, invalid_inputs


def is_valid_minute(minute):
  return (minute >= 1) and (minute <= 90)

def is_valid_stoppage(stoppage):
  return (stoppage >= 1) and (stoppage <= 10)
