import pygame
from pygame.math import Vector2
from pygame.rect import Rect

from utils import *


class Player(pygame.sprite.Sprite):
    
    def __init__(self, x, y , game):
        
        pygame.sprite.Sprite.__init__(self)
        self.colorLock = False
        self.game = game
        self.image = pygame.Surface((32, 56))
        texture = pygame.image.load("assets/kowalsky.png").convert_alpha()
        self.spritesheet = Spritesheet(texture)
        self.current_frame = 0
        self.last_update = 0
        self.animation = [self.spritesheet.get_region(i * 32, 0, 32, 56).convert_alpha() for i in range(0, int(self.spritesheet.image.get_rect().right / 32))]
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.pos = Vector2(x, y)
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)
        self.onGround = False
        self.colors = [BLUE, RED, GREEN]
        self.colorIndex = 0
        self.color = self.colors[self.colorIndex]
        
        
    def update(self):
        
        if not self.onGround :
            self.acc = Vector2(ACC * self.game.gamespeed, 0.5)
        else :
            self.acc = Vector2(ACC * self.game.gamespeed, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_c]:
            if not self.colorLock :
                self.colorIndex += 1
                if self.colorIndex > 2:
                    self.colorIndex = 0
            self.colorLock = True
        else : 
            self.colorLock = False
        if keys[pygame.K_v] and self.onGround:
            self.jump()
            
        self.color = self.colors[self.colorIndex]
        
        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        self.rect.midbottom = self.pos + Vector2(0, 1)
        self.update_animation()
        self.image = pygame.Surface((32, 56),pygame.SRCALPHA)
        self.image.fill(self.color)
        self.image.blit(source =self.animation[self.current_frame], dest=Rect(0,0,32,56))
        self.imageKey = pygame.Surface((32,56))
        self.imageKey.blit(self.image, (0,0))
        self.imageKey.set_colorkey(PINK)
        self.image = self.imageKey
        

    def update_animation(self):
        
        now = pygame.time.get_ticks()
        if not self.onGround : 
            self.current_frame = 2
        else : 
            if now - self.last_update > 75 / self.game.gamespeed :
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.animation)
        
    def jump(self):
        
        if self.onGround : 
            self.rect.y -= 1
            self.vel.y = -18

class Platform(pygame.sprite.Sprite):
    
    def __init__(self, x, y, width, height, color, texture):
        
        pygame.sprite.Sprite.__init__(self)
        self.image1 = pygame.Surface((width, height))
        self.image1.fill(color)
        for i in range(0, int(width / texture.get_rect().right + 1), 1):
            self.image1.blit(texture, Rect(i * texture.get_rect().right, 0, texture.get_rect().width, texture.get_rect().height))
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color

class Item(pygame.sprite.Sprite):
    
    def __init__(self, x, y, type, texture):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.image = texture
        self.rect = Rect(x, y, self.image.get_rect().width, self.image.get_rect().height)

class BackgroundLayer(pygame.sprite.Sprite):
    
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.bgimage = image
        self.bgWidth = self.bgimage.get_rect().right
        self.bgHeight = self.bgimage.get_rect().top
        self.x , self.x1 = 0, self.bgWidth
        self.y , self.y1 = 0, 0
        imgrect = self.bgimage.get_rect()
        self.image = pygame.Surface((imgrect.right * 2, imgrect.top))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
    
    def update(self, basespeed, gamespeed):
        
        self.x -= basespeed * gamespeed
        self.x1 -= basespeed * gamespeed
        if self.x < -self.bgWidth:
            self.x = self.bgWidth
        if self.x1 < -self.bgWidth:
            self.x1 = self.bgWidth
        self.rect = self.image.get_rect()
    
    def draw(self, display):
        
        display.blit(self.bgimage, Rect(self.x, self.y, self.bgWidth, self.bgHeight))
        display.blit(self.bgimage, Rect(self.x1, self.y1, self.bgWidth, self.bgHeight))
