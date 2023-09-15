import db_builder
import show_table
from Weapon import Weapon
from Battle import Battle
from Player import Player
from Attack import Attack

db_builder.main()
show_table.main()
player = Player("A")
player.teachAttack("QUICKDRAWSLASH")
player.unlockPower("ARCHER")
player.equipPower("ARCHER")
print(player.active_powers)
print(player.unlocked_powers)
battler = player.barbarian
"""
battler3 = Troop("archer")
"""

battler.equip(Weapon("LONSDALEITESWORD"))
battler.equip(Weapon("WOODENSHIELD"))
battle = Battle(player,["giant"])