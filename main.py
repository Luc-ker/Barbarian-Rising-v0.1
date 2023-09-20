import db_builder
import show_table
from Weapon import Weapon
from Battle import Battle
from Player import Player

db_builder.main()
#show_table.main()
player = Player("A")
barb = player.barbarian

barb.unlockAttack("FLAMEBREATH")
#barb.unlockAttack("BALLOONSTORM")
barb.learnAttack("FLAMEBREATH")
#barb.learnAttack("BALLOONSTORM")
player.unlockPower("ETITAN")
player.equipPower("ETITAN")
player.unlockPower("EDRAG")
player.equipPower("EDRAG")
"""
battler3 = Troop("archer")
"""

barb.equip(Weapon("LONSDALEITESWORD"))
barb.equip(Weapon("WOODENSHIELD"))
barb.stats["crit_rate"] = 100
battle = Battle(player, ["ARCHER", "GIANT", "GOBLIN"])
