import sqlite3
import os
from Weapon import Weapon
from Ability import Ability
from Attack import Attack

def get_base_stats(troop,level):
  if os.path.exists("./Data/troop_stats.db"):
    connection = sqlite3.connect("./Data/troop_stats.db")
  else:
    return
  sqlCommand = f"""SELECT * FROM {troop};"""
  cursor = connection.cursor()
  cursor.execute(sqlCommand)
  return cursor.fetchall()[level-1]

def get_troop_info(troop):
  if os.path.exists("./Data/troop_info.db"):
    connection = sqlite3.connect("./Data/troop_info.db")
  else:
    raise FileNotFoundError("/Data/troop_info.db was not found.")
  sqlCommand = f"""SELECT * FROM TROOPS WHERE internal_name = "{troop}";"""
  cursor = connection.cursor()
  cursor.execute(sqlCommand)
  return cursor.fetchall()[0]

def make_attacks(str):
  return [Attack(x) for x in str[1:-1].split(":")]
  
class Troop():
  int_name = None
  name = None
  level = 0
  ability = None
  attacks = []
  
  def __init__(self,troop,level=1,ownedBy=None):
    troop = troop.upper().replace(" ","")
    dbstats = get_base_stats(troop,level)
    info = get_troop_info(troop)
    if type(dbstats) != tuple:
      raise TypeError

    self.int_name = troop
    self.name = info[1]
    self.level = level
    if info[2] != "":
      self.ability = Ability(info[2])

    self.attacks = make_attacks(info[3])
    self.unlocked_attacks = []
    self.max_attacks = 2

    self.stats = {
      "hp":dbstats[1],
      "attack":dbstats[2],
      "defence":dbstats[3],
      "speed":dbstats[4],
      "ability_level":dbstats[5],
      "crit_rate": 5,
      "damage_mult": 1,
      "damage_reduction": 0
    }
    self.weapons = {
      "sword": None,
      "shield": None
    }
    self.owner = ownedBy
    self.description = info[8]

  def equip(self,weapon):
    if type(weapon) != Weapon:
      print("This weapon is not valid.")
      return
    elif self.weapons[weapon.type] is not None:
      choice = input(f"{self.weapons[weapon.type].display_name} is already equipped. Equip the new weapon? (y/n)")
      while choice != "y" and choice != "n":
        print("Invalid input.")
        choice = input(f"{self.weapons[weapon.type].display_name} is already equipped. Equip the new weapon? (y/n)")
      if choice.lower() == "n":
        return
    self.weapons.update({weapon.type: weapon})
    self.calc_stats()

  def calc_stats(self):
    stats = get_base_stats(self.int_name,self.level)
    if type(stats) != tuple:
      raise TypeError
    self.stats.update({
      "hp":stats[1],
      "attack":stats[2],
      "defence":stats[3],
      "speed":stats[4],
      "ability_level":stats[5],
      "crit_rate": 5,
      "damage_mult": 1,
      "damage_reduction": 0
    })
    for weapon in self.weapons.values():
      if weapon is not None:
        for newStat in weapon.stats.items():
          operation,modifier,stat = newStat[1].split(":")[0],float(newStat[1].split(":")[1]),newStat[0]
          if operation == "mult":
            self.stats.update({stat: int(self.stats[stat]*modifier)})
          elif operation == "plus":
            self.stats.update({stat: int(self.stats[stat]+modifier)})

  def level_up(self,levels=1):
    self.level += levels
    if levels == 1:
      print(f"{self.name} gained {levels} level!")
    else:
      print(f"{self.name} gained {levels} levels!")
    self.calc_stats()

  def unlockAttack(self, attack):
    if type(attack) != Attack:
      attack = Attack(attack)
    if attack.internal_name in [x.internal_name for x in self.unlocked_attacks]:
      print("Attack already unlocked.")
    else:
      self.unlocked_attacks.append(attack)
      print(f"{self.name} can now use {attack.display_name}!")

  def learnAttack(self,attack):
    if type(attack) != Attack:
      attack = Attack(attack)
    if attack.internal_name not in [x.internal_name for x in self.unlocked_attacks]:
      print(f"{self.name} can't learn {attack.display_name}.")
      return
    if len(self.attacks) >= self.max_attacks:
      choice = "0"
      while len(choice) < 1 or not choice.isdigit() or int(choice) < 1 or int(choice) > len(self.attacks) + 1:
        self.show_attacks()
        print(f"{len(self.attacks) + 1}: Return")
        choice = input("Select an attack to replace.")
        if len(choice) < 1:
          pass
        elif int(choice) == len(self.attacks) + 1:
          return
      else:
        replaced = self.attacks[int(choice)-1]
        self.attacks[int(choice)-1] = attack
        print(f"{replaced.display_name} was forgotten for {attack.display_name}!")
    else:
      self.attacks.append(attack)
      print(f"Barbarian learnt {attack.display_name}!")

  def forgetAttack(self, attack):
    if type(attack) != Attack:
      raise TypeError("Not a valid attack.")
    else:
      self.attacks.remove(attack)

  def show_attacks(self):
    for i,x in enumerate(self.attacks):
      print(f"{i+1}: {x.display_name}")