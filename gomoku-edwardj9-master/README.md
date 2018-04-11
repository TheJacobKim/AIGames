Assignment 3: Gomoku with Monte Carlo Tree Search
=========
Name: Edward Ji
PID: A12962197
Note - Please run this program with python3

Your task is to implement the MCTS method for playing Gomoku. The base game engine is from [here](https://github.com/HackerSir/PygameTutorials/tree/master/Lesson04/Gomoku). 

Important: Your commits should be using the Github Classroom link (in a private repository), not directly cloning from the open repositiory. 

Due date
-----
Feb-24 11:59pm Pacific Time. Extra credits for earlier submission (see below). 

The Game
-----
Gomoku is a popular game played on the Go board, following much simpler rules. 

- There are two players, one placing black pieces and the other white pieces, at the grid intersections of the board. 
- The two players take turns to place one piece each time. Pieces are never moved or removed from the board. 
- The players' goal is to have five pieces of their own color to form an unbroken line horizontally (`examples/ex1.png`), vertically (`examples/ex2.png`), or diagonally (`examples/ex3.png`). Of course, these are unlikely realistic games between reasonable players. A real game is more like `examples/ex4.png` (black is still very lame in the end).  
- The game engine starts with human against a random-play agent. Click any grid intersections and see what the computer does. Press enter to see a random game between two random-play agents (also press enter to pause autoplay and switch back to human vs random). Press 'm' to switch to manually playing both sides.  

Grading
-----
- Regular Commits (1 point)

At least one nontrivial commit by Feb-17 11:59pm. 

- Documentation (1 point)

Comment your code generously. 

- Functionality (10 points)

The MCTS agent should use the standard Monte Carlo Tree Search methods, and consistently beat the random-play agent. 

In the starter code, the automated game (press Enter) is played between two random-play agents. You need to change one of them to an MCTS agent (See the `#TODO` line in the `Board.autoplay` function). 

Read the code for the random-play agent in `randplay.py` carefully. It is more verbose than needed for a random player, just to provide hints for functions that you may need in the MCTS code. In particular, you may want to (not required) implement the random rollout function in the `Randplay` class which can be used in the MCTS class. 

Again, the template in `mcts.py` is just a suggestion. Feel free to change the given functions, and also the other files in minor ways. 

In MCTS the standard loop exits when the "computation budget" is reached. Depending on how fast your code runs, you can put a bound on the number of iterations of the MCTS loop, so that each step by the MCTS takes less than roughly 10 seconds (just so that grading is not painful for us; no need to precisely keep track of time). Note that the requirement of beating the random-play agent is a very low bar, so perhaps you can shorten the computation. 

A main bottleneck of performance is how many next moves you need to consider each time. It is easy to realize that all the interesting moves should be pretty close to the pieces already on the board. Thus, to accelerate search, you could limit the next moves in a small square around where the pieces of your color are. 

Again, random-play agent gives a pretty low bar (if you abuse that by hard-coding any scripted steps, you won't get credits since the point of the assignment is to understand MCTS, not to beat an uninteresting agent). Try entertaining yourself by playing against your MCTS AI and see whether it's smart enough. 


Extra credits (up to 4 points)
------
- 1 extra point for showing on the board the winning line of five pieces (for instance, draw a line through them, or circle each of them). 
- If your last commit is pushed by Feb-17 11:59pm, with no significant bug, then you will earn 3 extra points. 
- If your last major commit is pushed by Feb-17 11:59pm, with also one minor commit after that (definition of a minor commit is less than 5 lines of changes in total), and with no significant bug, you can earn 2 extra points. 

Note
------
- Make sure to start early. It requires more work than Assignment 2. 
- Check the lecture slides for details on MCTS. This [survey article](http://mcts.ai/pubs/mcts-survey-master.pdf) also has all you need to complete the assignment. 
- At the deadline, Github will automatically save the last commit as your submission. Make sure to commit your full solutions before that, and also your name and PID in the README.md file.  
