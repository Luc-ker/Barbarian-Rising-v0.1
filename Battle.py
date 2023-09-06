from BattleTroop import BattleTroop
from Player import Player
from Turn_Order import PriorityQueue
import os
import random

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def digit_range_check(vari,min=0,max=9):
  if len(vari) != 1 or vari.isdigit() == False or (int(vari) < min or int(vari) > max):
    return False
  return True

class Battle():
  def __init__(self,player,enemyTroops,mechanic=None):
    if type(player) != Player:
      return
    self.player = player
    self.barb = BattleTroop(player.barbarian)
    self.enemyTroops = [BattleTroop(x) for x in enemyTroops]
    self.mechanic = mechanic
    self.queue = PriorityQueue()
    self.start()

  def allEnemiesBeaten(self):
    for enemy in self.enemyTroops:
      if enemy.stats["hp"] > 0:
        return False
    return True

  def start(self):
    enemies = self.enemyTroops
    last = enemies.pop()
    print(f"Battle occured between {self.barb.name} vs {', '.join([i.name for i in enemies])} and {last.name}")
    self.enemyTroops.append(last)
    self.queue.enqueue(self.barb)
    for enemy in self.enemyTroops:
      self.queue.enqueue(enemy)
    self.queue.toZero()
    self.queue.printActionOrder()
    self.mainLoop()

  def mainLoop(self):
    while self.barb.stats["hp"] >= 0 and not self.allEnemiesBeaten():
      troop = self.queue.dequeue()
      if troop == self.barb:
        attacked = False
        targets = None
        while not attacked:
          choice = troop.chooseAction()
          if choice == 1:
            attack = troop.selectAttack()
            if attack != None: targets = troop.selectTarget(self.enemyTroops)
            if targets != None: attacked = troop.attack(attack,self.enemyTroops[targets])
          elif choice == 2:
            power = troop.selectPower()
            if power != None: targets = troop.selectTarget(self.enemyTroops)
            if targets != None: attacked = troop.usePower(power,self.enemyTroops[targets])
        attack.effect(self.queue,troop,targets)
      else:
        choice = random.randint(0,len(troop.attacks)-1)
        attack = troop.attacks[choice]
        troop.attack(attack,self.barb)
        attack.effect(self.queue,troop,self.barb)
      if self.barb.stats["hp"] <= 0:
        input("Press Enter to retreat.")
        return 0
      elif self.allEnemiesBeaten():
        input("Press Enter to finish the battle.")
        return 1
      self.queue.toZero()
      troop.resetAV()
      self.queue.enqueue(troop)
      self.queue.printActionOrder()
      
    