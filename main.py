from random import randrange, choice
import random

import pygame
from pygame.font import SysFont
from pygame.locals import *
from pygame.mixer import Sound, music

from sprites import *
from utils import *


class Game:
    
    def __init__(self):
        
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT), FULLSCREEN)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        pygame.time.set_timer(USEREVENT, 500)
        pygame.time.set_timer(USEREVENT + 1 , 1000)
        self.font = SysFont("sans", 16)
        self.font2 = SysFont("sans", 48 , True, False)
        # self.bg60 = BackgroundLayer(pygame.image.load("assets/bg60.png").convert_alpha())
        self.bg1 = pygame.transform.scale(pygame.image.load("assets/parallax-space-background.png").convert(), (WIDTH, HEIGHT))
        bg2 = pygame.image.load("assets/parallax-space-stars.png").convert_alpha()
        bg3 = pygame.image.load("assets/parallax-space-far-planets.png").convert_alpha()
        self.bg2 = BackgroundLayer(pygame.transform.scale(bg2, (WIDTH, HEIGHT)))
        self.bg3 = BackgroundLayer(pygame.transform.scale(bg3, (WIDTH, HEIGHT)))
        self.imgSpeed = pygame.image.load("assets/arrowUp.png").convert_alpha()
        self.imgSlow = pygame.image.load("assets/arrowDown.png").convert_alpha()
        self.imgMap = pygame.image.load("assets/question.png").convert_alpha()
        self.platTexture = pygame.image.load("assets/platBlock.png").convert_alpha()
        self.go_sound = Sound("assets/gameover.wav")
        self.go_sound.set_volume(0.15)
        self.faster_sound = Sound("assets/tFTFaster.ogg")
        self.faster_sound.set_volume(0.15)
        pygame.mixer.music.load("assets/alphacentauri.ogg")
        pygame.mixer.music.set_volume(1.0)
        self.running = True
        self.run()
    
    def run(self):
        
        self.reset()
        
        timer = 0
        while self.running:
            self.dt = float(self.clock.tick(FPS) / 1000)
            timer += self.dt
            if timer >= (60 / 1000):
                timer = 0
                self.events()
                self.update()
            self.render()
            
        pygame.quit()
        
    def events(self):
        
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == USEREVENT:
                self.fpsText = "FPS : " + str(int(self.clock.get_fps()))
                self.fpsLabel = self.font.render(self.fpsText, True, WHITE)
                # self.platText = "Loaded platforms : " + str(len(self.platforms.sprites()))
                # self.platLabel = self.font.render(self.platText, True, WHITE)
            elif event.type == USEREVENT + 1:
                self.speedtimer += 1
                if self.speedtimer >= 12:
                    self.speedtimer = 0
                    self.faster_sound.play()
                    self.gamespeed += 0.1
                self.seconds += 1
                if self.seconds >= 60:
                    self.minutes += 1
                    self.seconds = 0
                self.timeText = str(self.minutes) + " : " + str(self.seconds)
                self.timeLabel = self.font2.render(self.timeText, True, WHITE)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                
    def update(self):
        
        self.camera.update(self.player)
        # self.bg60.update(0.6,self.gamespeed)
        self.bg2.update(0.6, self.gamespeed)
        self.bg3.update(0.9, self.gamespeed)
        self.sprites.update()
        hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            if (self.player.color != hits[0].color) and (hits[0].color != WHITE):
                self.game_over()
            self.player.pos.y = hits[0].rect.top
            self.player.vel.y = 0
            self.player.onGround = True
        else :
            self.player.onGround = False
        if self.player.rect.top > HEIGHT:
            self.game_over()
        hitsitems = pygame.sprite.spritecollide(self.player, self.items, False)
        if hitsitems : 
            if hitsitems[0].type == "speed":
                self.gamespeed += 0.1
                self.faster_sound.play()
                hitsitems[0].kill()
            if hitsitems[0].type == "slow":
                self.gamespeed -= 0.1
                hitsitems[0].kill()
        for platform in self.platforms:
            if self.camera.apply(platform).right <= 0:
                platform.kill()
        for item in self.items:
            if self.camera.apply(item).right <= 0:
                item.kill()
                    
        # Generation de plateformes 
        self.pgapx = 100 * self.gamespeed
        self.scroll = self.camera.apply(self.platforms.sprites()[len(self.platforms.sprites()) - 1]).right
        if (len(self.platforms.sprites()) < 7):
            color = random.choice([RED, GREEN, BLUE, WHITE])
            width = randrange(200, 600) * self.gamespeed
            yoffset = choice([-48, 0, 48])
            item = randrange(0, 10)
            self.currentp = Platform(self.currentplatx + self.pgapx, HEIGHT - 100 + yoffset, width, 48, color, self.platTexture)
            self.platforms.add(self.currentp)
            
            if item == 6:
                itemtype = random.choice(["speed", "slow", "map"])
                try:
                    if itemtype == "speed":
                        self.items.add(Item(self.currentplatx + 100 + randrange(0, self.currentplatx - 100), self.currentp.rect.top - 225, "speed", self.imgSpeed))
                    elif itemtype == "slow":
                        self.items.add(Item(self.currentplatx + 100 + randrange(0, self.currentplatx - 100), self.currentp.rect.top - 225, "slow", self.imgSlow))
                    elif itemtype == "map":
                        self.items.add(Item(self.currentplatx + 100 + randrange(0, self.currentplatx - 100), self.currentp.rect.top - 225, "slow", self.imgMap))
                except:
                    pass
            self.currentplatx = self.currentp.rect.right + self.pgapx
            
    def render(self):
        
        self.display.fill(BLACK)
        # self.bg60.draw(self.display)
        self.display.blit(self.bg1, self.bg1.get_rect())
        self.bg2.draw(self.display)
        self.bg3.draw(self.display)
        for p in self.platforms:
            self.display.blit(p.image, self.camera.apply(p))
        for s in self.sprites:
            self.display.blit(s.image, self.camera.apply(s))
        
        for i in self.items:
            self.display.blit(i.image, self.camera.apply(i))
        try :
            self.display.blit(self.fpsLabel, self.fpsLabel.get_rect())
            timeRect = self.timeLabel.get_rect()
            self.display.blit(self.timeLabel, Rect(75 - (timeRect.width / 2), 35, timeRect.width, timeRect.height))
        except :
            pass
        pygame.display.flip()
    
    def reset(self):
        
        self.gamespeed = 0.8
        self.speedtimer = 0
        self.pgapx = 100
        self.sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        p = Platform(100, HEIGHT - 100, 1000, 48, WHITE, self.platTexture)
        self.currentplatx = 1100
        self.platforms.add(p)
        self.player = Player(100, 100, self)
        self.sprites.add(self.player)
        self.camera = Camera(Camera.follow_camera, WIDTH, HEIGHT)
        pygame.mixer.music.play(loops=-1, start=0.0)
        self.seconds = 0
        self.minutes = 0
        self.displayMap = False;
    
    def game_over(self):
        self.go_sound.play()
        # pygame.time.delay(5000)
        self.reset()
        
game = Game()
