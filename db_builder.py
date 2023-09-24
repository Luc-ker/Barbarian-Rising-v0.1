import sqlite3
import os
from time import time

def add_update():
  if os.path.exists("./Data/times.db"):
    os.remove("./Data/times.db")
  connection = sqlite3.connect("./Data/times.db")
  sqlCreateCommand = """CREATE TABLE IF NOT EXISTS TIMES(
    file varchar(255),
    last_modified float,
    PRIMARY KEY(file)
  );"""
  cursor = connection.cursor()
  cursor.execute(sqlCreateCommand)
  for file in os.listdir("./Stats/"):
    file = f"./Stats/{file}"
    sqlInsertCommand = f"""INSERT INTO TIMES VALUES ("{file}",{os.path.getmtime(file)});"""
    cursor.execute(sqlInsertCommand)
    connection.commit()

def should_update():
  sqlCommand = """SELECT * FROM times;"""
  connection = sqlite3.connect("./Data/times.db")
  cursor = connection.cursor()
  cursor.execute(sqlCommand)
  result = cursor.fetchall()
  for file in os.listdir("./Stats/"):
    file = f"./Stats/{file}"
    last_modified = os.path.getmtime(file)
    for i,x in result:
      if i == file and x != last_modified:
        return True
  return False

def update_troop_stats():
  with open("./Stats/troop_stats.txt", "r") as f1:
    if os.path.exists("./Data/troop_stats.db"):
      os.remove("./Data/troop_stats.db")
    connection = sqlite3.connect("./Data/troop_stats.db")
    troop = None
    cursor = connection.cursor()
    for line in f1:
      if line[0] == "#" or line == "\n":
        pass
      elif line[0] == "[":
        connection.commit()
        troop = line[1:-2]
#        print(f"Creating table for {troop}'s stats...")
        sqlCreateCommand = f"""CREATE TABLE IF NOT EXISTS {troop}(
          level int,
          hp int,
          attack int,
          defense int,
          speed int,
          ability_level int,
          PRIMARY KEY(level)
        );"""
        cursor = connection.cursor()
        cursor.execute(sqlCreateCommand)
      else:
        battler = line[:-1].split(",")
        sqlInsertCommand = f"""INSERT INTO {troop} VALUES ("{battler[0]}","{battler[1]}","{battler[2]}","{battler[3]}","{battler[4]}","{battler[5]}");"""
        cursor.execute(sqlInsertCommand)
        connection.commit()
  print("Troop stats databases updated.")

def update_attacks():
  with open("./Stats/attacks.txt", "r") as f1:
    if os.path.exists("./Data/attacks.db"):
      os.remove("./Data/attacks.db")
    sqlCreateCommand = """CREATE TABLE IF NOT EXISTS ATTACKS(
      internal_name varchar(255),
      display_name varchar(255),
      element varchar(255),
      power int,
      target varchar(255),
      effect_code varchar(255),
      effect_chance int,
      effect_turns int,
      flags varchar(100),
      shield_damage int,
      description varchar(510),
      PRIMARY KEY(internal_name)
    );"""
    connection = sqlite3.connect("./Data/attacks.db")
    cursor = connection.cursor()
    cursor.execute(sqlCreateCommand)
    for line in f1:
      if line[0] == "#" or line == "\n":
        pass
      else:
        attack = line[:-1].split(",")
#        print(f"Creating row for {attack[0]}...")
        desc = ",".join(attack[10:-1] + [attack[-1]])
        sqlInsertCommand = f"""INSERT INTO ATTACKS VALUES ("{attack[0]}","{attack[1]}","{attack[2]}","{attack[3]}","{attack[4]}","{attack[5]}","{attack[6]}","{attack[7]}","{attack[8]}","{attack[9]}","{desc}");"""
        cursor.execute(sqlInsertCommand)
        connection.commit()
  print("Attack database updated.")

