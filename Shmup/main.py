#Ty Smart
#3/10/21

#Imports
import pygame as pg
import random as r
import math
from os import path

img_dir = path.join(path.dirname(__file__), 'imgs')
Snd_dir = path.join(path.dirname(__file__), 'Snd')


# Game Functions
####################################################################

# Player Functions
class Player(pg.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.image = pg.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = (WIDTH / 2)
        self.rect.bottom = (HEIGHT - (HEIGHT * .05))
        self.radius = 20
        self.speedx = 0
        self.shield = 100
        self.keypressed = False
        self.shoot_delay = 250
        self.last_shot = pg.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pg.time.get_ticks()
        self.power = 1
        self.power_time = pg.time.get_ticks()
        self.fuel = 100
        self.power_level = 1
        self.lazer_timer = 2500

    def shields_up(self, num):
        self.shield += num
        if self.shield >= 100:
            self.shield = 100

    def fuel_add(self, num):
        self.fuel += num
        if self.fuel >= 100:
            self.fuel = 100

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power_level == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullet_group.add(bullet)
                shoot_sound.play()
            if self.power_level == 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullet_group.add(bullet1)
                bullet_group.add(bullet2)
                shoot_sound.play()
            if self.power_level == 3:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                bullet3 = Bullet(self.rect.centerx, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                bullet_group.add(bullet1)
                bullet_group.add(bullet2)
                bullet_group.add(bullet3)
                shoot_sound.play()
            if self.power_level == 4:
                bullet1 = Bullet(self.rect.left, self.rect.top - 1)
                bullet2 = Bullet(self.rect.centerx-5, self.rect.top - 1)
                bullet3 = Bullet(self.rect.centerx+5, self.rect.top - 1)
                bullet4 = Bullet(self.rect.right, self.rect.top - 1)
                bullet1.speedx = -5
                bullet4.speedx = 5
                bullet2.speedx = -2.5
                bullet3.speedx = 2.5
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                all_sprites.add(bullet4)
                bullet_group.add(bullet1)
                bullet_group.add(bullet2)
                bullet_group.add(bullet3)
                bullet_group.add(bullet4)
                shoot_sound.play()
            if self.power_level == 5:
                bullet1 = Bullet(self.rect.left, self.rect.top - 1)
                bullet2 = Bullet(self.rect.centerx-5, self.rect.top - 1)
                bullet3 = Bullet(self.rect.centerx+5, self.rect.top - 1)
                bullet4 = Bullet(self.rect.right, self.rect.top - 1)
                bullet5 = Bullet(self.rect.centerx, self.rect.top - 1)
                bullet1.speedx = -5
                bullet4.speedx = 5
                bullet2.speedx = -2.5
                bullet3.speedx = 2.5
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                all_sprites.add(bullet4)
                all_sprites.add(bullet5)
                bullet_group.add(bullet1)
                bullet_group.add(bullet2)
                bullet_group.add(bullet3)
                bullet_group.add(bullet4)
                bullet_group.add(bullet5)
                shoot_sound.play()






    def powerup(self):
        self.power += 1
        self.power_time = pg.time.get_ticks()

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pg.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

    def update(self):
        # unhide if hidden
        if self.hidden and pg.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        keystate = pg.key.get_pressed()
        self.rect.x += self.speedx
        if self.shoot_delay <= 250 and pg.time.get_ticks() - self.lazer_timer > 2500:
            self.lazer_timer = pg.time.get_ticks()
            self.shoot_delay = 250

    # Movement
        self.speedx = 0
        self.speedy = 0
        if self.fuel >= 0:
            # Moving Left
            if keystate[pg.K_LEFT]:
                self.speedx += -10
                self.fuel -= .25
            #Moving Right
            if keystate[pg.K_RIGHT]:
                self.speedx += 10
                self.fuel -= .25
        #Shooting
        if keystate[pg.K_SPACE]:
            self.shoot()

#Keeps in the screen
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH


class NPC(pg.sprite.Sprite):
    def __init__(self):
        #Getting different Meteors
        meteor_images = []
        meteor_list =["meteorBrown_big1.png", "meteorBrown_med1.png",
                      "meteorBrown_tiny2.png", "meteorBrown_small2.png",
                      "meteorGrey_big2.png"]
        for img in meteor_list:
            meteor_images.append(pg.image.load(path.join(img_dir, img)).convert())

        super(NPC, self).__init__()
        self.image_orig = r.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK  )
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width  * .85 / 2)
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = r.randrange(WIDTH - self.rect.width)
        self.rect.y = r.randrange(-100, -40)
        self.speedy = r.randrange(1, 8)
        self.speedx = r.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = r.randint(-8, 8)
        self.last_update = pg.time.get_ticks()
        self.img = self.image.copy()



    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 60:
            self.last_update = now
            # rotate sprite
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pg.transform.rotate(self.image, self.rot_speed)
            new_image = pg.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()


        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = r.randrange(WIDTH - self.rect.width)
            self.rect.y = r.randrange(-100, -40)
            self.speedy = r.randrange(1,8)

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        # self.image = pg.Surface((10,10))
        # self.image.fill(GREEN)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        self.speedx = 0

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pg.sprite.Sprite):
    def __init__(self, center, size):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Pow(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.type = r.choice(['shield', 'gun', 'fuel','lazer'])
        self.image = powerup_images[self.type]
        if self.type == 'fuel':
            self.image.set_colorkey(WHITE)
        elif self.type == 'lazer':
            self.image.set_colorkey(WHITE)
        else:
            self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the bottom of the screen
        if self.rect.top > HEIGHT:
            self.kill()


####################################################################
# Game Constants
####################################################################
HEIGHT = 600
WIDTH = 600
FPS = 60

# Colors (R,G,B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

powchance = ["shield","gun","fuel","shield","shield","shield","fuel", "fuel", "fuel", "fuel"]
powTypes = ["gun", "shield", "fuel","lazer"]



POWERUP_TIME = 6000

title = "Shmup"

creator = "Ty Smart Python 2/4"

####################################################################
# initialize pygame and create window
####################################################################
pg.init()
pg.mixer.init()

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(title)
clock = pg.time.Clock()
################################################################
# Load all game graphics
################################################################
#Game Images
background = pg.image.load(path.join(img_dir, 'starfield.png')).convert()
background_rect = background.get_rect()
player_img = pg.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
player_mini_img = pg.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
meteor_img = pg.image.load(path.join(img_dir, "meteorBrown_med1.png")).convert()
bullet_img = pg.image.load(path.join(img_dir, "laserRed16.png")).convert()

#Power-up images
powerup_images = {}
powerup_images['shield'] = pg.image.load(path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pg.image.load(path.join(img_dir, 'bolt_gold.png')).convert()
powerup_images['fuel'] = pg.image.load(path.join(img_dir, "Coal.png")).convert()
powerup_images['lazer'] = pg.image.load(path.join(img_dir, "lazer.png")).convert()

#Explosions
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pg.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pg.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pg.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    player_expl = pg.transform.scale(img, (100, 100))
    explosion_anim['player'].append(player_expl)
################################################################
# Load all game sounds
################################################################
#Sounds for game
shoot_sound = pg.mixer.Sound(path.join(Snd_dir, 'Lazer Fire 1.wav'))
expl_sounds = []
for Snd in ['Explosion 1.wav','Explosion 2.wav']:
    expl_sounds.append(pg.mixer.Sound(path.join(Snd_dir, Snd)))
pg.mixer.music.load(path.join(Snd_dir, 'MattOglseby - 3.ogg'))
pg.mixer.music.set_volume(0.4)

####################################################################
# Game Loop
####################################################################
# game update Variables
########################################
playing = True
game_over = True
pg.mixer.music.play(loops=-1)

##################################################
# Render
##################################################
font_name = pg.font.match_font('arial')


def newmob():
    m = NPC()
    all_sprites.add(m)
    npc_group.add(m)

def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, BLUE, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)
def draw_fuel_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, GREEN, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)
def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, title, 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, "Created by "+creator, 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, "Arrow keys to move, Space Bar to fire", 18, WIDTH/2, HEIGHT*3/4)
    draw_text(screen, "Press any key to begin", 18, WIDTH/2, HEIGHT*7/8)
    pg.display.flip()
    waiting = True
    while waiting:
        clock.tick()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYUP:
                waiting = False
