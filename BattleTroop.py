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
    self.addBuff(Status(name,attack,turns,stat,operand,mult))

  def debuff(self,name,attack,turns,stat=None,operand=None,mult=None):
    self.addDebuff(Status(name,attack,turns,stat,operand,mult))

  def changeSpeed(self, queue, attack, speed, turns):
    if speed == 0:
      return
    elif speed > 0:
      self.addBuff(Status("Speed Buff",attack,turns,"speed","add",speed))
    elif speed < 0:
      self.addDebuff(Status("Speed Debuff",attack,turns,"speed","minus",speed))
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
    for i,x in enumerate(enemies):
      print(f"{i+1}: {x.name}")
    print(f"{i+2}: Return")
    choice = input("Select an enemy to attack. ")
    while not digit_range_check(choice,1,i+2):
      print("Invalid input.")
      choice = input("Select an enemy to attack. ")
    if int(choice) == i+2:
      return None
    return int(choice)-1

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
    if len(player.powers) == 0: return None
    i = 0
    for i,x in enumerate(player.powers):
      print(f"{i+1}: {x}")
    print(f"{i+2}: Return")
    choice = input("Select an power to use. ")
    while not digit_range_check(choice,max=i+2):
      print("Invalid input.")
      choice = input("Select an power to use. ")
    if int(choice) == i+2:
      return None
    return player.powers[int(choice)-1]

  def usePower(self,power,enemy):
    print(f"{power} was used on {enemy.name}!")
    return True

  def attack(self,battle,attack,enemy):
    if enemy.flying and "f" not in attack.flags:
      print("The attack couldn't reach!")
    else:
      damage = self.calc_damage(battle,attack,enemy)
      enemy.stats["hp"] -= damage
      print(f"{self.name} used {attack.display_name} and {enemy.name} was dealt {damage} damage!")
      if enemy.shield > 0 and attack.element in enemy.weaknesses:
        enemy.shield -= attack.shieldDamage
        if enemy.shield <= 0:
          enemy.shield = 0
          enemy.breakShield(battle.queue)
    return True

  def calc_damage(self,battle,attack,enemy):
    dmg = int(attack.power/10)
    return dmg
  
  def ai(self,battle,enemy):
    #if self.ownedBy == "Player" or self.name in ["Giant"]:
    return random.choice(self.attacks)
