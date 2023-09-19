import db_builder
import show_table
from Weapon import Weapon
from Battle import Battle
from Player import Player

#db_builder.main()
#show_table.main()
player = Player("A")
barb = player.barbarian
print(barb)
print(player.barbarian)

#barb.unlockAttack("QUICKDRAWSLASH")
barb.unlockAttack("BALLOONSTORM")
#barb.learnAttack("QUICKDRAWSLASH")
barb.learnAttack("BALLOONSTORM")
barb.show_attacks()
player.unlockPower("ARCHER")
player.equipPower("ARCHER")
"""
battler3 = Troop("archer")
"""

barb.equip(Weapon("LONSDALEITESWORD"))
barb.equip(Weapon("WOODENSHIELD"))
battle = Battle(player,["GIANT","GIANT","GOBLIN"])