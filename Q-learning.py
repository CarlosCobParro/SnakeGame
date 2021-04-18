
import random
import numpy as np

from keras import Sequential
from collections import deque
import keras.optimizers
import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout, Flatten
from keras.optimizers import SGD


class DQN:

    """ Deep Q Network """

    def __init__(self, env, params):

        self.action_space = env.action_space
        self.state_space = env.state_space
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
        model = Sequential()
        Adam = keras.optimizers.Adam(
            learning_rate=self.learning_rate,
            beta_1=0.9,
            beta_2=0.999,
            epsilon=1e-01,
            amsgrad=False,
            name="Adam"
        )
        #input layer and first layer with 128 neurons
        self.neuralNet.add(Dense(128, input_shape=12, activation='relu'))

        #layer2
        self.neuralNet.add(Dense(128))
        self.neuralNet.add(Activation('relu'))

        #layer3
        self.neuralNet.add(Dense(128))
        self.neuralNet.add(Activation('relu'))

        # output layer (up, down, right and left) 4 neurons
        self.neuralNet.add(Dense(4))
        self.neuralNet.add(Activation('softmax'))


        self.neuralNet.compile(loss="mean_squared_error", optimizer=Adam, metrics=["mean_squared_error"])
        return model


    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))


    def act(self, state):

        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_space)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])


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

        targets = rewards + self.gamma*(np.amax(self.model.predict_on_batch(next_states), axis=1))*(1-dones)
        targets_full = self.model.predict_on_batch(states)

        ind = np.array([i for i in range(self.batch_size)])
        targets_full[[ind], [actions]] = targets

        self.model.fit(states, targets_full, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
