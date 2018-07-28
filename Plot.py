###################################################################
######################   Abdallah Kobresli   ######################
##########################   June 2018   ##########################
###################################################################

import matplotlib.pyplot as plt
import numpy as np
import os

# Enter The Name of the Log File
LOG_FileName = 'ScoreLog_Size....SCORE'

CWD = os.getcwd() + '/Logs/'
if not os.path.exists(CWD):
    os.makedirs(CWD)


WinsPerXiterations = 100
TWinsTrue = 0.0
TwinsDraw = 0.0
Scores = list()

ScorePath = CWD + LOG_FileName + '.txt'

with open(ScorePath, 'r') as text_file:
    k = 0 ; Wins = 0.0
    for line in text_file:
        k += 1
        line2 = line.strip().split(',') # [7,False,4,28.57]
        if line2[1] == 'True':
            Wins += 1
            TWinsTrue += 1
        if line2[1] == 'Draw':
            Wins += 0.5
            TwinsDraw += 1

        if k % WinsPerXiterations == 0:
            print(Wins)
            X = []
            X = [k,Wins]
            Scores.append(X)
            Wins = 0
            
        

fig = plt.figure(figsize=(7, 4))  

fig.suptitle('Snake Wins Per ' + str(WinsPerXiterations) + ' Iterations', fontsize=12)

plt.xlabel('Iteration', fontsize=12)
plt.ylabel('Wins', fontsize=12)

XAxis1 = list()
YAxis1 = list()

for line in Scores:
    XAxis1.append(line[0])
    YAxis1.append(line[1])


plt.plot(XAxis1,YAxis1, '.g-',label='RL Q-Learning + Advanced Exploration Gradient')
    


xposition = [15000, 50000]
for xc in xposition:
    plt.axvline(x=xc, color='y', linestyle='--')

plt.legend()
print('Plotting')
plt.show()
fig.savefig('test1.jpg')