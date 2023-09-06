import db_builder
#import show_table
from Troop import Troop
from Weapon import Weapon
from Battle import Battle
from Player import Player

db_builder.main()
#show_table.main()
player = Player("A")
battler = player.barbarian
"""
battler3 = Troop("archer")
"""

battler.equip(Weapon("LONSDALEITESWORD"))
battler.equip(Weapon("WOODENSHIELD"))
battle = Battle(player,["giant"])
