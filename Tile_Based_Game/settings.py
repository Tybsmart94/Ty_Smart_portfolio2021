#Imports
import pygame as pg
vec = pg.math.Vector2

# game options/settings
TITLE = "Dungeon"
WIDTH = 1024   #16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768   #16 * 48 or 32 * 24 or 64 * 12
FPS = 60

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

#Other
WALL_IMG = 'tile_71.png'

#Mob settings
MOB_IMG = 'zoimbie1_hold.png'
SPLAT = 'splat green.png'
MOB_SPEED = [150, 100, 75, 125, 150]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50
DETECT_RADIUS = 400

#Sounds
BG_MUSIC = 'espionage.ogg'
PLAYER_HIT_SOUNDS = ['pain_8.wav', 'pain_9.wav', 'pain_10.wav', 'pain_11.wav']
ZOMBIE_MOAN_SOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav', 'zombie-roar-4.wav',
                      'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav', 'zombie-roar-8.wav']
ZOMBIE_HIT_SOUNDS = ['splat-15.wav']
WEAPON_SOUNDS = {'pistol': ['pistol.wav'],
                 'shotgun': ['shotgun.wav']}
EFFECTS_SOUNDS = {'level_start': 'level_start.wav',
                  'health_up': 'health_pack.wav',
                  'gun_pickup': 'gun_pickup.wav'}

#Weapon settings
BULLET_IMG = 'bullet.png'
WEAPONS = {}
WEAPONS['pistol'] = {'bullet_speed': 500,
                     'bullet_lifetime': 1000,
                     'rate': 250,
                     'kickback': 200,
                     'spread': 5,
                     'damage': 10,
                     'bullet_size': 'lg',
                     'bullet_count': 1}
WEAPONS['shotgun'] = {'bullet_speed': 400,
                     'bullet_lifetime': 500,
                     'rate': 900,
                     'kickback': 300,
                     'spread': 20,
                     'damage': 5,
                     'bullet_size': 'sm',
                     'bullet_count': 12}

#Player settings
PLAYER_SPEED = 250
PLAYER_IMG = 'manBlue_gun.png'
PLAYER_ROT_SPEED = 250
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(30, 10)
PLAYER_HEALTH = 100

#Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

#Items
ITEM_IMAGES = {'health': 'health_pack.png',
               'shotgun': 'obj_shotgun.png'}
HEALTH_PACK_ADD_AMOUNT = 20
BOB_RANGE = 15
BOB_SPEED = 0.4

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
LIGHTGREY = (100, 100, 100)
BROWN = (106, 55, 5)
CYAN = (0, 100, 100)
BGCOLOR = BROWN

#Effects
MUZZLE_FLASHES = ['whitePuff15.png', 'whitePuff16.png', 'whitePuff17.png', 'whitePuff18.png']
FLASH_DURATION = 40
DAMAGE_ALPHA = [i for i in range(0, 255, 55)]
