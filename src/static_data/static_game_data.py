DIVISION_DATA = {
  10:{
    "RELEGATION": None,
    "PROMOTION": 9,
    "TITLE": 12
  },
  9:{
    "RELEGATION": 6,
    "PROMOTION": 10,
    "TITLE": 13
  },
  8:{
    "RELEGATION": 8,
    "PROMOTION": 12,
    "TITLE": 15
  },
  7:{
    "RELEGATION": 8,
    "PROMOTION": 14,
    "TITLE": 17
  },
  6:{
    "RELEGATION": 10,
    "PROMOTION": 16,
    "TITLE": 18
  },
  5:{
    "RELEGATION": 10,
    "PROMOTION": 16,
    "TITLE": 19
  },
  4:{
    "RELEGATION": 10,
    "PROMOTION": 16,
    "TITLE": 19
  },
  3:{
    "RELEGATION": 12,
    "PROMOTION": 18,
    "TITLE": 21
  },
  2:{
    "RELEGATION": 12,
    "PROMOTION": 18,
    "TITLE": 21
  },
  1:{
    "RELEGATION": 14,
    "PROMOTION": None,
    "TITLE": 23
  },
}


def is_valid_division(div):
  return (div >= 1) and (div <= 10)

def is_valid_n_games(n_games):
  # before a game, can't have already played 10 games
  return (n_games >= 0) and (n_games <= 9)