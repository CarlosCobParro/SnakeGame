import keras.optimizers
import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout, Flatten
from keras.optimizers import SGD

class DNN_neural():
    def __init__(self):
        self.neuralNet = Sequential()
        self.hiddenLayer_1 = 100
        self.hiddenLayer_2 = 100
        self.Adam = keras.optimizers.Adam(
                            learning_rate=0.00251,
                            beta_1=0.9,
                            beta_2=0.999,
                            epsilon=1e-01,
                            amsgrad=False,
                            name="Adam"
                                        )
        self.sgd = SGD(lr = 0.001, decay = 0.0, momentum = 0.0, nesterov = False)
        self.batch_size = 500
        self.epoch = 20
        self.loss = 10000
        self.epsilon= 5e-01
        self.neuralNet.add(keras.Input(shape=(4,)))

        self.neuralNet.add(Dense(self.hiddenLayer_1))
        self.neuralNet.add(Activation('relu'))

        self.neuralNet.add(Dense(self.hiddenLayer_2))
        self.neuralNet.add(Activation('relu'))

        # create third and last layer
        self.neuralNet.add(Dense(4))
        self.neuralNet.add(Activation('softmax'))

        self.neuralNet.compile(loss="mean_squared_error", optimizer=self.Adam, metrics=["mean_squared_error"])

    def fitting(self, X_train, Y_train):
        self.neuralNet.fit(X_train, Y_train, batch_size=self.batch_size, epochs=self.epoch, verbose=1)
        self.loss = self.neuralNet.history.history['loss'][-1]
    def predicting(self, state):
        prediction = self.neuralNet.predict(np.array([state])).flatten().tolist()
        action = prediction.index(max(prediction))
        action_mov = [0, 0, 0, 0]
        action_mov[action] = 1
        return action_mov

