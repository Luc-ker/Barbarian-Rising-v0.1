from Battle import Battle
from BattleTroop import BattleTroop

def golblinBattle1(player):
    Battle(player,[BattleTroop("goblin"),BattleTroop("goblin"),BattleTroop("goblin")])
    player.addGold(500)
    player.addElixir(500)

def TH2Battle(player):
    Battle(player,[BattleTroop("goblin",1),BattleTroop("archer")])
    player.addGold(500)
    player.addElixir(500)
    player.unlockPower("archer")