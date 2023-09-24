import pygame, sys
from pygame.locals import *
from db_builder import update_player_table

pygame.init()

WINDOW_WIDTH = 512
WINDOW_HEIGHT = 384
font = pygame.font.SysFont('power clear', 36)
display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
textBox = pygame.image.load("./Graphics/text box.png").convert_alpha()

#colours
green = (0, 255, 0)
blue = (0, 0, 128)
orange = pygame.Color("Orange")

def blit_text(player,message="", color=blue,speed="Normal"):
    speeds = {
        "Slow"   : 90,
        "Normal" : 45,
        "Fast"   : 15,
        "Instant": 0
    }
    waitTime = speeds[speed]
    message = [word.split(' ') for word in message.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    boxWidth, boxHeight = textBox.get_size()
    boxWidth -= 40
    display.blit(textBox,(0,WINDOW_HEIGHT-boxHeight))
    pygame.display.update()
    pygame.time.wait(30)
    pos = (25, (WINDOW_HEIGHT - boxHeight + 11))
    x, y = pos
    row = 1
    for line in message:
        for word in line:
            text = ""
            wordSurface = font.render(word, 0, color)
            wordWidth, wordHeight = wordSurface.get_size()
            if x + wordWidth >= boxWidth:
                x, y, row = updateTextVariables(player,y,row,pos,wordHeight,boxHeight)
            for letter in word:
                text += letter
                text_surface = font.render(text, True, blue)
                display.blit(text_surface, (x, y))
                pygame.display.update()
                pygame.time.wait(waitTime)
            x += wordWidth + space
        end = (word is message[-1][-1])
        if end:
            waitForReturn(player)
            display.fill(orange)
            return
        x, y, row = updateTextVariables(player,y,row,pos,wordHeight,boxHeight)

def updateTextVariables(player, y, row, pos,wordHeight,boxHeight):
    x = pos[0]  # Reset the x.
    y += wordHeight + 3 # Start on new row.
    row += 1
    if row > 2:
        waitForReturn(player)
        display.blit(textBox,(0,WINDOW_HEIGHT-boxHeight))
        y = pos[1]
        row -= 2
    return x, y, row

def close(player):
    update_player_table(player)
    pygame.quit()
    sys.exit()

def waitForReturn(player):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                close(player)
            if event.type == KEYDOWN and event.key == K_RETURN:
                return
     
def main():
    pass

if __name__ == "main":
    main()
