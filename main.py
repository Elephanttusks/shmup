import pygame
import random
from os import path
img_dir = path.join(path.dirname(__file__), 'img')
highscore_file = 'highscore.txt'

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# how many monsters?
print("")
print("Welcome to Shmupland!")
print("")
print("Arrow keys or WASD to move, hold Space to fire.")
print("")
print("After every 6 bullets you fire, you will have to wait 800 ticks to fire again.")
print("The exact length of that time depends on your FPS.")
print("")
print("You will gain points for every second you survive.")
print("")
print("You will gain points for every mob you kill.")
print("")
print("You will lose points for every bullet you fire.")
print("")
print("Your score will be multiplied by the number of mobs and FPS.")
print("")
monsters = "none yet"
while not monsters.isnumeric():
  monsters = input("How many mobs do you want? Pick something between 5 and 20. 10 is a good medium. ")

monsters = int(monsters)
while monsters < 5 or monsters > 20 :
  monsters = int(input("How many mobs do you want? Pick something between 5 and 20. 10 is a good medium. "))

WIDTH = 480
HEIGHT = 600
FPS = "none yet"
while not FPS.isnumeric():
   FPS =input("What FPS do you want? Pick something between 45 and 80. 60 is a good medium. ")
FPS = int(FPS)
while FPS < 45 or FPS > 80:
  FPS = int(input("What FPS do you want? Pick something between 45 and 80. 60 is a good medium. "))

# initialize pygame and create window
pygame.init()

name = input("What is your name?")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Grand Shmuppenation")
clock = pygame.time.Clock()


font_name = pygame.font.match_font('jua')
def draw_text(surf, text, size, x, y):
  font = pygame.font.Font(font_name, size)
  text_surface = font.render(text, True, WHITE)
  text_rect = text_surface.get_rect()
  text_rect.midtop = (x, y)
  surf.blit(text_surface, text_rect)

def newmob():
  m = Mob()
  all_sprites.add(m)
  mobs.add(m)

def draw_shield_bar(surf, x, y, pct):
  if pct < 0:
    pct = 0
  BAR_LENGTH = 100
  BAR_HEIGHT = 10
  fill = (pct/100) * BAR_LENGTH
  outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
  fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
  pygame.draw.rect(surf, GREEN, fill_rect)
  pygame.draw.rect(surf, WHITE, outline_rect, 2)

def show_go_screen():
  screen.blit(background, background_rect)
  draw_text(screen, "Welcome to Shmupland.", 60, WIDTH / 2, HEIGHT / 4)
  draw_text(screen, "Arrow keys or WASD to move, hold Space to fire.", 22, WIDTH / 2, HEIGHT / 2)
  draw_text(screen, "Press a key to begin your journey into the unknown.", 18, WIDTH / 2, HEIGHT *3 / 4)
  pygame.display.flip()
  if highscore > 0:
    print("")
    print("time alive:", seconds, "seconds")
    print("bullets fired:", player.bullet_number)
    print("mob score:", killed)
    print("Mobs:", monsters)
    print("FPS:", FPS)
    print("score:", score)
    print("your high score:", highscore)
    
  waiting = True
  while waiting:
    clock.tick(FPS)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
      if event.type == pygame.KEYUP:
        waiting = False

