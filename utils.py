import pygame
from pygame import Surface
from pygame.constants import BLEND_RGBA_ADD, BLEND_RGBA_MULT

# Fonctions, classes et constantes utiles

TITLE = "Le meilleur jeu du monde (et le plus modeste)"
WIDTH = 1366
HEIGHT = 768
FPS = 90  # Le cap du framerate

ACC = 0.5
FRICTION = -0.12

# Quelques Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255,0,255) #COLORKEY
    
class Spritesheet:
    
    def __init__(self, file):
        
        #self.image = pygame.image.load(file).convert_alpha()
        self.image = file
    
    def get_region(self, x, y, width, height):
        
        rimage = pygame.Surface((width, height),pygame.SRCALPHA)
        rimage.blit(source=self.image, dest=(0, 0), area =(x, y, width, height))
        return rimage

class Camera(object):
    
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.rect.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move((int(self.state.left),int(self.state.top)))

    def update(self, target):
        self.state = self.camera_func(self ,self.state, target.rect)
    
    def follow_camera(self, camera, target_rect):
        l, _, _, _ = target_rect
        _, _, w, h = camera
        #return pygame.rect.Rect(int(-l + WIDTH / 2),int( -t + HEIGHT / 2),int(w),int(h))
        return pygame.rect.Rect(int(-l + WIDTH / 4),0,int(w),int(h))
        
        