########################################
#Game Over
########################################

while playing:
    if game_over:
        show_go_screen()
        game_over = False
        ####################################################################
        # create Sprite groups
        ####################################################################
        all_sprites = pg.sprite.Group()
        players_group = pg.sprite.Group()
        npc_group = pg.sprite.Group()
        bullet_group = pg.sprite.Group()
        powerups = pg.sprite.Group()
        ####################################################################
        # create Game Objects
        ####################################################################
        player = Player()
        for i in range(8):
            newmob()
        ####################################################################
        # add objects to sprite groups
        ####################################################################
        players_group.add(player)

        for i in players_group:
            all_sprites.add(i)
        for i in npc_group:
            all_sprites.add(i)


        #########################################



        score = 0


    # timing
    ##################################################
    clock.tick(FPS)
    ##################################################
    # collecting Input
    ##################################################

    # Quiting the game when we hit the x
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                playing = False
        if event.type == pg.QUIT:
            playing = False



    # Check to see if a npc hit the player
    hits = pg.sprite.groupcollide(npc_group, bullet_group, True, True)
    for hit in hits:
        score += 50 - hit.radius
        r.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if r.random() > 0.6:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()


    # Check to see if bullet hits npc
    hits = pg.sprite.spritecollide(player, npc_group, True, pg.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.power_level = 1
            player.shield = 100
            player.fuel = 100
        if player.lives <= 0:
            show_go_screen()
            player.lives = 3
            player.fuel = 100

            # if the player died and the explosion has finished playing
            if not player.alive() and not death_explosion.alive():
                running = False

    # check to see if player hit a powerup
    hits = pg.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += r.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.shoot_delay = 250
            player.power_level += 1
            if player.power_level >= 5:
                player.power_level = 5
        if hit.type == 'fuel':
            player.fuel += r.randrange(30, 50)
            if player.fuel >= 100:
                player.fuel = 100
        if hit.type == 'lazer':
            player.power_level -= 1
            player.shoot_delay = 50
            if player.power_level <= 1:
                player.power_level = 1






    ##################################################
    # Updates
    ##################################################
    all_sprites.update()

    ##################################################
    # Game Functions
    ##################################################
    def spawn_npc():
        for i in range(2):
            npc = NPC()
            npc_group.add(npc)
            all_sprites.add(npc)



    ##################################################


    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_fuel_bar(screen, 5, 27, player.fuel)
    draw_lives(screen, WIDTH - 100, 5, player.lives,
               player_mini_img)

    pg.display.flip()
    ##################################################

pg.quit()


