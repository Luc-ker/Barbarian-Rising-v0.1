from Troop import Troop, get_troop_info
from BattleAttack import BattleAttack
from Status import Status
import random

def make_array(str):
  return str[1:-1].split(":")

def digit_range_check(vari,min=1,max=4):
  if len(vari) != 1 or not vari.isdigit() or (int(vari) < min or int(vari) > max):
    return False
  return True
  
def allFlying(enemies):
  if type(enemies) != list:
    return enemies.flying
  for enemy in enemies:
    if enemy.flying is False:
      return False
  return True

class BattleTroop(Troop):
  weaknesses = []
  resistances = []
  shield = 0
  flying = None
  broken = False
  
  def __init__(self,troop,level=1):
    if type(troop) == str:
      super().__init__(troop,level)
    elif type(troop) == Troop:
      super().__init__(troop.int_name,troop.level)
      self.weapons = troop.weapons
      self.ownedBy = troop.owner
      self.stats = troop.stats
      if troop.owner == "Player":
        self.attacks = troop.attacks
    else:
      raise TypeError("Not a valid troop.")
    info = get_troop_info(self.int_name)
    self.weaknesses = make_array(info[4])
    self.resistances = make_array(info[5])
    self.shield = info[6]
    self.flying = (info[7] == "true")
    self.buffs = []
    self.debuffs = []
    self.broken = False
    self.original_action = 1000 / self.stats["speed"]
    self.action = self.original_action # AV = Action Value
    self.attacks = [BattleAttack(x.internal_name).convert() for x in self.attacks]
    self.base_stats = self.stats
    self.calc_stats()

  def __str__(self):
    return self.name
    
  def calc_stats(self):
    self.stats = self.base_stats
    for buff in self.buffs:
      if buff.stat is not None:
        if buff.operand == "mult":
          self.stats.update({buff.stat: self.stats[buff.stat]+self.stats[buff.stat]*buff.mult})
        elif buff.operand == "add":
          self.stats.update({buff.stat: self.stats[buff.stat]+buff.mult})
        elif buff.operand == "minus":
          self.stats.update({buff.stat: self.stats[buff.stat]-buff.mult})

  def reduceShield(self,queue,shieldDmg):
    self.shield -= shieldDmg
    if self.shield <= 0:
      self.shield = 0
      self.breakShield(queue)

  def faint(self,queue):
    if self.stats["hp"] <= 0:
      print(f"{self.name} was defeated!")
      queue.dequeue(queue.getPos(self))

  def resetAV(self):
    self.action = self.original_action

  def addBuff(self,buff):
    if type(buff) != Status:
      raise TypeError
    self.buffs.append(buff)
    self.calc_stats()

  def addDebuff(self,debuff):
    if type(debuff) != Status:
      raise TypeError
    self.debuffs.append(debuff)
    self.calc_stats()

  def haveBuff(self,buff):
    for b in self.buffs:
      if buff.name == b.name and buff.causedBy == b.causedBy:
        return True
    return False

  def haveDebuff(self,debuff):
    for d in self.debuffs:
      if debuff.name == d.name and debuff.causedBy == d.causedBy:
        return True
    return False

  def buff(self,name,attack,turns,stat=None,operand=None,mult=None):
    buff = Status(name,attack,turns,stat,operand,mult)
    if not self.haveBuff(buff):
      self.addBuff(buff)

  def debuff(self,name,attack,turns,stat=None,operand=None,mult=None):
    debuff = Status(name,attack,turns,stat,operand,mult)
    if not self.haveDebuff(debuff):
      self.addDebuff(debuff)

  def changeSpeed(self, queue, attack, turns, speed):
    if speed == 0:
      return
    elif speed > 0:
      self.buff("Speed Buff",turns,attack,"speed","add",speed)
    elif speed < 0:
      self.debuff("Speed Debuff",turns,attack,"speed","minus",speed)
    distance = self.stats["speed"] * self.action
    self.stats["speed"] += speed
    self.updateAction()
    self.action = distance / self.stats["speed"]
    self.updateQueue(queue)

  def advanceForward(self, queue, mult):
    self.action -= (self.original_action * mult / 100)
    if self.action < 0:
      self.action = 0
    self.updateQueue(queue)

  def breakShield(self,queue):
    self.broken = True
    self.pushBack(25)
    self.updateQueue(queue)
    print(f"{self.name} was broken!")

  def updateQueue(self,queue):
    queue.dequeue(queue.getPos(self))
    queue.enqueue(self)

  def pushBack(self, mult):
    self.action += (self.original_action * mult / 100)

  def updateAction(self):
    self.original_action = 1000 / self.stats["speed"]

  def unbreak(self):
    self.broken = False

  def chooseAction(self):
    option = input("What would you like to do?\n1: Attack\n2: Power\n")
    while not digit_range_check(option,1,2):
      print("Invalid option.")
      option = input("What would you like to do?\n1: Attack\n2: Power\n")
    return int(option)

  def selectTarget(self,attack,enemies):
    i = 0
    if attack.target == "SingleTarget":
      for i,x in enumerate(enemies):
        print(f"{i+1}: {x.name}")
      print(f"{i+2}: Return")
      choice = input("Select an enemy to attack. ")
      while not digit_range_check(choice,1,i+2):
        print("Invalid input.")
        choice = input("Select an enemy to attack. ")
      choice = int(choice)
      if choice == i+2:
        return None
      return [enemies[choice-1]]
    elif attack.target == "Blast":
      if len(enemies) == 1:
        print(f"1: {enemies[0].name}")
      else:
        for i,x in enumerate(enemies):
          if i == 0:
            print(f"{i+1}: {x.name} and {enemies[i+1]}")
          elif i == len(enemies)-1:
            print(f"{i+1}: {x.name} and {enemies[i-1]}")
          else:
            print(f"{i+1}: {x.name}, {enemies[i-1]} and {enemies[i+1]}")
      print(f"{i+2}: Return")
      choice = input("Select enemies to attack. ")
      while not digit_range_check(choice,1,i+2):
        print("Invalid input.")
        choice = input("Select enemies to attack. ")
      choice = int(choice)
      if choice == i+2:
        return None
      if len(enemies) == 1:
        return [enemies]
      elif choice == 1:
        return [enemies[0],enemies[1]]
      elif choice == len(enemies):
        return [enemies[-1],enemies[-2]]
      else:
        return [enemies[choice-1],enemies[choice-2],enemies[choice]]
    elif attack.target == "AoE":
      print(f"""1: {', '.join([i.name for i in enemies[:-1]])} and {enemies[-1].name}""")
      print("2: Return")
      choice = input("Select enemies to attack. ")
      while not digit_range_check(choice,1,i+2):
        print("Invalid input.")
        choice = input("Select enemies to attack. ")
      if int(choice) == 2:
        return None
      return enemies

  def selectAttack(self):
    i = 0
    for i,x in enumerate(self.attacks):
      print(f"{i+1}: {x.display_name}")
    print(f"{i+2}: Return")
    choice = input("Select an attack to use. ")
    while not digit_range_check(choice,max=i+2):
      print("Invalid input.")
      choice = input("Select an attack to use. ")
    if int(choice) == i+2:
      return None
    return self.attacks[int(choice)-1]

  def selectPower(self,player):
    if len(player.active_powers) == 0: return None
    i = 0
    for i,x in enumerate(player.active_powers):
      print(f"{i+1}: {x}")
    print(f"{i+2}: Return")
    choice = input("Select an power to use. ")
    while not digit_range_check(choice,max=i+2):
      print("Invalid input.")
      choice = input("Select an power to use. ")
    if int(choice) == i+2:
      return None
    return player.active_powers[int(choice)-1]

  def usePower(self,battle,power,enemies):
    if len(enemies) == 1:
      names = enemies[0].name
    else:
      names = f"{', '.join([i.name for i in enemies[:-1]])} and {enemies[-1].name}"
    print(f"{power} was used on {names}!")
    if power.type == "dmg":
      self.usePowerEffect(battle,power,enemies,"hp")
    elif power.type == "slow":
      self.usePowerEffect(battle,power,enemies,"speed")
    elif power.type == "heal":
      battle.barb.stats["hp"] += power.power
    elif power.type == "weaken":
      self.usePowerEffect(battle,power,enemies,"attack")
    return True

  def usePowerEffect(self,battle,power,enemies,stat):
    if power.target == "SingleTarget":
      enemy = enemies[0]
      if stat != "speed":
        enemy.stats[stat] -= power.power
      if stat == "hp":
        print(f"{enemy.name} was dealt {power.power} damage!")
      elif stat == "speed":
        enemy.changeSpeed(power.power)
      elif stat == "attack":
        print(f"{enemy} was weakened!")
      if power.element in enemy.weaknesses:
        enemy.reduceShield(battle.queue,power.shieldDamage)
      if enemy.stats["hp"] <= 0:
        enemy.faint(battle.queue)
    elif power.target == "Blast":
      if stat != "speed":
        for enemy in enemies:
          if enemy == enemies[0]:
            dmg = power.power
            enemy.stats[stat] -= dmg
          else:
            dmg = round(power.power/2)
            enemy.stats[stat] -= dmg
          if stat == "hp":
            print(f"{enemy.name} was dealt {dmg} damage!")
      elif stat == "speed":
        for enemy in enemies:
          enemy.changeSpeed(power.power)
      elif stat == "attack":
        print(f"{', '.join([i.name for i in enemies[:-1]])} and {enemies[-1].name} were weakened!")
      for enemy in enemies:
        if power.element in enemy.weaknesses:
          enemy.reduceShield(battle.queue,power.shieldDamage)
        if enemy.stats["hp"] <= 0:
          enemy.faint(battle.queue)
    elif power.target == "AoE":
      for enemy in enemies:
        if stat != "speed":
          enemy.stats[stat] -= power.power
        if stat == "hp":
          print(f"{enemy.name} was dealt {power.power} damage!")
          if enemy.stats["hp"] <= 0:
            enemy.faint(battle.queue)
        elif stat == "speed":
          enemy.changeSpeed(power.power)
        elif stat == "attack":
          print("All enemies were weakened!")
        if power.element in enemy.weaknesses:
          enemy.reduceShield(battle.queue,power.shieldDamage)
        if enemy.stats["hp"] <= 0:
          enemy.faint(battle.queue)

  def attack(self,battle,attack,user,enemies):
    print(f"{self.name} used {attack.display_name}!")
    if allFlying(enemies) and "f" not in attack.flags:
      print("But the attack couldn't reach!")
    elif type(enemies) is list:
      for enemy in enemies:
        self.process_attack(battle,attack,user,enemy)
    else:
      self.process_attack(battle,attack,user,enemies)
    return True
  
  def process_attack(self,battle,attack,user,enemy):
    crit = (user.stats["crit_rate"] >= random.randint(1,100))
    print(crit)
    if crit:
      print("It was a critical hit!")
    damage = self.calc_damage(battle,attack,user,enemy,crit)
    enemy.stats["hp"] -= damage
    print(f"{enemy.name} was dealt {damage} damage!")
    if enemy.shield > 0 and attack.element in enemy.weaknesses:
      enemy.reduceShield(battle.queue,attack.shieldDamage)
    if enemy.stats["hp"] <= 0:
      enemy.faint(battle.queue)

  def calc_damage(self,battle,attack,user,enemy,crit):
    critdmg = 1
    if crit:
      critdmg = 1.5
    if enemy.immune(attack):
      return 0
    base = ((2*user.level/5+2)*attack.power*(user.stats["attack"]/enemy.stats["defence"]))/50 + 2
    dmg = base * critdmg
    return round(dmg)
  
  def immune(self,attack):
    if self.flying and "f" not in attack.flags:
      return True
    return False
  
  def ai(self,battle,enemy):
    if self.int_name == "GIANT" and enemy.debuffs == []:
      return self.attacks[1]
    #if self.ownedBy == "Player" or self.name in ["Giant"]:
    return random.choice(self.attacks)
