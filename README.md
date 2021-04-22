# SnakeGame (PyGame) with Keras and Q-learning method

In this repository, I try to explain the way to design a snake game with classes and
controlled for a DNN using Q-learning. The Q-learning is a branch of deep learning that consists 
in create an AI that can learn for itself. 

The required libraries are:
* Pygame (2.0.1)
* Numpy (Last version)
* random
* deque
* TensorFlow > 2.1.0
* Keras (This library need that tensorflow is installed)


The firs step to create this project is to program the snake code. For this purpose
I have used the PyGame library but if you feel more comfortable with other as turtle library
it does not matter, the important is the concept. Once the game has been created and running the 
next step is to include the AI, in this case a DNN with three layers with 30 neurons per layer. 

In the firs step, to create this game I have generated four classes: snake, canvas, DNN and apple. 
They are the main objects in the game. It is possible to program this game without classes, 
but it was more comfortable for me to use classes.

## Class Canvas:

This class is the game board. Its aim is to draw each element of the game, control the score, to 
link the other objects (Snake, apple and DNN).  




