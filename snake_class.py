import pygame, random, sys
from pygame.locals import *

import numpy as np
import math as m
import random
from apple_class import *

class snake():

    def __init__(self, height, width, size):
        self.pos_snake_X = [int(height / 2), int(height / 2), int(height / 2)]
        self.pos_snake_Y = [int(height / 2), int(height / 2), int(height / 2)]
        self.size_snake = size
        self.randomize_movement = [1, 1]
        self.up = [0, 0, 0, 1]
        self.down = [0, 0, 1, 0]
        self.right = [0, 1, 0, 0]
        self.left = [1, 0, 0, 0]
        self.dir = [0, 0, 0, 1]
        self.action = []
        self.snake_image = pygame.Surface((size, size))
        self.colour_snake = (0, 0, 0)
        self.snake_image.fill(self.colour_snake)


    def move_snake(self, screen, DNN_model, apple):
        if self.randomize_movement == [0, 0]:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.action = self.left.copy()

                    elif event.key == pygame.K_RIGHT:
                        self.action = self.right.copy()

                    elif event.key == pygame.K_UP:
                        self.action = self.up.copy()

                    elif event.key == pygame.K_DOWN:
                        self.action = self.down.copy()
                else:
                    pass


        if self.dir == self.up and (self.action == self.left or self.right):
            if self.action == self.left:
                self.pos_snake_X[0] -= 20
                self.dir = [1, 0, 0, 0]
            elif self.action == self.right:
                self.pos_snake_X[0] += 20
                self.dir = [0, 1, 0, 0]
            else:
                self.pos_snake_Y[0] -= 20
                self.dir = [0, 0, 0, 1]

        elif self.dir == self.down and (self.action == self.left or self.right):
            if self.action == self.left:
                self.pos_snake_X[0] -= 20
                self.dir = [1, 0, 0, 0]
            elif self.action == self.right:
                self.pos_snake_X[0] += 20
                self.dir = [0, 1, 0, 0]
            else:
                self.pos_snake_Y[0] += 20
                self.dir = [0, 0, 1, 0]

        elif self.dir == self.right and (self.action == self.up or self.down):
            if self.action == self.up:
                self.pos_snake_Y[0] -= 20
                self.dir = [0, 0, 0, 1]
            elif self.action == self.down:
                self.pos_snake_Y[0] += 20
                self.dir = [0, 0, 1, 0]
            else:
                self.pos_snake_X[0] += 20
                self.dir = [0, 1, 0, 0]

        elif self.dir == self.left and (self.action == self.up or self.down):
            if self.action == self.up:
                self.pos_snake_Y[0] -= 20
                self.dir = [0, 0, 0, 1]
            elif self.action == self.down:
                self.pos_snake_Y[0] += 20
                self.dir = [0, 0, 1, 0]
            else:
                self.pos_snake_X[0] -= 20
                self.dir = [1, 0, 0, 0]



        i = len(self.pos_snake_X) - 1
        # propogates x and y cordinates backwards
        while i >= 1:
            self.pos_snake_X[i] = self.pos_snake_X[i - 1]
            self.pos_snake_Y[i] = self.pos_snake_Y[i - 1]
            i -= 1

        self.draw_snake(screen)

    def draw_snake(self, screen):
        # print snake on the screen
        for i in range(0, len(self.pos_snake_X)):
            screen.blit(self.snake_image, (self.pos_snake_X[i], self.pos_snake_Y[i]))

    def collide(self, Object1x, Object2x, Object1y, Object2y, Object1Width, Object2Width, Object1Height, Object2Height):
        if Object1x + Object1Width > Object2x and Object1x < Object2x + Object2Width and Object1y + Object1Height > Object2y and Object1y < Object2y + Object2Height:
            return True
        else:
            return False

    def eat_apple(self, apple):
        if self.collide(self.pos_snake_X[0], apple.pos_apple_X, self.pos_snake_Y[0], apple.pos_apple_Y, 20, 20, 20, 20):
            self.pos_snake_X.append(700)
            self.pos_snake_Y.append(700)

            return True
        else:
            return False

    def collide_self_wall(self, height, width):
        SnakeX = self.pos_snake_X[0]
        SnakeY = self.pos_snake_Y[0]
        # collided with itself
        i = len(self.pos_snake_X) - 1
        collided_w_itself = False
        while i >= 2:
            if self.collide(SnakeX, self.pos_snake_X[i], SnakeY, self.pos_snake_Y[i],
                            self.size_snake, self.size_snake, self.size_snake, self.size_snake):
                return (True)
            i -= 1

        # collide with wall
        if (SnakeX < 0 or SnakeX > height or SnakeY < 0 or SnakeY > width):
            return (True)
        return False

    def reset(self, screen, height):
        self.pos_snake_X = [int(height / 2), int(height / 2), int(height / 2)]
        self.pos_snake_Y = [int(height / 2), int(height / 2), int(height / 2)]
        for i in range(0, len(self.pos_snake_X)):
            screen.blit(self.snake_image, (self.pos_snake_X[i], self.pos_snake_Y[i]))