from random import randrange, choice
import random

import pygame
from pygame.locals import *

from pygame.font import SysFont
from pygame.mixer import Sound, music
from sprites import *
from utils import *
from tkinter import *


class Game:

    def __init__(self,width,height,fs,white,colors):

        self.width = width
        self.height = height
        self.white_platforms = white
        self.resolution = (self.width,self.height)
        self.colors = colors

        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        if fs :
            self.display = pygame.display.set_mode(self.resolution,FULLSCREEN)
        else :
            self.display = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        pygame.time.set_timer(USEREVENT, 500)
        pygame.time.set_timer(USEREVENT + 1, 1000)
        self.font = SysFont("sans", 16)
        self.font2 = SysFont("sans", 48, True, False)
        self.manager = ResourcesManager("assets")
        self.bg1 = self.manager.load_image("parallax-space-background.png",False,self.resolution)
        self.bg2 = BackgroundLayer(self.manager.load_image("parallax-space-stars.png",True,self.resolution))
        self.bg3 = BackgroundLayer(self.manager.load_image("parallax-space-far-planets.png",True,self.resolution))
        self.imgSpeed = self.manager.load_image("arrowUp.png",True)
        self.imgSlow = self.manager.load_image("arrowDown.png",True)
        self.imgMap = self.manager.load_image("question.png",True)
        self.platTexture = self.manager.load_image("platBlock.png",True)
        self.go_sound = self.manager.load_sound("gameover.wav")
        self.go_sound.set_volume(0.15)
        self.faster_sound = self.manager.load_sound("tFTFaster.ogg")
        self.faster_sound.set_volume(0.15)
        pygame.mixer.music.load(os.path.join("assets","alphacentauri.ogg"))
        pygame.mixer.music.set_volume(1.0)
        self.running = True
        self.run()

    def run(self):

        self.reset()

        timer = 0
        while self.running:
            self.dt = float(self.clock.tick(FPS) / 1000)
            timer += self.dt
            if timer >= (1 / 190):
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
                if self.displayMap :
                    self.mapTimer -= 1
                    if self.mapTimer <= 0 :
                        self.mapTimer = 0
                        self.displayMap = False
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
        else:
            self.player.onGround = False
        if self.player.rect.top > self.height:
            self.game_over()
        hitsitems = pygame.sprite.spritecollide(self.player, self.items, False)
        if hitsitems:
            if hitsitems[0].type == "speed":
                self.gamespeed += 0.1
                self.faster_sound.play()
                hitsitems[0].kill()
            if hitsitems[0].type == "slow":
                self.gamespeed -= 0.1
                hitsitems[0].kill()
            if hitsitems[0].type == "map":
                self.displayMap = True
                self.mapTimer = 15
                hitsitems[0].kill()
        for platform in self.platforms:
            if self.camera.apply(platform).right <= 0:
                platform.kill()
        for item in self.items:
            if self.camera.apply(item).right <= 0:
                item.kill()

        # Generation de plateformes
        self.pgapx = 100 * self.gamespeed
        self.scroll = self.camera.apply(self.platforms.sprites()[
                                        len(self.platforms.sprites()) - 1]).right
        if (len(self.platforms.sprites()) < 7):
            if self.white_platforms : 
                color = random.choice(self.colors + [WHITE])
            else :
                color = random.choice(self.colors)
            width = randrange(200, 600) + (self.gamespeed * 50)
            yoffset = choice([-48, 0, 48])
            item = randrange(0, 10)
            self.currentp = Platform(self.currentplatx + self.pgapx,
                                     self.height - 100 + yoffset, width, 48, color, self.platTexture)
            self.platforms.add(self.currentp)

            if item == 6:
                itemtype = random.choice(["speed", "slow", "map"])
                try:
                    if itemtype == "speed":
                        self.items.add(Item(self.currentplatx + 100 + randrange(
                            0, self.currentplatx - 100), self.currentp.rect.top - 225, "speed", self.imgSpeed))
                    elif itemtype == "slow":
                        self.items.add(Item(self.currentplatx + 100 + randrange(
                            0, self.currentplatx - 100), self.currentp.rect.top - 225, "slow", self.imgSlow))
                    elif itemtype == "map":
                        self.items.add(Item(self.currentplatx + 100 + randrange(
                            0, self.currentplatx - 100), self.currentp.rect.top - 225, "map", self.imgMap))
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
        try:
            self.display.blit(self.fpsLabel, self.fpsLabel.get_rect())
            timeRect = self.timeLabel.get_rect()
            self.display.blit(self.timeLabel, Rect(
                75 - (timeRect.width / 2), 35, timeRect.width, timeRect.height))
            n = 0
            for i in self.platforms :
                n += 1
                if n < 7:
                    img = Surface((32,32))
                    img.fill(i.color)
                    self.display.blit(img,Rect(100 + n*48,200,32,32))
                
        except:
            pass
        pygame.display.flip()

    def reset(self):

        self.gamespeed = 2.5
        self.speedtimer = 0
        self.pgapx = 100
        self.sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        p = Platform(100, self.height - 100, 1000, 48, WHITE, self.platTexture)
        self.currentplatx = 1100 + (100 * self.gamespeed)
        self.platforms.add(p)
        self.player = Player(100, self.height - 150, self)
        self.sprites.add(self.player)
        self.camera = Camera(self, Camera.follow_camera, self.width, self.height)
        pygame.mixer.music.play(loops=-1, start=0.0)
        self.seconds = 0
        self.minutes = 0
        self.displayMap = False
        
    def game_over(self):
        self.go_sound.play()
        # pygame.time.delay(5000)
        self.reset()