class Player(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.transform.scale(player_img, (50, 38))
    self.image.set_colorkey(BLACK)
    self.rect = self.image.get_rect()
    self.radius = 20
    self.rect.centerx = int(WIDTH / 2)
    self.rect.bottom = HEIGHT - 10
    self.speedx = 0
    self.shield = 100
    self.shoot_delay = 200
    self.reload = 800
    self.bullet_number = 0
    self.bullet_count = 0
    self.shootable = True
    self.now = pygame.time.get_ticks()
    self.last_shot = self.now

  def update(self):
    self.now = pygame.time.get_ticks()
    self.speedx = 0
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
      self.speedx = -8
    if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
      self.speedx = 8
    if keystate[pygame.K_SPACE]:
      self.shoot()
    self.rect.x += self.speedx
    if self.rect.right > WIDTH:
      self.rect.right = WIDTH
    if self.rect.left < 0:
      self.rect.left = 0
    if self.bullet_count >= 6:
      if self.now - self.last_shot < self.reload:
        self.shootable = False
      else:
        self.shootable = True
        self.bullet_count = 0
    else:
      if self.now - self.last_shot > self.shoot_delay:
        self.shootable = True
      else:
        self.shootable = False

  def shoot(self):
    if self.shootable:
      self.last_shot = self.now
      bullet = Bullet(self.rect.centerx, self.rect.top)
      all_sprites.add(bullet)
      bullets.add(bullet)
      self.bullet_number += 1
      self.bullet_count += 1

class Mob(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.image_orig = random.choice(meteor_images)
    self.image_orig.set_colorkey(BLACK)
    self.image = self.image_orig.copy()
    self.rect = self.image.get_rect()
    self.radius = int(self.rect.width*.85 / 2)
    self.rect.x = random.randrange(WIDTH - self.rect.width)
    self.rect.y = random.randrange(-100, -40)
    self.speedy = random.randrange(1, 8)
    self.speedx = random.randrange(-3, 3)
    self.rot = 0
    self.rot_speed = random.randrange(-8, 8)
    self.last_update = pygame.time.get_ticks()

  def update(self):
    self.rotate()
    self.rect.y += self.speedy
    self.rect.x += self.speedx
    if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
      self.rect.x = random.randrange(WIDTH - self.rect.width)
      self.rect.y = random.randrange(-100, -40)
      self.speedy = random.randrange(1, 8)
      self.speedx = random.randrange(-3, 3)
      self.image_orig = random.choice(meteor_images)

  def rotate(self):
    now = pygame.time.get_ticks()
    if now - self.last_update > 50:
      self.last_update = now
      self.rot = (self.rot + self.rot_speed) % 360
      new_image = pygame.transform.rotate(self.image_orig, self.rot)
      old_center = self.rect.center
      self.image = new_image
      self.rect = self.image.get_rect()
      self.rect.center = old_center

class Bullet(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.image = bullet_img
    self.image.set_colorkey(BLACK)
    self.rect = self.image.get_rect()
    self.rect.bottom = y
    self.rect.centerx = x
    self.speedy = -10

  def update(self):
    self.rect.y += self.speedy
    if self.rect.bottom <0:
      self.kill()

class Explosion(pygame.sprite.Sprite):
  def __init__(self, center, size):
    pygame.sprite.Sprite.__init__(self)
    self.size = size
    self.image = explosion_anim[self.size][0]
    self.rect = self.image.get_rect()
    self.rect.center = center
    self.frame = 0
    self.last_update = pygame.time.get_ticks()
    self.frame_rate = 50

  def update(self):
    now = pygame.time.get_ticks()
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

#load all game graphics
background = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
meteor_images = []
meteor_list =['meteorBrown_big1.png', 'meteorBrown_med1.png', 'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png', 'meteorBrown_tiny1.png']
for img in meteor_list:
  meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())
explosion_anim  ={}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['pl'] = []
for i in range(9):
  filename = 'regularExplosion0{}.png'.format(i)
  img = pygame.image.load(path.join(img_dir, filename)).convert()
  img.set_colorkey(BLACK)
  img_lg = pygame.transform.scale(img, (75, 75))
  explosion_anim['lg'].append(img_lg)
  img_sm = pygame.transform.scale(img, (32, 32))
  explosion_anim['sm'].append(img_sm)
  filename ='sonicExplosion0{}.png'.format(i)
  img = pygame.image.load(path.join(img_dir, filename)).convert()
  img.set_colorkey(BLACK)
  explosion_anim['pl'].append(img)

#Game loop
game_over = True
running = True
highscore = 0
while running:
  if game_over:
    show_go_screen()
    game_over = False
    # groups, variables, etc
    all_sprites = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    for i in range(monsters):
      newmob()
    time = 0
    seconds = 0
    killed = 0
    score = 0
    player.bullet_number = 0

  #keep loop running at the right speed
  clock.tick(FPS)
  #procces input(events)
  for event in pygame.event.get():
    #check for closing window
    if event.type == pygame.QUIT:
      running = False

  #update
  all_sprites.update()
  time += 1

  #check to see if a mob hit the player
  hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
  for hit in hits:
    player.shield -= hit.radius * 2
    expl = Explosion(hit.rect.center, 'sm')
    all_sprites.add(expl)
    newmob()
    if player.shield <= 0:
      death_explosion = Explosion(player.rect.center, 'pl')
      all_sprites.add(death_explosion)
      player.kill()
  # If the player died and the explosion is finished playing
  if not player.alive() and not death_explosion.alive():
    game_over = True

  #check to see if a bullet hit a mob
  hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
  for hit in hits:
    killed += 50 - hit.radius
    expl = Explosion(hit.rect.center, 'lg')
    all_sprites.add(expl)
    newmob()

  #analyze score
  if time % 60 == 0:
    seconds += 1
    score = int(seconds*(monsters*FPS/15) + killed/16 - player.bullet_number/10)
    if score > highscore:
      highscore = score
      allscore = (highscore_file, 'r')

      #allscore.split(",")

      with open(highscore_file, 'w') as f:
        f.write("something in quotes")


  #draw/render
  screen.fill(BLACK)
  screen.blit(background, background_rect)
  all_sprites.draw(screen)
  draw_text(screen, str(score), 18, WIDTH/2, 10)
  draw_shield_bar(screen, 5, 5, player.shield)
  draw_text(screen, str(6 - player.bullet_count), 20, WIDTH-50, 10)

  # *after* drawing everything, flip the display
  pygame.display.flip()

pygame.quit()
