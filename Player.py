from Power import Power
from Troop import Troop


class Player():
  name = ""
  id = ""

  def __init__(self, name):
    self.name = name
    self.id = ""
    self.max_gold = 3000
    self.max_elixir = 3000
    self.max_d_elixir = 0
    self.gold = 500
    self.elixir = 500
    self.d_elixir = 0
    self.barbarian = Troop("barbarian")
    self.unlocked_powers = []
    self.active_powers = []
    self.power_limit = 3
    self.unlocked_moves = []
    self.active_moves = []
    self.move_limit = 2
    self.stamina = 240

  def addPower(self, power):
    if type(power) != Power:
      raise TypeError("Not a valid power.")
    elif power.name in [x.name for x in self.unlocked_powers]:
      print("You have already obtained that power.")
    else:
      self.unlocked_powers.append(power)

  def equipPower(self, power):
    if type(power) != Power:
      raise TypeError("Not a valid power.")
    elif power.name in [x.name for x in self.active_powers]:
      print("You have already equipped that power.")
    else:
      self.active_powers.append(power)
      self.unlocked_powers.remove(power)

  def unequipPower(self, power):
    if type(power) != Power:
      raise TypeError("Not a valid power.")
    else:
      self.active_powers.remove(power)