class SettingsFrame():

    def hex_to_rgb(self,hex):

        hex = hex.lstrip('#')
        lv = len(hex)
        return tuple(int(hex[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    def launch_game(self):
        self.win.destroy()
        colors = []
        print(self.color1.get(),",",self.color2.get(),",",self.color3.get())
        if self.color1.get() :
            colors.append(self.hex_to_rgb(self.color1text.get()))
        if self.color2.get() :
            colors.append(self.hex_to_rgb(self.color2text.get()))
        if self.color3.get() :
            colors.append(self.hex_to_rgb(self.color3text.get()))
        game = Game(int(self.width.get()),int(self.height.get()),self.fs.get(),self.white.get(),colors)
        
        

    def __init__(self) :

        self.win = Tk()
        self.win.title("Configuration")
        self.labelR = Label(self.win,text = "Resolution : ")
        self.labelR.grid(row =0,column = 0)
        self.width = StringVar()
        self.height = StringVar()
        self.wField = Entry(self.win,textvariable = self.width,width = 6).grid(row = 0,column = 1)
        self.xLabel = Label(self.win,text = "x").grid(row = 0,column = 2)
        self.hField = Entry(self.win,textvariable = self.height,width = 6).grid(row = 0,column = 3)
        self.fs = BooleanVar()
        self.fButton = Checkbutton(self.win,text = "Fullscreen",variable= self.fs,command = self.fs.set(True)).grid(row = 1,column = 0)
        self.white = BooleanVar()
        self.whiteButton = Checkbutton(self.win,text = "Plateformes blanches",variable= self.white,command = self.white.set(True)).grid(row = 1,column = 1)
        self.button_play = Button(self.win,text = "Jouer",command = lambda : self.launch_game())
        self.color1 = BooleanVar()
        self.color1button = Checkbutton(self.win,text="Couleur 1",variable = self.color1,command = self.color1.set(True)).grid(row = 2,column = 0)
        self.color2 = BooleanVar()
        self.color2button = Checkbutton(self.win,text="Couleur 2",variable = self.color2,command = self.color2.set(True)).grid(row = 3,column = 0)
        self.color3 = BooleanVar()
        self.color1text = StringVar()
        self.color2text = StringVar()
        self.color3text = StringVar()
        self.color3button = Checkbutton(self.win,text="Couleur 3",variable = self.color3,command = self.color3.set(True)).grid(row = 4,column = 0)
        self.color1Field = Entry(self.win,textvariable = self.color1text,width = 6).grid(row = 2,column = 1)
        self.color2Field = Entry(self.win,textvariable = self.color2text,width = 6).grid(row = 3,column = 1)
        self.color3Field = Entry(self.win,textvariable = self.color3text,width = 6).grid(row = 4,column = 1)
        self.button_play.grid(columnspan = 4,sticky = S)
        self.win.mainloop()

   

conf = SettingsFrame()
