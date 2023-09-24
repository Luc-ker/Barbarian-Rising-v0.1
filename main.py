import db_builder
import show_table
from Weapon import Weapon
from Battle import Battle
from Player import Player
from Graphics import *

def main():
    run = True
#    score = 0
    pygame.display.set_caption('Barbarian Rising')
    pygame.display.set_icon(pygame.image.load("./Graphics/icon.png"))
    clock = pygame.time.Clock()
    display.fill(orange)
    player = Player("A")
#    text = font.render(f'Score: {score}', True, green, blue)

    while run:
        for event in pygame.event.get():
            if event.type == QUIT:
                close(player)
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    blit_text("Enter a message.\nDon't type too much. df df dfd df df df",speed="Fast")
                if event.key == K_RETURN:
                    display.fill(orange)
#        display.blit(text,(0,0))
        pygame.display.update()
        clock.tick(60)

db_builder.main()
"""
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

barb.equip(Weapon("LONSDALEITESWORD"))
barb.equip(Weapon("WOODENSHIELD"))
#battle = Battle(player, ["ARCHER", "GIANT", "GOBLIN"])
"""

#main()
