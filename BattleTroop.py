from Troop import Troop, get_troop_info
from BattleAttack import BattleAttack

def make_array(str):
  return str[1:-1].split(":")

def digit_range_check(vari,min=1,max=4):
  if len(vari) != 1 or vari.isdigit() == False or (int(vari) < min or int(vari) > max):
    return False
  return True

class BattleTroop(Troop):
  weaknesses = []
  resistances = []
  shield = 0
  flying = None
  broken = False
  
  def __init__(self,troop,level=1,powers=[]):
    if type(troop) == str:
      super().__init__(troop,level)
    elif type(troop) == Troop:
      super().__init__(troop.int_name,troop.level)
      self.weapons = troop.weapons
      self.powers = powers
      self.ownedBy = "Player"
    else:
      raise TypeError("Not a valid troop.")
    info = get_troop_info(self.int_name)
    self.weaknesses = make_array(info[4])
    self.resistances = make_array(info[5])
    self.shield = info[6]
    self.flying = (info[7] == 1)
    self.buffs = []
    self.debuffs = []
    self.broken = False
    self.original_action = 1000 / self.stats["speed"]
    self.action = self.original_action # AV = Action Value
    self.attacks = [BattleAttack(x.internal_name) for x in self.attacks]
    self.base_stats = self.stats
    self.calc_stats()

  def __str__(self):
    return self.name

  def resetAV(self):
    self.action = self.original_action

  def changeSpeed(self, queue, speed):
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
    while digit_range_check(option,1,2) == False:
      print("Invalid option.")
      option = input("What would you like to do?\n1: Attack\n2: Power\n")
    return int(option)

  def selectTarget(self,enemies):
    for i,x in enumerate(enemies):
      print(f"{i+1}: {x.name}")
    print(f"{i+2}: Return")
    choice = input("Select an enemy to attack. ")
    while digit_range_check(choice,1,i+2) == False:
      print("Invalid input.")
      choice = input("Select an enemy to attack. ")
    if int(choice) == i+2:
      return None
    return int(choice)-1

  def selectAttack(self):
    for i,x in enumerate(self.attacks):
      print(f"{i+1}: {x.display_name}")
    print(f"{i+2}: Return")
    choice = input("Select an attack to use. ")
    while digit_range_check(choice,max=i+2) == False:
      print("Invalid input.")
      choice = input("Select an attack to use. ")
    if int(choice) == i+2:
      return None
    return self.attacks[int(choice)-1]

  def selectPower(self):
    for i,x in enumerate(self.powers):
      print(f"{i+1}: {x}")
    print(f"{i+2}: Return")
    choice = input("Select an power to use. ")
    while digit_range_check(choice,max=i+2) == False:
      print("Invalid input.")
      choice = input("Select an power to use. ")
    if int(choice) == i+2:
      return None
    return self.powers[int(choice)-1]

  def attack(self,attack,enemy):
    damage = int(attack.power/10)
    enemy.stats["hp"] -= damage
    print(f"{self.name} used {attack.display_name} and {enemy.name} was dealt {damage} damage!")
    if enemy.shield > 0 and attack.element in enemy.weaknesses:
      enemy.shield -= attack.shieldDamage
      if enemy.shield <= 0:
        enemy.shield = 0
        enemy.broken = True
    return True

  def usePower(self,power,enemy):
    print(f"{power} was used on {enemy.name}!")
    return True