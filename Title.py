import pygame, sys
from pygame.locals import QUIT, KEYDOWN

def message(display, message="", text=(0, 255, 0), textBg=(0, 0, 128)):
    message = input("Enter a message.\n")
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(message, True, text, textBg)
    display.blit(text,(0,436))
  

def title():
    run = True
    green = (0, 255, 0)
    blue = (0, 0, 128)
    pygame.init()
    score = 0
    display = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('Barbarian Rising')
    pygame.display.set_icon(pygame.image.load("./Graphics/icon.png"))
    clock = pygame.time.Clock()
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(f'Score: {score}', True, green, blue)

    while run:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            message(display)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        display.blit(text,(0,0))
        pygame.display.update()
        clock.tick(60)
#overtext = font.render('Press any key to restart.', True, green, blue)

if __name__ == "main":
    title()