def update_weapons():
  with open("./Stats/weapons.txt", "r") as f1:
    if os.path.exists("./Data/weapons.db"):
      os.remove("./Data/weapons.db")
    sqlCreateCommand = """CREATE TABLE IF NOT EXISTS WEAPONS(
      id int,
      internal_name varchar(255),
      display_name varchar(255),
      weapon_type varchar(255),
      stats varchar(255),
      description varchar(510),
      PRIMARY KEY(internal_name)
    );"""
    connection = sqlite3.connect("./Data/weapons.db")
    cursor = connection.cursor()
    cursor.execute(sqlCreateCommand)
    for line in f1:
      if line[0] == "#" or line == "\n":
        pass
      else:
        weapon = line[:-1].split(",")
#        print(f"Creating row for {weapon[0]}...")
        desc = ",".join(weapon[5:-1] + [weapon[-1]])
        sqlInsertCommand = f"""INSERT INTO WEAPONS VALUES ("{weapon[0]}","{weapon[1]}","{weapon[2]}","{weapon[3]}","{weapon[4]}","{desc}");"""
        cursor.execute(sqlInsertCommand)
        connection.commit()
  print("Weapon database updated.")

def update_troop_info():
  with open("./Stats/troop_info.txt", "r") as f1:
    if os.path.exists("./Data/troop_info.db"):
      os.remove("./Data/troop_info.db")
    sqlCreateCommand = """CREATE TABLE IF NOT EXISTS TROOPS(
      internal_name varchar(255),
      display_name varchar(255),
      ability varchar(255),
      attacks varchar(255),
      weaknesses varchar(255),
      resistances varchar(255),
      shield int,
      flying varchar(255),
      description varchar(510),
      PRIMARY KEY(internal_name)
      );"""
    connection = sqlite3.connect("./Data/troop_info.db")
    cursor = connection.cursor()
    cursor.execute(sqlCreateCommand)
    for line in f1:
      if line[0] == "#" or line == "\n":
        pass
      else:
        info = line[:-1].split(",")
#        print(f"Creating row for {info[0]}...")
        desc = ",".join(info[8:-1] + [info[-1]])
        sqlInsertCommand = f"""INSERT INTO TROOPS VALUES ("{info[0]}","{info[1]}","{info[2]}","{info[3]}","{info[4]}","{info[5]}","{info[6]}","{info[7]}","{desc}");"""
        cursor.execute(sqlInsertCommand)
        connection.commit()
  print("Troop info database updated.")

def update_abilities():
  with open("./Stats/ability_info.txt", "r") as f1:
    if os.path.exists("./Data/ability_info.db"):
      os.remove("./Data/ability_info.db")
    sqlCreateCommand = """CREATE TABLE IF NOT EXISTS ABILITIES(
      internal_name varchar(255),
      display_name varchar(255),
      description varchar(510),
      PRIMARY KEY(internal_name)
    );"""
    connection = sqlite3.connect("./Data/ability_info.db")
    cursor = connection.cursor()
    cursor.execute(sqlCreateCommand)
    for line in f1:
      if line[0] == "#" or line == "\n":
        pass
      else:
        ability = line[:-1].split(",")
#        print(f"Creating row for {ability[0]}...")
        desc = ",".join(ability[2:-1] + [ability[-1]])
        sqlInsertCommand = f"""INSERT INTO ABILITIES VALUES ("{ability[0]}","{ability[1]}","{desc}");"""
        cursor.execute(sqlInsertCommand)
        connection.commit()
  print("Ability info database updated.")

def update_power_info():
  with open("./Stats/power_info.txt", "r") as f1:
    if os.path.exists("./Data/power_info.db"):
      os.remove("./Data/power_info.db")
    sqlCreateCommand = """CREATE TABLE IF NOT EXISTS POWERS(
      id int,
      internal_name varchar(255),
      display_name varchar(255),
      cooldown int,
      type varchar(255),
      element varchar(255),
      shield_damage int,
      target varchar(255),
      description varchar(510),
      PRIMARY KEY(internal_name)
    );"""
    connection = sqlite3.connect("./Data/power_info.db")
    cursor = connection.cursor()
    cursor.execute(sqlCreateCommand)
    for line in f1:
      if line[0] == "#" or line == "\n":
        pass
      else:
        power = line[:-1].split(",")
