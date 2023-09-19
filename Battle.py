from BattleTroop import BattleTroop
from Player import Player
from Turn_Order import PriorityQueue
from BattleAttack import BattleAttack
import os

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def digit_range_check(vari,min=0,max=9):
  if len(vari) != 1 or vari.isdigit() is False or (int(vari) < min or int(vari) > max):
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
    self.turnTime = 0
    self.turns = 1
    self.start()

  def allEnemiesBeaten(self):
    for enemy in self.enemyTroops:
      if enemy.stats["hp"] > 0:
        return False
    return True

  def start(self):
    enemies = self.enemyTroops
    if len(enemies) == 1:
      print(f"Battle occured between {self.barb.name} vs {enemies[0].name}")
    else:
      print(f"Battle occured between {self.barb.name} vs {', '.join([i.name for i in enemies[:-1]])} and {enemies[-1].name}")
    self.queue.enqueue(self.barb)
    for enemy in self.enemyTroops:
      self.queue.enqueue(enemy)
    self.mainLoop()

  def mainLoop(self):
    while self.barb.stats["hp"] >= 0 and not self.allEnemiesBeaten():
      self.turnTime += self.queue.toZero()
      while self.turnTime >= 150:
        self.turnTime -= 150
        self.turns += 1
      self.queue.printActionOrder()
      troop = self.queue.queue[0]
      if troop == self.barb:
        attacked = False
        targets = None
        attack = None
        while not attacked:
          choice = troop.chooseAction()
          if choice == 1:
            attack = troop.selectAttack()
            if attack is not None: targets = troop.selectTarget(attack,self.enemyTroops)
            if targets is not None and attack.target == "AoE":
              attacked = troop.attack(self,attack,troop,self.enemyTroops)
            elif targets is not None:
              attacked = troop.attack(self,attack,troop,self.enemyTroops[targets])
          elif choice == 2:
            power = troop.selectPower(self.player)
            if power is not None: targets = troop.selectTarget(power,self.enemyTroops)
            if targets is not None: attacked = troop.usePower(self,power,self.enemyTroops[targets])
        if attack is not None:
          attack.effect(self,troop,targets)
      else:
        attack = troop.ai(self,self.barb)
        troop.attack(self,attack,troop,self.barb)
        attack.effect(self,troop,self.barb)
      if self.barb.stats["hp"] <= 0:
        input("Press Enter to retreat.")
        return 0
      elif self.allEnemiesBeaten():
        input("Press Enter to finish the battle.")
        return 1
      self.queue.dequeue()
      troop.resetAV()
      self.queue.enqueue(troop)
      for buff in troop.buffs:
        print(buff.name,buff.turns)
        buff.turns -= 1
        print(buff.name,buff.turns)
        if buff.turns <= 0:
          troop.buffs.remove(buff)
      for debuff in troop.debuffs:
        debuff.turns -= 1
        if debuff.turns <= 0:
          troop.buffs.remove(debuff)
      
    