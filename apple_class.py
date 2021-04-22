import pygame, random, sys
from pygame.locals import *

import numpy as np
import math as m

class apple():

    def __init__(self, pos_X, pos_Y, size):
        self.pos_apple_X = 40
        self.pos_apple_Y = 40

        self.apple_image = pygame.Surface((size, size))
        self.apple_image.fill((255,0,0)) #It is red, but the order numbers is RGB

    def pos_apple(self,height, width,size):

        self.pos_apple_X,self.pos_apple_Y = np.floor(random.randint(0, int((height-size) / size))) * size, \
                                            np.floor(random.randint(0, int((height-size) / size)) * size)
        #aparecer donde no esta la serpiente

        return self.pos_apple_X,self.pos_apple_Y

    def draw_apple(self,screen):
        screen.blit(self.apple_image, (self.pos_apple_X, self.pos_apple_Y))

