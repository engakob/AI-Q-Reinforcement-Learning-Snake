# Snake Reinforcement Learning Project using Q-Learning


My goal of this project is to teach a program how to play snake and eventually reach a super-human level of accuracy and wins.

This program was written from scratch and not built on top or inspired by another project.

The snake learns to play on a NxN grid which can be adjusted in the code, 3x3 being a reasonable environment and 10x10 will take so much time to train.

On a regular i5 - 8GB RAM computer, a 3x3 snake takes 4-6 hours to start winning, and more than a day to become optimal. This is due to the enormous amount of possible actions that exist for winning or losing.

And according to the Q-Learning algorithm, the program has to scan all possible state-action-reward pairs before attempting the next action, which gets bigger and bigger as the program runs.


### Requirements
Python 2 or 3\
`pip install turtle`\
`pip install tqdm`\
`pip install os`




### How to start
Run Snake_RL.py to start the game and watch the snake learning.