#        print(f"Creating row for {power[0]}...")
        desc = ",".join(power[8:-1] + [power[-1]])
        sqlInsertCommand = f"""INSERT INTO POWERS VALUES ("{power[0]}","{power[1]}","{power[2]}","{power[3]}","{power[4]}","{power[5]}","{power[6]}","{power[7]}","{desc}");"""
        cursor.execute(sqlInsertCommand)
        connection.commit()
  print("Power info database updated.")
  
def update_power_stats():
  with open("./Stats/power_stats.txt", "r") as f1:
    if os.path.exists("./Data/power_stats.db"):
      os.remove("./Data/power_stats.db")
    connection = sqlite3.connect("./Data/power_stats.db")
    power = None
    cursor = connection.cursor()
    for line in f1:
      if line[0] == "#" or line == "\n":
        pass
      elif line[0] == "[":
        connection.commit()
        power = line[1:-2]
#        print(f"Creating table for {power}'s stats...")
        sqlCreateCommand = f"""CREATE TABLE IF NOT EXISTS {power}(
          level int,
          power int,
          TH_needed int,
          PRIMARY KEY(level)
        );"""
        cursor = connection.cursor()
        cursor.execute(sqlCreateCommand)
      else:
        stats = line[:-1].split(",")
        sqlInsertCommand = f"""INSERT INTO {power} VALUES ("{stats[0]}","{stats[1]}","{stats[2]}");"""
        cursor.execute(sqlInsertCommand)
        connection.commit()
  print("Power stats database updated.")

def create_player_table():
  connection = sqlite3.connect("./Data/player_data.db")
  cursor = connection.cursor()
  sqlCreateCommand = f"""CREATE TABLE IF NOT EXISTS PLAYERS(
    id int,
    username varchar(255),
    password varchar(255),
    th_level int,
    gold int,
    gold_storage_lv int,
    elixir int,
    elixir_storage_lv int,
    d_elixir int,
    d_elixir_storage_lv int,
    barb_lv int,
    barb_sword varchar(255),
    barb_shield varchar(255),
    unlocked_powers varchar(255),
    active_powers varchar(255),
    power_limit int,
    weapons varchar(510),
    stamina int,
    last_login float,
    PRIMARY KEY(id)
  );"""
  cursor.execute(sqlCreateCommand)

def update_player_table(player,username="",password=""):
  connection = sqlite3.connect("./Data/player_data.db")
  cursor = connection.cursor()
  # Fetch uname and pword before insert
  unlocked_powers = [x.id for x in player.unlocked_powers]
  active_powers = [x.id for x in player.unlocked_powers]
  weapons = [x.id for x in player.weapons]
  try:
    sqlInsertCommand = f"""INSERT INTO PLAYERS VALUES (
      "{player.id}","{username}","{password}","{player.gold}","{player.gold_lv}",
      "{player.elixir}","{player.elixir_lv}","{player.d_elixir}","{player.d_elixir_lv}",
      "{player.barb.level}","{player.barb.weapons["sword"].id}","{player.barb.weapons["shield"].id}",
      "{unlocked_powers}","{active_powers}","{player.power_limit}","{weapons}","{player.stamina}","{time()}"
    );"""
    cursor.execute(sqlInsertCommand)
  except:
    sqlInsertCommand = f"""UPDATE PLAYERS SET
      th_level = "{player.th}",
      gold = "{player.gold}",
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
  
  
  

def update_all():
  update_troop_stats()
  update_attacks()
  update_weapons()
  update_troop_info()
  update_abilities()
  update_power_info()
  update_power_stats()
  add_update()

def main():
  if not should_update():
    print("Not updating databases.")
    return False
  # Database building
  else:
    update_all()
    print("All databases complete.")

if __name__ == '__main__':
    main()
