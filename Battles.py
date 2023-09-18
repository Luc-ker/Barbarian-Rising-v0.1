from Battle import Battle
from BattleTroop import BattleTroop

def golblinBattle1(player):
    result = Battle(player,[BattleTroop("GOBLIN"),BattleTroop("GOBLIN"),BattleTroop("GOBLIN")])
    if result == 1:
        player.addGold(500)
        player.addElixir(500)

def TH2Battle(player):
    result = Battle(player,[BattleTroop("GOBLIN",1),BattleTroop("ARCHER")])
    if result == 1:
        player.addGold(500)
        player.addElixir(500)
        player.unlockPower("ARCHER")