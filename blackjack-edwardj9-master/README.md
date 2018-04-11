Assignment 4: Blackjack with Reinforcement Learning
=========

Name: Edward Ji

PID: A12962197
Note: Please run program using python3

Your task is to implement policy evaluation and Q-Learning for Blackjack. The base game engine is from [here](https://github.com/ServePeak/Blackjack-Python/blob/master/blackjack.py). 

Important: Your commits should be using the Github Classroom link (in a private repository), not directly cloning from the open repositiory. 

Note that I've increased the points of Assignment 4 and Assignment 5 to 16 points (other than extra credits), and Assignment 6 will still be 12 points. This is to incentivize you to collect the points earlier because the last assignment will likely be due just a few days before the final exam. 

Due date
-----
March 4 (Sunday) 11:59pm Pacific Time. Extra credits for earlier submission (see below). 

The Game
-----
The game more or less follows the standard Blackjack rules. Read the game engine code to see minor simplification (note that the learning algorithms do not need to understand the rules). 

Grading
-----
Regular Commits (1 point): At least one nontrivial commit by Feb-28 11:59pm. 

Documentation (1 point): Comment your code generously. 

Functionality (14 points): Your task is to implement the following algorithms. In all of them, use 0.9 for the discount factor gamma. When the player wins, give reward +1, and when loses, give -1. Currently there is a "draw" case, which you can either give 0 or count it as the player losing in that case. 

- (4 points) Monte Carlo Policy Evaluation (named Direct Utility Estimation in the AIMA book)

Evaluate the policy "Hit (ask for a new card) if sum of cards is below 17, and Stand (switch to dealer) otherwise" using the Monte Carlo method -- namely, learn the utilities for each state under the policy. One should be able to click the "MC" white button to start or pause the learning process. When the user manually plays the game, the learned utility will be shown for the current state. 

- (4 points) Temporal-Difference Policy Evaluation

Evaluate the policy "Hit (ask for a new card) if sum of cards is below 17, and Stand (switch to dealer) otherwise" using the Temporal-Difference method. One should be able to click the "TD" white button to start or pause the learning process. When the user manually plays the game, the learned utility will be shown for the current state. 

- (6 points) Q-Learning

Implement the Q-learning algorithm. After learning, when the user plays manually, the Q values will be displayed for each action (two choices) to guide the user. 

Extra credits (up to 3 points)
------
If your last commit is pushed by Feb-28 11:59pm, with no significant bug, then you will earn 3 extra points. 

Note
------
Make sure to start early. The algorithms are simple, but making it work with the game engine still requires some work. 
