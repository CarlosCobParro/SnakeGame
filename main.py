import pygame, random, sys
from pygame.locals import *

import numpy as np
import math as m
from canvas import *
from snake_class import *

if __name__ == '__main__':
    pygame.init()
    background=canvas()
    while (True):
        background.background()