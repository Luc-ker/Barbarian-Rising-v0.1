import sqlite3
import os

def get_power_info(weapon):
  if os.path.exists("./Data/weapons.db"):
    connection = sqlite3.connect("./Data/weapons.db")
  else:
    return
  sqlCommand = f"""SELECT * FROM WEAPONS WHERE internal_name = "{weapon}";"""
  cursor = connection.cursor()
  cursor.execute(sqlCommand)
  return cursor.fetchall()[0]

class Power():
  def __init__(self,power,level=1):
    power = power.upper().replace(" ","")
    info = get_power_info(power)
    if type(info) != tuple:
      raise TypeError
  
    self.internal_name = info[0]
    self.display_name = info[1]
    self.initial_cooldown = info[2]
    self.cooldown = self.initial_cooldown
    self.type = info[3]
    self.element = info[4]
    self.target = info[5]
    self.description = info[6]
    self.stats = {}
    self.level = level

  def __str__(self):
    return self.display_name

