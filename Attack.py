import sqlite3
import os

def get_stats(attack):
  if os.path.exists("./Data/attacks.db"):
    connection = sqlite3.connect("./Data/attacks.db")
  else:
    return
  sqlCommand = f"""SELECT * FROM ATTACKS WHERE internal_name = "{attack}";"""
  cursor = connection.cursor()
  cursor.execute(sqlCommand)
  return cursor.fetchall()[0]

class Attack():
  internal_name = ""
  display_name = ""
  element = ""
  power = 0
  description = ""
  effectCode = ""
  properties = ""

  def __init__(self,attack):
    details = get_stats(attack)
    if type(details) != tuple:
      raise TypeError
    
    self.internal_name = details[0]
    self.display_name = details[1]
    self.element = details[2]
    self.power = details[3]
    self.target = details[4]
    self.effectCode = details[5]
    self.flags = details[6]
    self.shieldDamage = details[7]
    self.description = details[8]

  def __str__(self):
    return self.display_name
  
  def effect(self):
    pass
    