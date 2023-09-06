import sqlite3
import os

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
    for line in f1:
      if line[0] == "#" or line == "\n":
        pass
      elif line[0] == "[":
        connection.commit()
        troop = line[1:-2]
        print(f"Creating table for {troop}'s stats...")
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
  print("Troop databases updated.")

def update_attacks():
  with open("./Stats/attacks.txt", "r") as f1:
    if os.path.exists("./Data/attacks.db"):
      os.remove("./Data/attacks.db")
    sqlCreateCommand = """CREATE TABLE IF NOT EXISTS ATTACKS(
      internal_name varchar(255),
      display_name varchar(255),
      element varchar(255),
      power int,
      effect_code varchar(255),
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
        print(f"Creating row for {attack[0]}...")
        desc = ",".join(attack[7:-1] + [attack[-1]])
        sqlInsertCommand = f"""INSERT INTO ATTACKS VALUES ("{attack[0]}","{attack[1]}","{attack[2]}","{attack[3]}","{attack[4]}","{attack[5]}","{attack[6]}","{desc}");"""
        cursor.execute(sqlInsertCommand)
        connection.commit()
  print("Attack database updated.")

def update_weapons():
  with open("./Stats/weapons.txt", "r") as f1:
    if os.path.exists("./Data/weapons.db"):
      os.remove("./Data/weapons.db")
    sqlCreateCommand = """CREATE TABLE IF NOT EXISTS WEAPONS(
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
        print(f"Creating row for {weapon[0]}...")
        desc = ",".join(weapon[4:-1] + [weapon[-1]])
        sqlInsertCommand = f"""INSERT INTO WEAPONS VALUES ("{weapon[0]}","{weapon[1]}","{weapon[2]}","{weapon[3]}","{desc}");"""
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
        print(f"Creating row for {info[0]}...")
        desc = ",".join(info[8:-1] + [info[-1]])
        sqlInsertCommand = f"""INSERT INTO TROOPS VALUES ("{info[0]}","{info[1]}","{info[2]}","{info[3]}","{info[4]}","{info[5]}","{info[6]}","{info[7]}","{desc}");"""
        cursor.execute(sqlInsertCommand)
        connection.commit()
  print("Troop info database updated.")

def update_abilities():
  with open("./Stats/abilities.txt", "r") as f1:
    if os.path.exists("./Data/abilities.db"):
      os.remove("./Data/abilities.db")
    sqlCreateCommand = """CREATE TABLE IF NOT EXISTS ABILITIES(
      internal_name varchar(255),
      display_name varchar(255),
      description varchar(510),
      PRIMARY KEY(internal_name)
    );"""
    connection = sqlite3.connect("./Data/abilities.db")
    cursor = connection.cursor()
    cursor.execute(sqlCreateCommand)
    for line in f1:
      if line[0] == "#" or line == "\n":
        pass
      else:
        ability = line[:-1].split(",")
        print(f"Creating row for {ability[0]}...")
        desc = ",".join(ability[2:-1] + [ability[-1]])
        sqlInsertCommand = f"""INSERT INTO ABILITIES VALUES ("{ability[0]}","{ability[1]}","{desc}");"""
        cursor.execute(sqlInsertCommand)
        connection.commit()
  print("Ability database updated.")

def update_all():
  update_troop_stats()
  update_attacks()
  update_weapons()
  update_troop_info()
  update_abilities()
  add_update()

def main():
  if should_update() == False:
    print("Not updating databases.")
    return False
  # Database building
  else:
    update_all()
    print("All databases complete.")

if __name__ == '__main__':
    main()
