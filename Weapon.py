import sqlite3
import os

def get_stats(weapon):
  if os.path.exists("./Data/weapons.db"):
    connection = sqlite3.connect("./Data/weapons.db")
  else:
    return
  sqlCommand = f"""SELECT * FROM WEAPONS WHERE internal_name = "{weapon}";"""
  cursor = connection.cursor()
  cursor.execute(sqlCommand)
  return cursor.fetchall()[0][1:]

class Weapon():
  internal_name = ""
  display_name = ""
  type = ""
  description = ""

  def __init__(self,weapon):
    details = get_stats(weapon)
    if type(details) != tuple:
      raise TypeError
    
    self.id = details[0]
    self.internal_name = details[1]
    self.display_name = details[2]
    self.type = details[3]
    self.stats = {}
    self.level = 1
    stats = details[4].split(":")
    for i in range(0,len(stats),3):
      self.stats.update({stats[i]: f"{stats[i+1]}:{stats[i+2]}"})
    self.description = details[5]

  def __str__(self):
    return self.display_name
    