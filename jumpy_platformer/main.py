#Ty Smart
#Platformer Game
#04/07/21

#Imports
import pygame as pg
import random as r
from settings import *
from sprites import *
from os import path

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
        self.load_data()

    def load_data(self):
        #Load high score
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        #Load spritesheet image
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        #Cloud Images
        self.cloud_images = []
        for i in range(1, 4):
            self.cloud_images.append(pg.image.load(path.join(img_dir, 'cloud{}.png'.format(i))).convert())
        #load sounds
        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Jump33.wav'))
        self.boost_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Boost16.wav'))

    def new(self):
        #Start a new game
        self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.clouds = pg.sprite.Group()
        self.player = Player(self)
        for plat in PLATFORM_LIST:
            Platform(self, *plat)
        self.mob_timer = 0
        pg.mixer.music.load(path.join(self.snd_dir, 'Happy Tune.ogg'))
        for i in range(10):
            c = Cloud(self)
            c.rect.y += 500
        self.run()

    def run(self):
        #Game Loop
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def update(self):
        #Game Loop Update
        self.all_sprites.update()

        #Spawn a mob?
        now = pg.time.get_ticks()
        if now - self.mob_timer > 5000 + r.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)
        #Hit a mob?
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)
        if mob_hits:
            self.playing = False

        #Check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.centery:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right + 10 and self.player.pos.x > lowest.rect.left - 10:
                    if self.player.pos.y < lowest.rect.bottom:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False

        #If player reaches top quarter of screen
        if self.player.rect.top <= HEIGHT / 4:
            if r.randrange(100) < 15:
                Cloud(self)
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for cloud in self.clouds:
                cloud.rect.y += max(abs(self.player.vel.y / 2), 2)
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10

        #If player hits a powerup
        pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type == 'boost':
                self.boost_sound.play()
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False

        #Death
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

        #Spawn new platforms to keep same avg number
        while len(self.platforms) < 6:
            width = r.randrange(50, 100)
            p = Platform(self, r.randrange(0, WIDTH-width),
                         r.randrange(-75, -39))
            self.platforms.add(p)
            self.all_sprites.add(p)

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
        pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH /2, HEIGHT /4)
        self.draw_text("A and D to move, space to jump", 22, WHITE, WIDTH /2, HEIGHT /2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH /2, HEIGHT * 3/4)
        self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH /2, 15)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        #Game over/continue
        # pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.ogg'))
        # pg.mixer.music.play(loops=-1)
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, RED, WIDTH /2, HEIGHT /4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH /2, HEIGHT /2)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH /2, HEIGHT * 3/4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("YOU GOT A NEW HIGH SCORE!", 22, WHITE, WIDTH /2, HEIGHT /2+40)
            with open(path.join(self.dir, HS_FILE), 'w')as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT /2 + 40)
        pg.display.flip()
        self.wait_for_key()
        # pg.mixer.music.fadeout(500)


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()