import sqlite3
from time import time

def update_player_table(player,username="",password=""):
  connection = sqlite3.connect("./Data/player_data.db")
  cursor = connection.cursor()
  unlocked_powers = [x.id for x in player.unlocked_powers]
  active_powers = [x.id for x in player.unlocked_powers]
  weapons = [x.id for x in player.weapons]
  try:
    sqlInsertCommand = f"""INSERT INTO PLAYERS VALUES (
      "{player.id}","{username}","{password}","{player.name}","{player.gold}",
      "{player.gold_lv}","{player.elixir}","{player.elixir_lv}",
      "{player.d_elixir}","{player.d_elixir_lv}","{player.barb.level}",
      "{player.barb.weapons["sword"].id}","{player.barb.weapons["shield"].id}",
      "{unlocked_powers}","{active_powers}","{player.power_limit}","{weapons}",
      "{player.stamina}","{time()}"
    );"""
    cursor.execute(sqlInsertCommand)
  except:
    sqlInsertCommand = f"""UPDATE PLAYERS SET
      th_level = "{player.th}",
      gold = "{player.gold}",
      name = "{player.name}",
      gold_storage_lv = "{player.gold_lv}",
      elixir = "{player.elixir}",
      elixir_storage_lv = "{player.elixir_lv}",
      d_elixir = "{player.d_elixir}",
      d_elixir_storage_lv = "{player.d_elixir_lv}",
      barb_lv = "{player.barb.level}",
      barb_sword = "{player.barb.weapons["sword"].id}",
      barb_shield = "{player.barb.weapons["shield"].id}",
      unlocked_powers = "{unlocked_powers}",
      active_powers = "{active_powers}",
      power_limit = "{player.power_limit}",
      weapons = "{weapons}",
      stamina = "{player.stamina}",
      last_login = "{time()}",
      WHERE id = {player.id}
    ;"""
    cursor.execute(sqlInsertCommand)
  connection.commit()

def load_player_data(username,password):
  connection = sqlite3.connect("./Data/player_data.db")
  cursor = connection.cursor()
  sqlCommand = f"""SELECT * FROM PLAYERS WHERE username = {username} AND password = "{password}";"""
  cursor.execute(sqlCommand)
  connection.commit()
  return cursor.fetchall()[0]
