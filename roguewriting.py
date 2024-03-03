import pygame, random, pygame_gui
import mapping as M
import display as D
import keyboard as K
import loops as L

#random.seed(420)
pygame.init()
pygame.font.init()

#Size of tiles
textSize = 32
width = 1280
height = 720
textWidth = int(width / textSize)
textHeight = int(height / textSize)
#Haven't used yet
colors = L.ColorDict()
#dictionary mapping renderID to the image
tileDict = M.TileDict(textSize, colors)
#Responsible for game loops
loop = L.Loops(width, height, textSize)

display = D.Display(width, height, textSize, textWidth, textHeight)

keyboard = K.Keyboard()

player_turn = True
loop.init_game(display)
while player_turn:
    loop.change_screen(keyboard, display, colors, tileDict)
    player_turn = loop.action_loop(keyboard, display)
