class Player:

  def __init__(self, name):
    self.name = name
    self.n_goals = 0
    self.n_assists = 0
    self.goals = []
    self.assists = []

  
  def add_goal(self, goal):
    self.goals.append(goal)
    self.n_goals += 1