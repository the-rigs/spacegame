# Pygame template - skeleton for a new pygame project
import pygame
import random
import math
import sys
import spritesheet

vec = pygame.math.Vector2

WIDTH = 1000
HEIGHT = 800
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
NEON_GREEN = (11, 255, 1)
NEON_PURPLE = (254, 0, 246)
NEON_YELLOW = (253, 254, 1)
NEON_BLUE = (1, 30, 254)
NEON_PINK = (255, 110, 199)
colors = [NEON_BLUE, NEON_GREEN, NEON_PINK, NEON_PURPLE, NEON_YELLOW]
Level = 1
POWERUP_TIME = 5000
name = 'DAve'


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, BLACK, outline_rect, 2)

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y, Color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, Color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def create_mob():
    type = random.choice(['met', 'ali'])
    type = random.randrange(8)
    if type >= 1:
        m = MOB()
        all_sprites.add(m)
        mobs.add(m)
    else:
        m = MOB2(player)
        all_sprites.add(m)
        mobs2.add(m)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = 80
        self.height = 80
        self.image = pygame.Surface((self.width, self.height))
        self.image = pygame.image.load("images/green_ship.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.org_image = self.image.copy()
        self.angle = 0
        self.direction = pygame.Vector2(1, 0)
        self.rect = self.image.get_rect(center=(200, 200))
        # self.pos = pygame.Vector2(self.rect.center)
        x = WIDTH / 2
        y = HEIGHT / 8 * 7
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 300
        self.speedx = 0
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.health = 100
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        self.name = ''
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.acc = vec(0, 0)
        self.score = 0
        self.start_game = False
    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def update(self, dt):
        self.vel.x -= self.vel.x * .01
        self.vel.y -= self.vel.y * .01
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.angle += 7
        if keystate[pygame.K_RIGHT]:
            self.angle += -7
        if keystate[pygame.K_UP]:
            self.vel = vec(2, 0).rotate(-self.angle) * .15
        if keystate[pygame.K_DOWN]:
            self.vel = vec(-2 / 2, 0).rotate(-self.angle) * .15
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                self.angle_change = 0
        if keystate[pygame.K_SPACE]:
            self.shoot()
        ####### Creating walls for player
        if self.pos.x > WIDTH + self.width / 2:
            self.pos.x = 0
        if self.pos.x < 0 - self.width / 2:
            self.pos.x = WIDTH + self.width / 2 - 5
        if self.pos.y < 0 - self.height:
            self.pos.y = HEIGHT + self.height
        if self.pos.y > HEIGHT + self.height:
            self.pos.y = 0 - self.height
        self.pos += self.vel * dt
        self.direction = pygame.Vector2(1, 0).rotate(-self.angle)
        self.image = pygame.transform.rotate(self.org_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.center = self.pos

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.center, self.direction.normalize())
                all_sprites.add(bullet)
                bullets.add(bullet)
            if self.power >= 2:
                bullet2 = Bullet((self.rect.left, self.rect.centery), self.direction.normalize())
                bullet3 = Bullet((self.rect.right, self.rect.centery), self.direction.normalize())
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                bullets.add(bullet2)
                bullets.add(bullet3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        pygame.sprite.Sprite.__init__(self)
        self.width = 12
        self.height = 12
        self.image = pygame.Surface((self.width, self.height))
        bullet_img = pygame.image.load('images/bullet.png')
        bullet_img = pygame.transform.scale(bullet_img, (self.width, self.height))
        self.image = bullet_img
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction
        self.pos = pygame.Vector2(self.rect.center)

    def update(self, dt):
        self.pos += self.direction * dt
        self.rect.center = self.pos

class Bullet2(pygame.sprite.Sprite):
    def __init__(self, x, y, targetx, targety):
        pygame.sprite.Sprite.__init__(self)
        self.width = 12
        self.height = 12
        self.image = pygame.Surface((self.width, self.height))
        bullet_img = pygame.image.load('images/bullet.png')
        bullet_img = pygame.transform.scale(bullet_img, (self.width, self.height))
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.speed = 10
        angle = math.atan2(targety - y, targetx - x)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def update(self, dt):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

class MOB2(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.width = 60
        self.height = 60
        self.player = player
        self.pick = random.choice(aliens)
        self.image = self.pick
        # self.image= pygame.Surface((self.width,self.height))
        # self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH, WIDTH + 500)
        self.rect.y = random.randrange(0, HEIGHT - self.height)
        self.speedx = random.randrange(5, 15)
        self.shoot_range = random.randrange(50, 300)
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 1000

    def update(self, dt):
        self.rect.x -= self.speedx
        if self.rect.right < 0:
            self.rect.x = random.randrange(WIDTH, WIDTH + 500)
            self.rect.y = random.randrange(0, HEIGHT - self.height)
            self.speedx = random.randrange(5, 15)
        if self.rect.bottom > self.shoot_range:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                bullet4 = Bullet2(self.rect.x, self.rect.y, self.player.rect.x, self.player.rect.y)
                all_sprites.add(bullet4)
                bullets2.add(bullet4)

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = 80
        self.height = 100
        self.image = boss
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.y = -40
        self.speedx = random.randrange(10, 25)
        self.speedy = 4
        self.first = True
        self.shoot_range = random.randrange(50, 300)
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 1000
        self.health = 100

    def update(self, dt):
        if self.rect.top < 265 and self.first:
            self.rect.y += self.speedy
        if self.rect.top >= 265 and self.first:
            self.speedy *= -1
            self.first = False
        if self.rect.top >= 80 and self.first == False:
            self.rect.y += self.speedy
        if self.rect.top < 80 and self.first == False:
            self.speedy = 0
            self.rect.x += self.speedx
        if self.rect.right >= WIDTH:
            self.speedx *= -1
        if self.rect.left <= 0:
            self.speedx *= -1
        if self.health <= 0:
            self.kill()

class Mother(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = 150
        self.height = 100
        self.image = mother
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.y = -100
        self.speedy = 4

    def update(self, dt):
        self.rect.y += self.speedy
        if self.rect.top > 200:
            self.speedy = -4
        if b.health <= 0:
            self.kill()

class MOB(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = random.randrange(25, 100, 5)
        self.height = self.width
        self.frame = 0
        self.framex = 0
        self.framey = 0
        self.r_list = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
        self.load_images()
        mob_img = self.r_list[0][0]
        self.image = mob_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.width)
        self.rect.y = random.randrange(-500, -100)
        self.speedy = random.randrange(3, 7)
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = random.randrange(100, 150)

    def load_images(self):
        size_ran = random.randrange(2, 8)
        divide = random.randrange(4, 8)
        size = size_ran / divide
        for x in range(8):
            for y in range(8):
                self.r_list[x][y] = (sprite_sheet.get_image(y, x, 128, 128, size, BLACK))

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.framex += 1
            if self.framex > 7:
                self.framex = 0
                self.framey += 1
            if self.framey > 7:
                self.framex = 0
                self.framey = 0
            center = self.rect.center
            self.image = self.r_list[self.framey][self.framex]
            self.rect = self.image.get_rect()
            self.rect.center = center

    def update(self, dt):
        self.animate()
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(0, WIDTH - self.width)
            self.rect.y = random.randrange(-500, -100)
            self.speedy = random.randrange(3, 7)

class Powerup(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['health', 'gun'])
        power_img = {}
        power_img['health'] = pygame.image.load('images/healthpoerup.png')
        power_img['gun'] = pygame.image.load('images/doublebullets.png')
        self.image = power_img[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self, dt):
        self.rect.y += self.speedy
        if self.rect.y > HEIGHT:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size, endgame=False):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.framex = 0
        self.framey = 0
        self.r_list = [[0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0]]
        self.load_images()
        mob_img = self.r_list[0][0]
        self.image = mob_img
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75
        self.stopgame = endgame
        self.going = True

    def load_images(self):
        for x in range(4):
            for y in range(4):
                self.r_list[x][y] = (sprite_sheet2.get_image(y, x, 64, 64, 1, BLACK))

    def animate(self):
        if self.going:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.framex += 1
                if self.framex > 3:
                    self.framex = 0
                    self.framey += 1
                if self.framey >= 3:
                    self.going = False
                    self.kill()
            center = self.rect.center
            self.image = self.r_list[self.framey][self.framex]
            self.rect = self.image.get_rect()
            self.rect.center = center

    def update(self, dt):
        self.animate()
# initialize pygame and create window
def start_screen():
    waiting = True
    mo = MOB()
    all_sprites.add(mo)
    mobs.add(mo)
    play = Player()
    all_sprites.add(play)
    play.image = pygame.transform.flip(play.image, False, True)
    play.rect.center = (80, -80)
    mo.rect.center = (80, -180)
    speedy = 10
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            keystate = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if keystate[pygame.K_SPACE]:
                    waiting = False
                    mo.kill()
                    play.kill()
                    player.start_game = True
                    # hs_entry()
                # if keystate[pygame.K_l]:
                #     waiting = False
                #     mo.kill()
                #     play.kill()
                #     hs_screen()
                if keystate[pygame.K_u]:
                    # waiting = False
                    mo.kill()
                    play.kill()
                    upgrades(player.score)
        # all_sprites.update()
        mo.rect.y += speedy
        play.rect.y += speedy
        if mo.rect.top > HEIGHT + 90:
            mo.rect.center = (WIDTH - 80, HEIGHT + 80)
            play.rect.center = (WIDTH - 80, HEIGHT + 180)
            speedy = -1 * speedy
            play.image = pygame.transform.flip(play.image, False, True)
        if play.rect.bottom < -180:
            mo.rect.center = (80, -180)
            play.rect.center = (80, -80)
            speedy = -1 * speedy
            play.image = pygame.transform.flip(play.image, False, True)
        # Draw / render
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        ### draw text on screen
        draw_text(screen, 'Starstorm', 64, WIDTH / 2, HEIGHT / 4, WHITE)
        draw_text(screen, 'Arrow Keys to Move and Space Bar to Shoot', 22, WIDTH / 2, HEIGHT / 2, WHITE)
        draw_text(screen, 'Press Space to Start', 22, WIDTH / 2, HEIGHT / 2 + 22, WHITE)
        # draw_text(screen, 'Press L for leaderboard', 22, WIDTH / 2, HEIGHT / 2 + 44, WHITE)
        draw_text(screen, 'Press U for UPGRADES', 22, WIDTH / 2, HEIGHT / 2 + 44, WHITE)

        # *after* drawing everything, flip the display
        pygame.display.flip()

def level_screen():
    # screen.blit(background, background_rect)
    draw_text(screen, 'Level ' + str(Level + 1), 64, WIDTH / 2, HEIGHT / 4, GREEN)
    draw_text(screen, 'Press A to Continue', 18, WIDTH / 2, HEIGHT * 3 / 4, GREEN)
    draw_text(screen, 'Press U for UPGRADES', 22, WIDTH / 2, HEIGHT * 3 / 4 + 44, WHITE)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            keystate = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if keystate[pygame.K_a]:
                    waiting = False
            if keystate[pygame.K_u]:
                waiting = False
                upgrades(player.score)

def boss_level_screen():
    screen.blit(background, background_rect)
    draw_text(screen, ' Boss Level', 64, WIDTH / 2, HEIGHT / 4, GREEN)
    draw_text(screen, 'Press A to Continue', 18, WIDTH / 2, HEIGHT * 3 / 4, GREEN)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            keystate = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if keystate[pygame.K_a]:
                    waiting = False

def lose_screen(score):
    screen.blit(background, background_rect)
    draw_text(screen, 'Sorry You Lost', 64, WIDTH / 2, HEIGHT / 4, WHITE)
    draw_text(screen, 'Press M for menu', 32, WIDTH / 2, HEIGHT * 3 / 4, GREEN)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            keystate = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if keystate[pygame.K_m]:
                    waiting = False

def win_screen(score):
    screen.blit(background, background_rect)
    draw_text(screen, 'You Won', 64, WIDTH / 2, HEIGHT / 4, WHITE)
    draw_text(screen, 'Press M For menu', 32, WIDTH / 2, HEIGHT * 3 / 4, RED)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            keystate = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if keystate[pygame.K_m]:
                    waiting = False

def upgrades(score):
    screen.blit(background, background_rect)
    draw_text(screen, 'UPGRADES', 64, WIDTH / 2, HEIGHT/8, WHITE)
    draw_text(screen, 'Press b For back', 32, WIDTH/6, HEIGHT/8, RED)
    draw_text(screen, str(score), 32, WIDTH/6*5, HEIGHT/8, RED)

    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            keystate = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if keystate[pygame.K_b]:
                    if player.start_game:
                        start_screen()
                    else:
                        waiting = False

pygame.init()
# Groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
expl = pygame.sprite.Group()
bullets2 = pygame.sprite.Group()
powerups = pygame.sprite.Group()
mobs = pygame.sprite.Group()
mobs2 = pygame.sprite.Group()
bosss = pygame.sprite.Group()
##########

aliens = []
for i in range(1, 6):
    filename = 'images/ship{}.png'.format(i)
    img = pygame.image.load(filename)
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    aliens.append(img_lg)
background = pygame.image.load('images/galaxy.png')
boss = pygame.image.load('images/boss.png')
mother = pygame.image.load('images/mother.png')
ship1 = pygame.image.load('images/ship1.png')
ship2 = pygame.image.load('images/ship2.png')
ship3 = pygame.image.load('images/ship3.png')
ship4 = pygame.image.load('images/ship4.png')
ship5 = pygame.image.load('images/ship5.png')

player_mini_img = pygame.image.load('images/green_ship.png')
player_mini_img = pygame.transform.scale(player_mini_img, (30, 30))

background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()
# pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Game")
clock = pygame.time.Clock()

sprite_sheet_image = pygame.image.load('images/AsteroidAnimation.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
sprite_sheet_image2 = pygame.image.load('images/Explosion_sprite_sheet.png').convert_alpha()
sprite_sheet2 = spritesheet.SpriteSheet(sprite_sheet_image2)


the_end = False
level_score = 0
end_level = False
player = Player()
moth = Mother()
boss_alive = False
boss_level = 1
b_level = 0
winner = False
new_game = True
new_level = False
num_mob = 10
# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    dt = clock.tick(60)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False


    if new_game:
        start_screen()
        player = Player()
        all_sprites.add(player)
        # player.name = hs_entry()
        Level = 1
        boss_level = 1
        top = 80
        # level = 4
        dt = 0
        # level_rows = 4
        player.lives = 3
        num_mob = 10
        for i in range(num_mob):
            create_mob()
        powerup_percent = 15
        player.score = 0
        level_score = 0
        new_game = False
    if new_level:
        level_screen()
        Level += 1
        boss_level += 1
        level_score = 0
        num_mob +=5
        new_level = False
    if boss_level == 5:
        boss_level = 0
        boss_level_screen()
        for m in mobs:
            m.kill()
        for m in mobs2:
            m.kill()
        for e in expl:
            e.kill()
        for b1 in bullets:
            b1.kill()
        for p in powerups:
            p.kill()
        for b2 in bullets2:
            b2.kill()
        waiting = True
        all_sprites.add(moth)
        b = Boss()
        all_sprites.add(b)
        bosss.add(b)
        boss_alive = True

    hit_player = pygame.sprite.spritecollide(player, mobs, True)
    hit_player2 = pygame.sprite.spritecollide(player, bullets2, True)
    hit_player3 = pygame.sprite.spritecollide(player, mobs2, True)
    hit_player4 = pygame.sprite.spritecollide(player, bosss, True)
    hit_mobs = pygame.sprite.groupcollide(mobs, bullets, True, True)
    hit_mobs2 = pygame.sprite.groupcollide(mobs2, bullets, True, True)
    hit_mobs3 = pygame.sprite.groupcollide(mobs2, mobs, True, True)
    hit_mobs4 = pygame.sprite.groupcollide(mobs, bullets2, True, True)
    hit_powerups = pygame.sprite.spritecollide(player, powerups, True)

    for hit in hit_player:
        # damage to the player change later
        # insert small explosion
        explo = Explosion(player.rect.center, 'lg')
        all_sprites.add(explo)
        expl.add(explo)
        player.health -= 10
        create_mob()
    for hit in hit_player2:
        explo = Explosion(player.rect.center, 'lg')
        all_sprites.add(explo)
        expl.add(explo)
        player.health -= 5
    for hit in hit_player3:
        explo = Explosion(player.rect.center, 'lg')
        all_sprites.add(explo)
        expl.add(explo)
        player.health -= 20
        create_mob()
    for hit in hit_player4:
        player.health -= 5
    for hit in hit_mobs:
        player.score += 10
        level_score += 10
        explo = Explosion(hit.rect.center, 'lg')
        all_sprites.add(explo)
        expl.add(explo)
        create_mob()
        if random.randrange(100) <= powerup_percent:
            powerup = Powerup(hit.rect.center)
            all_sprites.add(powerup)
            powerups.add(powerup)
    for hit in hit_mobs2:
        player.score += 10
        level_score += 10
        explo = Explosion(hit.rect.center, 'lg')
        all_sprites.add(explo)
        expl.add(explo)
        create_mob()
        if random.randrange(100) <= powerup_percent:
            powerup = Powerup(hit.rect.center)
            all_sprites.add(powerup)
            powerups.add(powerup)
    for hit in hit_mobs3:
        explo = Explosion(hit.rect.center, 'lg')
        all_sprites.add(explo)
        expl.add(explo)
        create_mob()
        create_mob()
    for hit in hit_mobs4:
        explo = Explosion(hit.rect.center, 'lg')
        all_sprites.add(explo)
        expl.add(explo)
        create_mob()
    if boss_alive:
        hit_mobs5 = pygame.sprite.spritecollide(b, bullets, False)
        for hit in hit_mobs5:
            explo = Explosion(hit.rect.center, 'lg')
            all_sprites.add(explo)
            expl.add(explo)
            b.health -= 10
            if b.health <= 0:
                boss_alive = False
                b.kill()
                moth.kill()
                player.score += 50
                level_score += 50
                new_level = True
                for i in range(num_mob):
                    create_mob()
    if hit_powerups:
        for hit in hit_powerups:
            if hit.type == 'health':
                player.health += 100
                if player.health >= 100:
                    player.health = 100
            if hit.type == 'gun':
                player.powerup()
    if player.health <= 0:
        # player ship dies
        player.health = 100
        player.lives -= 1
        # when player loses a life put explosion in and then load player back into game.
    if player.lives == 0:
        # runnning = False
        new_game = True
        name = player.name
        player.kill()
        for m in mobs:
            m.kill()
        for m in mobs2:
            m.kill()
        for e in expl:
            e.kill()
        for b in bullets:
            b.kill()
        for p in powerups:
            p.kill()
        for b in bullets2:
            b.kill()

        the_end = True
    if level_score == 100:
        new_level = True
        level_score = 0
    if Level == 10 and boss_alive == False:
        win_screen(player.score)
        winner == True
        player.kill()
        for m in mobs:
            m.kill()
        for m in mobs2:
            m.kill()
        for e in expl:
            e.kill()
        for b in bullets:
            b.kill()
        for p in powerups:
            p.kill()
        for b in bullets2:
            b.kill()
        new_game = True

    # Update
    all_sprites.update(dt)
    # Draw / render
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    ### draw text on screen
    draw_text(screen, 'Level ' + str(Level), 32, WIDTH / 2 + 300, 10, GREEN)
    draw_text(screen, 'Score ' + str(player.score), 32, WIDTH / 2 - 300, 10, GREEN)
    draw_text(screen, 'Health ', 32, WIDTH / 2, 10, GREEN)
    draw_shield_bar(screen, WIDTH / 2 + 50, 20, player.health)
    draw_lives(screen, WIDTH - 100, 13, player.lives, player_mini_img)
    # *after* drawing everything, flip the display
    pygame.display.flip()
    if the_end:
        lose_screen(player.score)
        the_end = False

pygame.quit()
