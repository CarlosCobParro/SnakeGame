import pygame, random, sys
from pygame.locals import *
from nn import neural_net
import numpy as np
import math as m


class SnakeGame():

    def __init__(self, epoch=10, batch_size=10, epsilon=1, gamma=.8):
        self.epoch = epoch
        self.batch_size = batch_size
        self.epsilon = epsilon
        self.gamma = gamma
        self.model = neural_net([16, 14])
        self.experience = []

    # Check to see if there is a collision with a wall/apple/neither between two objects
    def collide(self, Object1x, Object2x, Object1y, Object2y, Object1Width, Object2Width, Object1Height, Object2Height):
        if Object1x + Object1Width > Object2x and Object1x < Object2x + Object2Width and Object1y + Object1Height > Object2y and Object1y < Object2y + Object2Height:
            return True
        else:
            return False

    def die(self, screen, score):
        f = pygame.font.SysFont('Arial', 30)
        t = f.render('Your score was: ' + str(score), True, (0, 0, 0))
        screen.blit(t, (10, 270))
        pygame.display.update()
        pygame.time.wait(500)
        sys.exit(0)

    def getNewState(self, oldState, action, dirs=0):
        newState = oldState[:]
        if (action == 2 and dirs != 0):
            dirs = 2
        elif (action == 0 and dirs != 2):
            dirs = 0
        elif (action == 3 and dirs != 1):
            dirs = 3
        elif (action == 1 and dirs != 3):
            dirs = 1

        if (dirs == 0):
            newState[1] += 20
        elif (dirs == 1):
            newState[0] += 20
        elif (dirs == 2):
            newState[1] -= 20
        elif (dirs == 3):
            newState[0] -= 20
        return newState

    def getState(self):
        #print("Position cabeza: ", self.xs[0], self.ys[0])
        #print("position apple: ", self.applepos[0], self.applepos[1])
        #print("position head snake: ", self.xs[0], self.ys[0])
        return ([self.xs[0], self.ys[0], self.applepos[0], self.applepos[1]])

    def distance(self, state):
        SnakeX = state[0]
        SnakeY = state[1]
        AppleX = state[2]
        AppleY = state[3]
        d = m.sqrt(m.pow((AppleX - SnakeX), 2) + m.pow((AppleY - SnakeY), 2))
        return d

    def reward(self, oldState, action, dirs, state):
        #Si se enostia con ella o con el muro le hundes
        newState = self.getNewState(state, action, dirs)
        if (self.collide_self_wall(newState)):
            return -500
        # reward +10 if snake is closer to apple, -10 if snake is farther
        # and +100 if the snake gets the apple
        oldDistance = self.distance(oldState)
        newDistance = self.distance(newState)
        if (oldDistance > newDistance):
            if (newDistance == 0):
                return 100
            else:
                return 10
        elif (oldDistance < newDistance):
            return -10
        else:
            return 0  # same spot: Unlikely but for debugging purposes

    def collide_self_wall(self, state):
        SnakeX = state[0]
        SnakeY = state[1]
        # collided with itself
        i = len(self.xs) - 1
        collided_w_itself = False
        while i >= 2:
            if self.collide(SnakeX, self.xs[i], SnakeY, self.ys[i], 20, 20, 20, 20):
                return (True)
            i -= 1
        # collide with wall
        if (SnakeX < 0 or SnakeX > 290 or SnakeY < 0 or SnakeY > 290):
            return (True)
        return False

    def collectExperience(self, experience):
        self.experience.append(experience)

    def draw_screen(self, screen, green, light_green, Snake, score, appleimage, f,frame):

        screen.fill(light_green)
        for x in range(10, 290, 40):
            for y in range(10, 290, 40):
                pygame.draw.rect(screen, green, [x, y, 20, 20])

        # print the snake onto the screen
        for i in range(0, len(self.xs)):
            screen.blit(Snake, (self.xs[i], self.ys[i]))

        screen.blit(appleimage, self.applepos)
        t = f.render(str(score), True, (250, 250, 250))
        screen.blit(t, (10, 10))


        score_surf = f.render(str(frame), True, (250, 250, 250))
        score_pos = [100, 10]

        screen.blit(score_surf, score_pos)
        pygame.display.update()

    def action(self, action, dirs, match, model,frame):
        if (action == 2 and dirs != 0):
            dirs = 2
        elif (action == 0 and dirs != 2):
            dirs = 0
        elif (action == 3 and dirs != 1):
            dirs = 3
        elif (action == 1 and dirs != 3):
            dirs = 1

        # In this point is had to decide the direction of the snake, and there are two ways. The first one is random,
        # and the second is to go toward the apple
        # decide which direction the snake will go
        if ((random.random() < self.epsilon) and (frame < self.batch_size)):
        # During three apples you teach the system to eat apples
        #if self.score < 10 and match < 1:
            # in this point is possible to teach the system with the help of the user
            # pygame.display.set_mode()
            flag = True
            '''
            while flag == True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            action = 3  # down
                            flag = False
                            state, prediction = 0,0
                        elif event.key == pygame.K_RIGHT:
                            action = 1  # right
                            flag = False
                            state, prediction = 0,0
                        elif event.key == pygame.K_UP:
                            action = 2  # down
                            flag = False
                            state, prediction = 0,0
                        elif event.key == pygame.K_DOWN:
                            action = 0  # left
                            flag = False
                            state, prediction = 0,0

                '''
            state, prediction = 0, 0
            action = random.choice([0, 1, 2, 3])  # take a random direction
        else:
            # In this point the system can predict the next movement
            state = np.array(self.getState())
            prediction = model.predict(np.array([state])).flatten().tolist()
            #print("perdiction", prediction)
            action = prediction.index(max(prediction))

        return action, dirs, state, prediction

    def movement(self, dirs):
        i = len(self.xs) - 1
        # propogates x and y cordinates backwards
        while i >= 1:
            self.xs[i] = self.xs[i - 1]
            self.ys[i] = self.ys[i - 1]
            i -= 1

        # updates the co-ordinates of the head which will be propogated backwards
        # HEre is the snake movement
        # dir = 0 -> down
        # dir = 1 -> right
        # dir = 2 -> up
        # dir = 3 -> left
        if dirs == 0:
            self.ys[0] += 20
        elif dirs == 1:
            self.xs[0] += 20
        elif dirs == 2:
            self.ys[0] -= 20
        elif dirs == 3:
            self.xs[0] -= 20

    def eat_apple(self):
        if self.collide(self.xs[0], self.applepos[0], self.ys[0], self.applepos[1], 20, 10, 20, 10):
            self.score += 1
            self.xs.append(700)
            self.ys.append(700)
            self.applepos = (
                np.floor(random.randint(0, int(280 / 20))) * 20, np.floor(random.randint(0, int(280 / 20)) * 20))

    def hit_wall_itself(self, match):

        i = len(self.xs) - 1
        collided_w_itself = False
        while i >= 2:
            if self.collide(self.xs[0], self.xs[i], self.ys[0], self.ys[i], 20, 20, 20, 20):
                # die(screen, score)
                collided_w_itself = True
            i -= 1

        if collided_w_itself:
            # reset the game
            self.xs = [160, 160]
            self.ys = [160, 160]
            self.score = 0
            return match + 1

        if (self.xs[0] < 0 or self.xs[0] > 290 or self.ys[0] < 0 or self.ys[0] > 290):
            # die(screen, score)
            # reset the game to beginning
            self.xs = [160, 160]
            self.ys = [160, 160]
            self.score = 0
            return match + 1
        return match

    def init_game(self,green,light_green):
        model=self.model

        # Init position To have stetic sense is neccesary that this value has been the same in multiple tha applepos
        self.xs = [160, 160]
        self.ys = [160, 160]
        self.score = 0
        # The award position always is random
        self.applepos = (int(
            np.floor(random.randint(0, int(300 / 20))) * 20), int(np.floor(random.randint(0, int(300 / 20)) * 20)))
        # framework init
        pygame.init()
        # colour of the can

        # draw the screen and adjust the window size
        screen = pygame.display.set_mode((300, 300))
        # draw a rectangle
        screen.fill(light_green)
        pygame.draw.rect(screen, green, [20, 20, 20, 20])
        pygame.display.update()
        # Screen name
        pygame.display.set_caption('Learning snake')
        # save a surface of 20,20 pixels to the snake
        Snake = pygame.Surface((20, 20))
        # fill the snake with colour black that is the (0,0,0)
        Snake.fill((0, 0, 0))

        # save a surface of 10,10 for the award, in this case is filled with a colour red.
        appleimage = pygame.Surface((20, 20))
        appleimage.fill((255, 0, 0))

        f = pygame.font.SysFont('Arial', 20)
        return model, screen, Snake, appleimage, f

    def playGame(self):

        light_green, green = (30, 100, 30), (30, 80, 30)
        model, screen, Snake, appleimage, f=self.init_game(green,light_green)
        clock = pygame.time.Clock()
        dirs, match, state, action, frame, frameRate , reward= 0, 0, 0, 0, 0, 0, 0
        loss= 10000

        while (frame < self.epoch):



            clock.tick(frameRate)

            for e in pygame.event.get():
                if e.type == "QUIT":
                    sys.exit(0)

            # Decrease epsilon over the first half of training
            # This epsilon establishs the size of the lift in the error function
            if (self.epsilon > 0.1):
                self.epsilon -= (0.9 / self.epoch)

            # It is choosen that movement is done
            action, dirs, state, prediction = self.action(action, dirs, match, model,frame)

            # get the reward for the action taken with the state
            state = self.getState()
            reward =  self.reward(state, action, dirs, state)

            # get data to record as experience
            predOutput = model.predict(np.array([state])).flatten().tolist()
            print(predOutput)
            newState = self.getNewState(state, action, dirs)
            newStatePrediction = model.predict(np.array([newState])).flatten().tolist()
            predOutput[action] = reward

            experience = [state, predOutput]
            self.collectExperience(experience)  # record experience
            # print(self.experience)

            # train nueral net on the experience collected
            if (frame == self.batch_size):
            #if loss > 2:
                # get training set from experience
                Xtrain = []
                Ytrain = []
                loss = 0
                for ele in self.experience:

                    Xtrain.append(ele[0])
                    Ytrain.append(ele[1])

                loss = model.fit(np.array(Xtrain), np.array(Ytrain),
                                 batch_size=self.batch_size, epochs=self.epoch,verbose=1)
                # reset frames and expereince

                loss=min(loss.history['loss'])
                print(loss)


                frame = 0
                self.experience = []

     #       elif frame%5 == 0:
     #           loss = model.fit(np.array(Xtrain), np.array(Ytrain),
     #                            batch_size=self.batch_size, epochs=self.epoch, verbose=0)
     #           loss = min(loss.history['loss'])

            # checks if snake collides with itself
            # check if snake collides with wall
            match = self.hit_wall_itself(match)
            # checks if snake collides with apple
            self.eat_apple()
            # in this case move the rest of the body parts
            self.movement(dirs)
            self.draw_screen(screen, green, light_green, Snake, self.score, appleimage, f,frame)

            frame += 1


if __name__ == '__main__':
    SnakeGame = SnakeGame(100)
    SnakeGame.playGame()
