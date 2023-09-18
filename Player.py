from Power import Power
from Troop import Troop
from Attack import Attack
from Weapon import Weapon

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
    self.gold_full = (self.gold == self.max_gold)
    self.elixir_full = (self.elixir == self.max_elixir)
    self.d_elixir_full = (self.d_elixir == self.max_d_elixir)
    self.barbarian = Troop("barbarian",5,"Player")
    self.unlocked_powers = []
    self.active_powers = []
    self.power_limit = 3
    self.stamina = 240
    self.weapons = []

  def unlockPower(self, power):
    if type(power) != Power:
      power = Power(power)
    if power.internal_name in [x.internal_name for x in self.unlocked_powers]:
      print("You have already obtained that power.")
      return
    else:
      self.unlocked_powers.append(power)
      print(f"You unlocked the power of the {power.display_name}!")

  def equipPower(self, power):
    if type(power) != Power:
      power = Power(power)
    if power.internal_name in [x.internal_name for x in self.active_powers]:
      print("You have already equipped that power.")
    else:
      for i,x in enumerate(self.unlocked_powers):
        if power.internal_name == x.internal_name:
          self.active_powers.append(x)
          self.unlocked_powers.remove(x)
          return
      print("Power not unlocked.")
  
  def unequipPower(self, power):
    if type(power) != Power:
      raise TypeError("Not a valid power.")
    else:
      self.active_powers.remove(power)

  def obtainWeapon(self, weapon):
    if type(weapon) != Weapon:
      weapon = Weapon(weapon)
    self.weapons.append(weapon)

  def addGold(self,amount):
    available = self.max_gold - self.gold
    if self.gold_full:
      print("Gold could not be collected because storages are full.")
    elif amount > available:
      self.gold += available
    else:
      self.gold += amount

  def addElixir(self,amount):
    available = self.max_elixir - self.elixir
    if self.elixir_full:
      print("Elixir could not be collected because storages are full.")
    elif amount > available:
      self.elixir += available
    else:
      self.elixir += amount

  def addDElixir(self,amount):
    available = self.max_d_elixir - self.d_elixir
    if self.d_elixir_full:
      print("Dark Elixir could not be collected because storages are full.")
    elif amount > available:
      self.d_elixir += available
    else:
      self.d_elixir += amount


