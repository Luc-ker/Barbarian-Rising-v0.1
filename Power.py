import sqlite3
import os

def get_stats(power,level):
  if os.path.exists("./Data/power_stats.db"):
    connection = sqlite3.connect("./Data/power_stats.db")
  else:
    return
  sqlCommand = f"""SELECT * FROM {power};"""
  cursor = connection.cursor()
  cursor.execute(sqlCommand)
  return cursor.fetchall()[level-1]

def get_power_info(power):
  if os.path.exists("./Data/power_info.db"):
    connection = sqlite3.connect("./Data/power_info.db")
  else:
    return
  sqlCommand = f"""SELECT * FROM POWERS WHERE internal_name = "{power}";"""
  cursor = connection.cursor()
  cursor.execute(sqlCommand)
  return cursor.fetchall()[0]

class Power():
  def __init__(self,power,level=1):
    power = power.upper().replace(" ","")
    info = get_power_info(power)
    dbstats = get_stats(power,level)
    if type(info) != tuple:
      raise TypeError
  
    self.internal_name = info[0]
    self.display_name = info[1]
    self.initial_cooldown = info[2]
    self.cooldown = self.initial_cooldown
    self.type = info[3]
    self.element = info[4]
    self.shieldDamage = info[5]
    self.target = info[6]
    self.description = info[7]
    self.power = dbstats[1]
    self.level = level

  def __str__(self):
    return self.display_name

