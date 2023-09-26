import db_builder
import show_table
from Weapon import Weapon
from Battle import Battle
from Player import Player
from Graphics import *
from Player_data import *
from BattleTroop import digit_range_check

def main():
    run = True
    loggedIn = False
    pygame.display.set_caption('Barbarian Rising')
    pygame.display.set_icon(pygame.image.load("./Graphics/icon.png"))
    clock = pygame.time.Clock()
    barb = pygame.image.load("./Graphics/title barbarian.png").convert_alpha() 
    newAccBox = InputBox(WINDOW_WIDTH-245,WINDOW_HEIGHT-32,245,32,"Create New Account")
    emailText = "Username: "
    emailBox = InputBox(170,(WINDOW_HEIGHT/2)-50,192,32,emailText)
    pwordText = "Password: "
    pwordBox = InputBox(170,(WINDOW_HEIGHT/2)+50,192,32,pwordText)
    pygame.display.update()

    while not loggedIn:
      for event in pygame.event.get():
          if event.type == QUIT:
            pygame.quit()
            sys.exit()
          elif event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
            emailText = emailBox.handle_event(event, display, emailText)
            pwordText = pwordBox.handle_event(event, display, pwordText)   
            display.fill(yellow)
            display.blit(barb,(10,(WINDOW_HEIGHT/2)-barb.get_height()/2))
            newAccBox.draw(display)
            pwordBox.draw(display)
            emailBox.draw(display)
          elif event.type == KEYDOWN and event.key == K_0:
            option = input("1: Login\n2: Create new account")
            while not digit_range_check(option,1,2):
              print("Invalid input.")
              option = input("1: Login\n2: Create new account")
            option = int(option)
            email = input("Username: ")
            pword = input("Password: ")
            if option == 1:
              try:
                details = load_player_data(email,pword)
                print(details)
                player = Player(details[3]).load(details)
                loggedIn = True
              except IndexError:
                choice = input("Player Data not found. Create a new account? (y/n)")
                while choice[0].lower() != "y" and choice[0].lower() != "n":
                  print("Invalid input.")
                  choice = input("Player Data not found. Create a new account? (y/n)")
                if choice[0].lower() == "y":
                  option = 2
            if option == 2:
              player = Player("")
              update_player_table(player,email,pword)
              loggedIn = True
        
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

main()
#  for event in pygame.event.get():
#    handle_event(event)
