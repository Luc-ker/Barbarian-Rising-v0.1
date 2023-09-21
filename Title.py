import pygame, sys, time
from pygame.locals import *

pygame.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 450
font = pygame.font.Font('freesansbold.ttf', 32)
display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#colours
green = (0, 255, 0)
blue = (0, 0, 128)
orange = (235, 171, 52)

def message(message=""):
    message = input("Enter a message.\n")
    text = ''
    for letter in message:
        display.fill(orange)
        text += letter
        text_surface = font.render(text, True, blue)
        text_rect = text_surface.get_rect()
        text_rect.left = 4
        text_rect.bottom = int(WINDOW_HEIGHT*0.8)
        display.blit(text_surface, text_rect)
        pygame.display.update()
        pygame.time.wait(100)
  

def main():
    run = True
    score = 0
    pygame.display.set_caption('Barbarian Rising')
    pygame.display.set_icon(pygame.image.load("./Graphics/icon.png"))
    clock = pygame.time.Clock()
    display.fill(orange)
    text = font.render(f'Score: {score}', True, green, blue)

    while run:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            message()
        if keys[pygame.K_RETURN]:
            display.fill(orange)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        display.blit(text,(0,0))
        pygame.display.update()
        clock.tick(60)
#overtext = font.render('Press any key to restart.', True, green, blue)

if __name__ == "main":
    main()
