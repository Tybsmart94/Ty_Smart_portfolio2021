#Ty Smart
#Platformer Game
#04/07/21

#Imports
import pygame as pg
import random as r
from settings import *
from sprites import *

#Game Setup
class Game:
    def __init__(self):
        #Initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.score = 0

    def new(self):
        #Start a new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.player_group = pg.sprite.Group()
        self.brick_group = pg.sprite.Group()
        self.ball_group = pg.sprite.Group()
        self.player = Player(self, WIDTH / 2, 0)
        self.player_group.add(self.player)
        x = 5
        y = 5
        for col in range(5):
            for row in range(8):
                self.brick = Brick(self, x, y)
                self.brick_group.add(self.brick)
                x += 55
            y += 30
            x = 5
        self.brick_group.add(self.brick)
        self.ball = Ball(self, WIDTH / 1.5, HEIGHT / 1.5)
        self.ball_group.add(self.ball)
        self.run()

    def run(self):
        #Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def update(self):
        #Game Loop Update
        self.all_sprites.update()

        #If ball hits player
        hits = pg.sprite.spritecollide(self.ball, self.player_group, False)
        if hits:
            self.ball.speedy *= -1
            if self.player.speedx < 0:
                self.ball.speedx = -5
            elif self.player.speedx > 0:
                self.ball.speedx = 5
            else:
                self.ball.speedx = self.ball.speedx

        #If ball hits brick
        hits = pg.sprite.spritecollide(self.ball, self.brick_group, False)
        for hit in hits:
            hit.health -= 1
            self.ball.speedy *= -1
            if hit.health <= 0:
                hit.kill()
                self.score += 10

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def show_start_screen(self):
        #game splash/start screen
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("A and D to move", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        #Game over/continue
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", 48, RED, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()
        # pg.mixer.music.fadeout(500)

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()