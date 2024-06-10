from dungeon_generation.configuration_data import *
from display_generation import *
from loop_workflow import keyboard as K
import loops as L
import static_configs


import warnings
warnings.filterwarnings("ignore")

#..random.seed(420)1
pygame.init()
pygame.font.init()

#Size of tiles
textSize = 32
infoObject = pygame.display.Info()
width = infoObject.current_w #1920 * 4/5
height = infoObject.current_h #1080 * 4/5
textWidth = int(width / textSize)

textHeight = int(height / textSize)
#dictionary mapping renderID to the image
tileDict = static_configs.TileDict(textSize)
ascaiiDict = static_configs.AscaiiTileDict()
dungeonData = DungeonData()
#Responsible for game loops

display = Display(width, height, textSize, textWidth, textHeight)
keyboard = K.Keyboard()
loop = L.Loops(width, height, textSize, tileDict, display, keyboard, ascaiiDict, dungeonData)

player_turn = True
loop.init_game(display)
loop.change_loop(L.LoopType.main)

while player_turn:
    loop.render_screen(display)
    player_turn = loop.action_loop(keyboard, display)
