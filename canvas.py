
from QLearning import *
from snake_class import *
from DNN_class import *
import math as m

class canvas():
    def __init__(self):
        #these are the colour of the background
        self.light_green = (30, 100, 30)
        self.green = (30,80,30)
        self.clock = pygame.time.Clock()
        #size of the backgrounf
        self.height = 300
        self.width = 300
        self.size_step = 20
        self.size_range = 20
        self.screen = pygame.display.set_mode((self.height, self.width))
        self.font = pygame.font.SysFont('Arial', 20)
        self.frame_pos = [70, 10]
        self.score_pos = [150, 10]
        self.score = 0
        self.frames = 0
        self.loss = 0
        self.reward = 0
        self.reset = False
        self.eat = False

        # parametros
        self.params = dict()
        self.params['name'] = None
        self.params['epsilon'] = 1
        self.params['gamma'] = .95
        self.params['batch_size'] = 500
        self.params['epsilon_min'] = .01
        self.params['epsilon_decay'] = .995
        self.params['learning_rate'] = 0.00025
        self.params['layer_sizes'] = [128, 128, 128]

        self.state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.apple = apple(self.size_range, self.size_range, self.size_step)
        self.snake = snake(self.height, self.width, self.size_step)
        self.agent_DQN = DQN(self.params, self.snake)

        self.X_train = []
        self.Y_train = []
        self.flag = 0



    def getState(self):
        return ([self.snake.pos_snake_X[0], self.snake.pos_snake_Y[0],
                 self.apple.pos_apple_Y, self.apple.pos_apple_Y])


    def distance(self,offset_X,offset_Y):
        array_snake = np.array([(self.snake.pos_snake_X[0] + offset_X, self.snake.pos_snake_Y[0] + offset_Y)])
        array_apple = np.array([(self.apple.pos_apple_X, self.apple.pos_apple_Y)])

        return m.sqrt(pow((array_snake[0][0]-array_apple[0][0]),2) + pow((array_snake[0][1]-array_apple[0][1]), 2))

    def train_DNN(self):

        dist = []
        #extract distance between head and apple
        dist_init= self.distance(0, 0)
        if self.snake.dir == self.snake.up:
            action_list=[self.snake.right, self.snake.left, self.snake.up]
            dist_up_right = m.fabs(self.distance(20, 0))
            dist_up_left = m.fabs( self.distance(-20, 0))
            dist_up_up = m.fabs(self.distance(0, -20))
            dist = [dist_up_right, dist_up_left, dist_up_up]
            action = action_list[dist.index(min(dist))]
        elif self.snake.dir == self.snake.down:
            action_list = [self.snake.right, self.snake.left, self.snake.down]
            dist_down_right = m.fabs( self.distance(20, 0))
            dist_down_left = m.fabs( self.distance(-20, 0))
            dist_down_down = m.fabs( self.distance(0, 20))
            dist = [dist_down_right, dist_down_left, dist_down_down]
            action = action_list[dist.index(min(dist))]
        elif self.snake.dir == self.snake.right:
            action_list = [self.snake.right, self.snake.down, self.snake.up]
            dist_right_up = m.fabs( self.distance(0, -20))
            dist_right_down = m.fabs( self.distance(0, 20))
            dist_right_right = m.fabs( self.distance(20, 0))
            dist = [dist_right_right, dist_right_down, dist_right_up]
            action = action_list[dist.index(min(dist))]
        elif self.snake.dir == self.snake.left:
            action_list = [self.snake.down, self.snake.left, self.snake.up]
            dist_left_up = m.fabs( self.distance(0, -20))
            dist_left_down = m.fabs( self.distance(0, 20))
            dist_left_left = m.fabs( self.distance(-20, 0))
            dist = [dist_left_down, dist_left_left, dist_left_up]
            action = action_list[dist.index(min(dist))]

        self.X_train.append([self.snake.pos_snake_X[0], self.snake.pos_snake_Y[0],
                        self.apple.pos_apple_X, self.apple.pos_apple_Y])

        self.Y_train.append(action)

        if self.frames > 5:
            self.DNN_model.fitting(np.array(self.X_train), np.array(self.Y_train))

        print(self.DNN_model.loss)

    def train_dqn(self, episode=100):

        sum_of_rewards = []

        for e in range(episode):
            self.score, self.frames, self.loss, self.reward, self.Death, self.state = self.snake.reset(self.screen, self.height, self.apple)
            max_steps = 10000
            for i in range(max_steps):

                self.snake.action = self.agent_DQN.act(self.state)
                prev_state = self.state

                next_state = self.system()

                self.score += self.reward
                #next_state = np.reshape(next_state, (1, self.snake.state_space))

                self.agent_DQN.remember(self.state, self.snake.action, self.reward, next_state, self.Death)

                self.state = next_state

                if self.params['batch_size'] > 1:
                    self.agent_DQN.replay()

                if self.Death:
                    print(f'final state before dying: {str(prev_state)}')
                    print(f'episode: {e + 1}/{episode}, score: {self.score}')
                    break

            sum_of_rewards.append(self.score)

        return sum_of_rewards


    def system(self):

        #Init pygame in this methods
        reward_given = False
        self.screen.fill(self.light_green)
        pygame.display.set_caption('La serpiente taka taka')
        self.screen.fill(self.light_green)
        for x in range(self.size_range, (self.height - self.size_step), 2 * self.size_step):
            for y in range(self.size_range, (self.height - self.size_step), 2 * self.size_step):
                pygame.draw.rect(self.screen, self.green, [x, y, self.size_step, self.size_step])
        self.screen.blit(self.font.render(str(self.frames), True, (250, 250, 250)), self.frame_pos)
        self.screen.blit(self.font.render(str(self.score), True, (250, 250, 250)), self.score_pos)

        dist_old = self.distance(0, 0)
        self.snake.move_snake(self.screen, self.agent_DQN, self.apple)
        self.apple.draw_apple(self.screen)
        dist_new = self.distance(0, 0)

        self.eat = self.snake.eat_apple(self.apple)
        if self.eat == True:
            reward_given = True
            self.reward = 70
            self.screen.blit(self.apple.apple_image, (self.apple.pos_apple(self.height, self.width, self.size_step)[0],
                                                      self.apple.pos_apple(self.height, self.width, self.size_step)[1]))

        self.reset = self.snake.collide_self_wall(self.height, self.width)
        if self.reset == True:
            self.snake.reset_position(self.screen, self.height,self.apple)
            self.reward = -100
            reward_given = True
            self.Death = True

        self.flag = self.flag + 1

        if reward_given == False:
            if dist_old < dist_new:
                self.reward = -2
            else:
                self.reward = 1

        self.snake.draw_snake(self.screen)
        pygame.display.update()
        next_state = self.snake.get_state(self.apple, self.height, self.height)



        return next_state
