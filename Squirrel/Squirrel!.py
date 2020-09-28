import pygame
import random
from pygame.locals import *
from random import randint

pygame.init()

sw = 800
sh = 600
screensize = [sw, sh]
screen = pygame.display.set_mode(screensize)
pygame.display.set_caption("Squirrel!")

clock = pygame.time.Clock()

white  = (255, 255, 255)
black  = (  0,   0,   0)
red    = (255,   0,   0)
green  = (  0, 255,   0)
blue   = (  0,   0, 255)
purple = (180,   0, 180)
yellow = (255, 255,   0)
brown =  (181, 101,  29)

class MonEl(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("monel.png")
        self.rect = self.image.get_rect()

class Squirrel(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Squirrel.png")
        self.rect = self.image.get_rect()
        self.direction = 1
        self.step = 0
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        
class Magic(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Magic.png")
        self.rect = self.image.get_rect()
        
def check_keys():
    global monel
    keys = pygame.key.get_pressed()
    if keys[K_RIGHT] and monel.rect.x + monel.rect.width < sw or keys[K_d] and monel.rect.x + monel.rect.width < sw:
        monel.rect.x += 10
    if keys[K_LEFT] and monel.rect.x > 5 or keys[K_a] and monel.rect.x > 5:
        monel.rect.x -= 10
    if keys[K_UP] and monel.rect.y > 5 or keys[K_w] and monel.rect.y > 5:
        monel.rect.y -= 10
    if keys[K_DOWN] and monel.rect.y + monel.rect.height < sh or keys[K_s] and monel.rect.y + monel.rect.height < sh:
        monel.rect.y += 10

monel = MonEl()
monel.rect.x = 400
monel.rect.y = 520

allsprites = pygame.sprite.Group()
allsprites.add(monel)

magics = pygame.sprite.Group()
enemies = pygame.sprite.Group()
squirrels = pygame.sprite.Group()

bark = pygame.mixer.Sound("Bark.wav")
death = pygame.mixer.Sound("pac_die.wav")
yay = pygame.mixer.Sound("cheer.wav")

dead = False
done = False
over = False
start = False
win = False
score = 0
  
while not start:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = True
    if keys[K_SPACE]:
        start = True
        
    screen.fill(black)
    bg = pygame.image.load("Startback.png")
    screen.blit(bg, [400, 0])
    
    font = pygame.font.Font(None, 40)
    text = font.render("Press 'Space' to begin", True, white)
    screen.blit(text, [150, 305])
    
    font = pygame.font.Font(None, 80)
    message = font.render("Squirrels!", True, white)
    screen.blit(message, [150, 250])
    
    pygame.display.flip()
    clock.tick(20)

while not done:
    # 1. Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    check_keys()
    # 2. Program logic, change variables, etc.
    collidelist = pygame.sprite.spritecollide(monel, squirrels, True)
    for squirrel in collidelist:
        allsprites.remove(squirrel)
        score = score + 1
        bark.play()
        
    chance = randint(1, 20)
    if chance <= 2:
        squirrel = Squirrel()
        squirrel.rect.x = randint(0, sw)
        squirrel.rect.y = randint(0, sh)
        squirrels.add(squirrel)
        allsprites.add(squirrel)
        
    for squirrel in squirrels:
        if squirrel.direction == 1:
            squirrel.rect.x -= 5
            squirrel.step += 1
        elif squirrel.direction == 2:
            squirrel.rect.x += 5
            squirrel.step += 1
        elif squirrel.direction == 3:
            squirrel.rect.y += 5
            squirrel.step += 1
        elif squirrel.direction == 4:
            squirrel.rect.y -= 5
            squirrel.step += 1
        if squirrel.step >= random.randint(10,15):
            squirrel.step = 0
            squirrel.direction = random.randint(1,4) 
            
    badlist = pygame.sprite.spritecollide(monel, enemies, True)
    for enemy in badlist:
        death.play()
        allsprites.remove(monel)
        done = True
        dead = True
        
    if score >=20:
        chance = random.randint(0, 100)
        if chance == 1:
            enemy = Enemy()
            enemy.rect.x = randint(0, sw)
            enemy.rect.y = randint(0, sh)
            enemies.add(enemy)
            allsprites.add(enemy)
            
    for enemy in enemies:
        if monel.rect.x > enemy.rect.x:
            enemy.rect.x += 3
        elif monel.rect.x < enemy.rect.x:
            enemy.rect.x -= 3
        
        if monel.rect.y > enemy.rect.y:
            enemy.rect.y += 3
        elif monel.rect.y < enemy.rect.y:
            enemy.rect.y -= 3
                
    goodlist = pygame.sprite.spritecollide(monel, magics, True)
    for magic in goodlist:
        yay.play()
        done = True
        win = True
        
    if score >=30:
        chance = random.randint(0, 1000)
        if chance == 1:
            magic = Magic()
            magic.rect.x = random.randint(0, sw)
            magic.rect.y = random.randint(0, sh)
            magics.add(magic)
            allsprites.add(magic)
    if score >=40:
        chance = random.randint(0, 1000)
        if chance <= 5:
            magic = Magic()
            magic.rect.x = random.randint(0, sw)
            magic.rect.y = random.randint(0, sh)
            magics.add(magic)
            allsprites.add(magic)
    for magic in magics:
        if monel.rect.x > magic.rect.x and magic.rect.x > 5:
            magic.rect.x -= 6
        elif monel.rect.x < magic.rect.x and magic.rect.x + magic.rect.width < sw :
            magic.rect.x += 6
        
        if monel.rect.y > magic.rect.y and magic.rect.y > 5:
            magic.rect.y -= 6
        elif monel.rect.y < magic.rect.y and magic.rect.y + magic.rect.height < sh:
            magic.rect.y += 6

    # 3. Draw stuff
    screen.fill(white)
    bg = pygame.image.load("Background.jpg")
    screen.blit(bg, [0, 0])
    
    allsprites.draw(screen)
    
    pygame.draw.rect(screen, black, [0, 0, 130, 30], 0)
    
    font = pygame.font.Font(None, 30)
    text = font.render("Squirrels: %d" % score, True, white)
    screen.blit(text, [0, 5])
    
    pygame.display.flip()
    clock.tick(20)
        
while dead and not over:
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            over = True
    if keys[K_ESCAPE]:
        over = True
        
    if keys[K_SPACE]:
        done = False
        dead = False

    screen.fill(black)
     
    font = pygame.font.Font(None, 40)
    text = font.render("press 'esc' to quit", True, white)
    screen.blit(text, [275, 330])
    
    font = pygame.font.Font(None, 40)
    text = font.render("Squirrels: %d" % score, True, white)
    screen.blit(text, [300, 305])
    
    font = pygame.font.Font(None, 80)
    message = font.render("A rabbid Squirrel killed you", True, red)
    screen.blit(message, [35, 250])
    
    pygame.display.flip()
    clock.tick(20)
        
while win and not over:
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            over = True
    if keys[K_ESCAPE]:
        over = True

    screen.fill(white)
    
    font = pygame.font.Font(None, 30)
    text = font.render("Squirrels: %d" % score, True, black)
    screen.blit(text, [330, 330])
     
    font = pygame.font.Font(None, 40)
    text = font.render("The squirrels worship you", True, yellow)
    screen.blit(text, [220, 305])
    
    font = pygame.font.Font(None, 80)
    message = font.render("You caught the magic squirrel", True, purple)
    screen.blit(message, [1, 250])
    
    pygame.display.flip()
    clock.tick(20)

pygame.quit()
