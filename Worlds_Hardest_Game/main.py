import pygame as pg
import random
from settings import *
import sys
from os import path
from sprites import *
from tilemap import *

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.font_name = pg.font.match_font(FONT_NAME)

        self.running = True
        self.deaths = 0
        self.level = 0
        self.coins = 0
        self.coins_on_screen = False
        self.total_coins = 0


    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map = Map(path.join(game_folder, LEVEL_MAP[self.level]))


    def new(self):
        # start a new game
        self.load_data()
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mob_group = pg.sprite.Group()
        self.end = pg.sprite.Group()
        self.coin_group = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row,)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'r':
                    self.mob = Mob(self, col, row, 'r')
                if tile == 'l':
                    self.mob = Mob(self, col, row, 'l')
                if tile == 'u':
                    self.mob = Mob(self, col, row, 'u')
                if tile == 'd':
                    self.mob = Mob(self, col, row, 'd')
                if tile == 'e':
                    End(self, col, row)
                if tile == 'c':
                    self.total_coins += 1
                    Coin(self, col, row)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_a:
            #         self.player.move(dx=-1)
            #     if event.key == pg.K_d:
            #         self.player.move(dx=1)
            #     if event.key == pg.K_s:
            #         self.player.move(dy=1)
            #     if event.key == pg.K_w:
            #         self.player.move(dy=-1)

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()

        #If player hits mob
        hits = pg.sprite.spritecollide(self.player, self.mob_group, False)
        for hit in hits:
            if hit:
                self.deaths += 1
                self.coins = 0
                self.new()

        #If player hits end
        hits = pg.sprite.spritecollide(self.player, self.end, False)
        for hit in hits:
            if hit and self.coins == self.total_coins:
                self.level += 1
                self.coins = 0
                self.new()

        #If player hits coin
        hits = pg.sprite.spritecollide(self.player, self.coin_group, True)
        for hit in hits:
            if hit:
                self.coins += 1

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, BLUE, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, BLUE, (0, y), (WIDTH, y))

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text("Deaths: "+ str(self.deaths), 22, WHITE, WIDTH / 2.5, 5)
        self.draw_text("Coins: "+ str(self.coins), 22, WHITE, WIDTH / 1.5, 5)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        #game splash/start screen
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH /2, HEIGHT /4)
        self.draw_text("W, A, S, D to move", 22, WHITE, WIDTH /2, HEIGHT /2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH /2, HEIGHT * 3/4)
        pg.display.flip()
        self.wait_for_key()

    def show_win_screen(self):
        #When you win
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH /2, HEIGHT /4)
        self.draw_text("YOU WIN", 22, WHITE, WIDTH /2, HEIGHT /2)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        # Game over/continue
        # pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.ogg'))
        # pg.mixer.music.play(loops=-1)
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, RED, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()
        # pg.mixer.music.fadeout(500)

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
