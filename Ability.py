import sqlite3
import os

def get_stats(ability):
  if os.path.exists("./Data/abilities.db"):
    connection = sqlite3.connect("./Data/abilities.db")
  else:
    return
  sqlCommand = f"""SELECT * FROM ABILITIES WHERE internal_name = "{ability}";"""
  cursor = connection.cursor()
  cursor.execute(sqlCommand)
  return cursor.fetchall()[0]

class Ability():
  internal_name = ""
  display_name = ""
  description = ""

  def __init__(self,ability):
    details = get_stats(ability)
    
    self.internal_name = details[0]
    self.display_name = details[1]
    self.description = details[2]

  def __str__(self):
    return self.display_name
    