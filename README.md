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


## Apple class:

To avoid problems is more useful divided every part of the code in classes, that is the sense of this
class. The apple class allows to create objects emulating a apple in the game. Its aim is simple, to appear
in the canvas in a random position and draw the apple, no more. This class has only two method that describe
the below behaviour "def pos_apple" and def "draw_apple". This object has the position X and Y as main variables


## Snake class:

The snake class is more complex than apple class because the snake in the game has number of actions than apple.
The main methods are:
* The snake Movement: is based in two parameters, the first one is the direction of the head, there are 4 directions:
up, down right and left. If the head snake has direction up its movement only can be up, right or left. In this case the
  snake can not move to down.
  
![alt text](images/move.png)

* The snake collide: these methods are used to define when the snake hits with the canvas edges and 
with itself. Two method are defined for this. "def collide_self_wall" to define the type of hit and
  "def collide" to analise if the hit was done. 
  
* The next movement is the eat apple: to know if the snake eats an apple it is necessary to know if the snake hit
the apple. Again, I have used the "def collide" method but in this case with the apple position. 
  
*Draw snake: to draw correctly the snake with their different body parts. 

*Reset: used to draw the snake in the center of the canvas and reset the score values. 

# DQN (Deep Q Network) class

This is the core of the project, this network will can learn and play with easly. The Deep-Q learning
is bases in DNN (deep neural network), the main difference is that included a reward in the result, 
this value is extremely important to punishing or rewarding the network. If you have more interest in this theme
this class also is names as agent. The next gif explains easily the visual way the reinforcement learning.

![alt text](images/Reinforcement-Learning-Animation.gif)

There are a lot of web pages where explain mathematicaly this method. The clue in all of this is the 
Bellman equation which define the next state through the use of the reward. 

![alt text](images/Bellman_equation.png)

The params of the network are approximated is important to understand that in DL this values are not exact. For this reason,
the best way to create the best model is testing with differents params. Some params will do that the training will be more precise but
this always it will do that will be slower. 
In the next link there is a URL to wikipedia for the  [Reinforcement-Learning](https://en.wikipedia.org/wiki/Q-learning)
