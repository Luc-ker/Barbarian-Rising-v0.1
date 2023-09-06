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

    self.int_name = troop
    self.name = info[1]
    self.level = level
    if info[2] != "":
      self.ability = Ability(info[2])
    self.attacks = make_attacks(info[3])
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
    elif self.weapons[weapon.type] != None:
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
    self.stats.update({
      "hp":stats[1],
      "attack":stats[2],
      "defence":stats[3],
      "speed":stats[4],
      "ability_level":stats[5]
    })
    for weapon in self.weapons.values():
      if weapon != None:
        for newStat in weapon.stats.items():
          operation,modifier,stat = newStat[1].split(":")[0],float(newStat[1].split(":")[1]),newStat[0]
          if operation == "mult":
            self.stats.update({stat: int(self.stats[stat]*modifier)})
          elif operation == "plus":
            self.stats.update({stat: int(self.stats[stat]+modifier)})
