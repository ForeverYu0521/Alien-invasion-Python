#-*-coding:utf-8-*-
import pygame
from pygame.sprite import Sprite
import random

class Tools(Sprite):
    def __init__(self, ai_settings, screen):
        super(Tools, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load("images/ToolsBullet.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        self.recty = float(-1 * self.rect.height)
        self.rect.x = random.randint(0,120) * 10 
        self.rect.y = self.recty

        self.bullet_flag = False
    def blitme(self):

        self.screen.blit(self.image, self.rect)

    def draw(self):
        if self.bullet_flag:
            self.recty += self.ai_settings.itemdrop
            self.rect.y = self.recty
