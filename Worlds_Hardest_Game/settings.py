# game options/settings
TITLE = "WORLDS HARDEST GAME"
WIDTH = 1024   #16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768   #16 * 48 or 32 * 24 or 64 * 12
FONT_NAME = 'arial'
FPS = 60

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

#Player settings
PLAYER_SPEED = 250

LEVEL_MAP = ['map1.txt', 'map2.txt', 'map.txt']

#Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
MOB_LAYER = 2
COLOR_LAYER = 3

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
CYAN = (0, 100, 100)
BGCOLOR = BLACK

