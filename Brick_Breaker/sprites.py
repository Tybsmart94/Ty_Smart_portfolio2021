#Sprite classes for platform game

#imports
import pygame as pg
from settings import *
vec = pg.math.Vector2

#Game
class Player(pg.sprite.Sprite):
    def __init__(self, game,x , y):
        self.groups = game.all_sprites, game.player_group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((50,20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = (WIDTH / 2)
        self.rect.bottom = (HEIGHT - (HEIGHT * .001))
        self.speedx = 0
        self.x = x
        self.y = y

    def update(self):
        self.rect.x += self.speedx
        self.speedx = 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT]:
            self.speedx = -10
        if keystate[pg.K_RIGHT]:
            self.speedx = 10

        # Keeps in the screen
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH

class Brick(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.brick_group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((50, 25))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.health = 3
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        if self.health == 2:
            self.image.fill(YELLOW)
        if self.health == 1:
            self.image.fill(RED)

class Ball(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.ball_group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = (WIDTH / 2)
        self.rect.bottom = (HEIGHT - (HEIGHT * .3))
        self.speedx = -5
        self.speedy = 5
        self.x = x
        self.y = y

    def update(self):

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.centerx > WIDTH or self.rect.centerx < 0:
            self.speedx *= -1
        if self.rect.centery < 0:
            self.speedy *= -1
        if self.rect.centery > HEIGHT:
            self.kill()
            self.game.playing = False
