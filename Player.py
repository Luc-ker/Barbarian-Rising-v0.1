from Power import Power
from Troop import Troop


class Player():
  name = ""
  id = ""

  def __init__(self, name):
    self.name = name
    self.id = ""
    self.gold = 500
    self.elixir = 500
    self.d_elixir = 0
    self.barbarian = Troop("barbarian")
    self.powers = []

  def addPower(self, power):
    if type(power) != Power:
      raise TypeError("Not a valid power.")
    elif power.name in [power.name for power in self.powers]:
      print("You have already obtained that power.")
    else:
      self.powers.append(power)
