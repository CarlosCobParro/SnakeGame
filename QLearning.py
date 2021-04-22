
import random
import numpy as np

from keras import Sequential
from collections import deque
import keras.optimizers
import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout, Flatten
from keras.optimizers import SGD
from keras.optimizers import Adam

class DQN:

    """ Deep Q Network """

    def __init__(self, env, params):



        self.epsilon = 1
        self.gamma = .95
        self.batch_size = 500
        self.epsilon_min = .01
        self.epsilon_decay = .995
        self.learning_rate = 0.00025
        self.layer_sizes = [128, 128, 128]
        self.memory = deque(maxlen=2500)
        self.neuralNet = self.build_model()


    def build_model(self):
        neuralNet = Sequential()
        adam = keras.optimizers.Adam(
            learning_rate=self.learning_rate,
            beta_1=0.9,
            beta_2=0.999,
            epsilon=1e-01,
            amsgrad=False,
            name="Adam"
        )
        #input layer and first layer with 100 neurons
        neuralNet.add(Dense(30, input_shape= (12,) , activation='relu'))

        #layer2
        neuralNet.add(Dense(30))
        neuralNet.add(Activation('relu'))

        # layer2
        neuralNet.add(Dense(30))
        neuralNet.add(Activation('relu'))


        # output layer (up, down, right and left) 4 neurons
        neuralNet.add(Dense(4))
        neuralNet.add(Activation('softmax'))


        neuralNet.compile(loss='mse', optimizer=adam)
        return neuralNet


    def remember(self, state, action, reward, next_state, Death):
        self.memory.append((state, action, reward, next_state, Death))


    def act(self, state):
        action = [0, 0, 0, 0]
        if np.random.rand() <= self.epsilon:
            action[random.sample(([0,1,2,3]),1)[0]] = 1
        else:
            act_values = self.neuralNet.predict(np.array([state]))
            action[np.argmax(act_values[0])] = 1
        return action


    def replay(self):

        if len(self.memory) < self.batch_size:
            return

        minibatch = random.sample(self.memory, self.batch_size)
        states = np.array([i[0] for i in minibatch])
        actions = np.array([i[1] for i in minibatch])
        rewards = np.array([i[2] for i in minibatch])
        next_states = np.array([i[3] for i in minibatch])
        dones = np.array([i[4] for i in minibatch])

        states = np.squeeze(states)
        next_states = np.squeeze(next_states)

        targets = rewards + self.gamma*(np.amax(self.neuralNet.predict_on_batch(next_states), axis=1))*(1-dones)
        targets_full = self.neuralNet.predict_on_batch(states)

        ind = np.array([i for i in range(self.batch_size)])

        pos = []

        for i in actions.tolist(): pos.append(i.index(max(i)))
        targets_full[[ind], [pos]] = targets

        self.neuralNet.fit(states, targets_full, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
