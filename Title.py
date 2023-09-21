import pygame, sys
from pygame.locals import QUIT, KEYDOWN

def main():
    run = True
    green = (0, 255, 0)
    blue = (0, 0, 128)
    pygame.init()
    score = 0
    display = pygame.display.set_mode((850, 634))
    clock = pygame.time.Clock()
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(f'Score: {score}', True, green, blue)

    while run:
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