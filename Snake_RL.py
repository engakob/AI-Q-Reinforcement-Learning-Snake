###################################################################
######################   Abdallah Kobresli   ######################
##########################   June 2018   ##########################
###################################################################

from turtle import *
import turtle
import random
from random import randint
import time
import datetime
from tqdm import tqdm
import os

CWD = os.getcwd() + '/Logs'
if not os.path.exists(CWD):
    os.makedirs(CWD)


# PENS are: GridPen, SnakePen, TextPen, FoodPen

# Variables 
S_PX = 400 #Screen resolution
global Grid_Size  #Grid Size
global Grid_Factor , GridArray , GridArrayFood , FoodPos
global Snake_Array
global QtxtPath
global ScorePath
global Move_Last
global Available_Moves , UDLR
global Ifgamewon
global TurnsCount, WonGamesCount
global Discount_Factor
global TrainedList
global TurnLog
global TrainedFilePath
global SnakeDead
global pbar
global Iteration
global TurnsToPlay

Snake_Array = list()
TrainedList = list()
Discount_Factor = 0.9
TurnLog = list()
TurnsCount = 0
WonGamesCount = 0.0
Ifgamewon = str()
Ifgamewon = 'False'
SnakeDead = True
UDLR = ['U','D','L','R']
Move_Last = str()
Available_Moves = []
Iteration = 0

TurnsToPlay = 200000
pbar = tqdm(total = TurnsToPlay)
Grid_Size = 10 #Grid Size
Grid_Factor = 20

strdate = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") )
QtxtPath =        CWD + '/TrainedList_Size' + str(Grid_Size) + '.txt'
QtxtPathtemp =    CWD + '/Q-Temp.txt'
ScorePath =       CWD + '/ScoreLog_Size' + str(Grid_Size) + str(strdate) + 'SCORE.txt'


# FoodPos = None

#Define size of the screen
setup(S_PX, S_PX)

GridPen = Pen()
SnakePen = Pen()
FoodPen = Pen()
SnakePen.speed(0)
SnakePen.hideturtle()
FoodPen.hideturtle()


# Comment this line below to make turtle slow!!!!!
turtle.tracer(0, 0)
#Set origin to left bottom corner as a graph
setworldcoordinates(0,0, S_PX, S_PX) #setworldcoordinates(llx, lly, urx, ury)

# Function to write text, Example: TextPenFunc(10,550,'Snake Array: ' + str(Snake_Array))
def TextPenFunc(x,y,i,t):
    turtle.update()
    StrPen = 'TextPen' + str(i)
    StrPen = Pen()
    StrPen.up()
    StrPen.clear()
    StrPen.up()
    StrPen.goto(x,y)
    StrPen.write(t,font=('Arial', 12, 'normal'))
    StrPen.up()
    StrPen.hideturtle()

#POPULATE GRID ARRAY LIST ###############    
def global_GridArray():
    global GridArray
    GridArray = []
    for i in range(0,Grid_Size):         #Fill the grid into an array
        for j in range(0,Grid_Size):
            x = [i,j]
            GridArray.append(x)
    for i in GridArray:                      #remove empty element in list
        if len(i) == 0:
            GridArray.remove(i)
global_GridArray()
def NewSnake():
    global TurnsCount
    global Snake_Array
    global Move_Last
    global TurnLog
    global SnakeDead
    global TrainedList
    global pbar
    global GridArray
    
    L1 = len(TrainedList)
    TrainedListI = list()
    for el in TrainedList:
        if el not in TrainedListI:
            TrainedListI.append(el)
    L2 = len(TrainedListI)
    # print('Removed:', str(L1-L2))
    TrainedList = TrainedListI
    # UpdateQTXT()

    # pbar = tqdm(total = TurnsToPlay)

    try:
        STRi = str(round(float(WonGamesCount/TurnsCount)*100,2))
    except:
        STRi = '0'

    with open(ScorePath, 'a') as text_file:
            str1 = str(TurnsCount) + ',' + str(Ifgamewon) + ',' + str(len(Snake_Array)) + ',' + STRi + '\n'   
            text_file.write(str1)
    


    


    ########## Turn log initialize
    # print('Log: \n')
    # for line in TurnLog:
        # print(line)
    UpdateWeights(TurnLog,TrainedList)
    TurnLog = []

    TurnsCount += 1
    

    Move_Last = ''
    Snake_Array = []
    global_GridArray()
    # X = [0,0]
    X = random.choice(GridArray)
    # print(X)
    Snake_Array.append(X)
    # print('Snake_Array',Snake_Array)

    MakeFood()
    SnakeDead = False
    # print('Won Games: '+ str(WonGamesCount) + ' of Total: ' + str(TurnsCount) + ' Acc: ' + str(round(float(WonGamesCount/TurnsCount)*100,2)) +'%')
    tqdm.write('Won Games: '+ str(WonGamesCount) + ' of Total: ' + str(TurnsCount) + ' Acc: ' + str(round(float(WonGamesCount/TurnsCount)*100,2)) +'%')
    pbar.update()
    StampSnake()
    
   

    
    


def Draw_Grid():
    GridPen.speed(0)
    for x in range(0 , (Grid_Size +1) * Grid_Factor, Grid_Factor):
        GridPen.speed(0)
        GridPen.setheading(0)
        GridPen.up()    
        GridPen.goto(0,x)
        GridPen.down()
        GridPen.forward(Grid_Size * Grid_Factor)
        GridPen.setheading(90)
        GridPen.up()
        # GridPen.write(x/Grid_Factor)
        GridPen.goto(x,0)
        GridPen.down()
        GridPen.forward(Grid_Size * Grid_Factor)
    # Label the coordinates on the grid
    for x in range(0,Grid_Size * Grid_Factor , Grid_Factor):
        GridPen.speed(0)
        GridPen.up()
        GridPen.goto(x + 10,Grid_Size * Grid_Factor + 5)
        GridPen.down()
        GridPen.write( int(x / Grid_Factor))
    for x in range(0,Grid_Size * Grid_Factor , Grid_Factor):
        GridPen.speed(0)
        GridPen.up()
        GridPen.goto(Grid_Size * Grid_Factor + 10,x + 5,)
        GridPen.down()
        GridPen.write( int(x / Grid_Factor))
    GridPen.hideturtle()

def MakeFood():
    global FoodPos
    global GridArrayFood
    global Ifgamewon
    global WonGamesCount
    
    GridArrayFood = None
    GridArrayFood = GridArray
    for i in Snake_Array:               #remove snake position from possible places to put food
        if i in GridArrayFood:
            GridArrayFood.remove(i)
    FoodPen.up()
    FoodPen.clear()
    if len(GridArrayFood) == 0:
        # print('Game Won!')
        Ifgamewon = 'True'
        WonGamesCount += 1
        FoodPen.up()
        FoodPen.clear()
        StampSnake()
    else:
        FoodPos = random.choice(GridArrayFood) #choose a random empty space to stam food in
        Ifgamewon = 'False'
    FoodPen.speed(0)
    FoodPen.shape('circle')
    FoodPen.color('Red')
    
    # FoodPen.goto(GridArray[F][0] * 20 + 10,GridArray[F][1] * 20 + 10)
    FoodPen.goto(FoodPos[0] * 20 + 10,FoodPos[1] * 20 + 10)
    FoodPen.stamp()
    # FoodPos = GridArray[F]
    # TextPenFunc(10,510,3,'Food Position: ' + str(FoodPos))
    turtle.update()

def StampSnake():
    global Snake_Array
    global Grid_Factor
    SnakePen.up()
    SnakePen.clear()
    SnakePen.shape('square')
    turtle.colormode(255)
    SnakePen.color(0,139,0)
    if len(Snake_Array) >= 1:
        # print('Snake_Array from def StampSnake:' ,Snake_Array)
        # print(Snake_Array)
        SnakePen.goto( (Snake_Array[0][0] * Grid_Factor) +10 , (Snake_Array[0][1]*Grid_Factor) +10) #I multiplied by grid factor and added 10 to make snake in the center
        SnakePen.stamp()
        # Stamp the rest of the snake
        if len(Snake_Array) > 1:
            for i in Snake_Array[1:]:
                # print(i)
                SnakePen.shape('circle')
                SnakePen.color(0,205,0)
                SnakePen.goto(i[0]*Grid_Factor +10 ,i[1]*Grid_Factor +10) #I multiplied by grid factor and added 10 to make snake in the center
                SnakePen.stamp()    

# Add a function to return an array of available moves
def Get_Available_Moves():
    global Available_Moves
    global Move_Last
    C = Move_Last
    ALLMoves = ['U','D','L','R']
    if len(Move_Last) == 0:
        Available_Moves = ALLMoves
    
    elif Move_Last == 'U':
        Available_Moves = ['U','L','R']
    elif Move_Last == 'D':
        Available_Moves = ['D','L','R']
    elif Move_Last == 'L':
        Available_Moves = ['U','L','D']
    elif Move_Last == 'R':
        Available_Moves = ['D','U','R']

            
    # else:
    #     for el in ALLMoves:
    #         if el == Move_Last:
    #             ALLMoves.remove(el)
    # Available_Moves = ALLMoves
    return Available_Moves

def SnakeMove(dir1): #I should delete the last element and add a new element at the begining
    # then the direction of the movement should be decided
    global Snake_Array
    global FoodPos
    global Move_Last
    global QtxtPath
    Move_Last = []
    Move_Last = dir1
    
    Snake_Array_Temp = [[]]
    # print('Snake_Array from def SnakeMove1:' ,Snake_Array)
    # with open(QtxtPath, 'a') as text_file:    
        # text_file.write(str(Snake_Array))
    Snake_Array_Temp = Snake_Array
    
    
    Add_Head = [] #Value to add X or Y
    X = Snake_Array_Temp[0][0]
    Y = Snake_Array_Temp[0][1]
    if dir1 == 'U':
        Y += 1
        Add_Head = [X,Y]
        Snake_Array_Temp.insert(0,Add_Head)
        # print('Dir: U')
    if dir1 == 'D':
        Y -= 1
        Add_Head = [X,Y]    
        Snake_Array_Temp.insert(0,Add_Head)
    if dir1 == 'L':
        X -= 1
        Add_Head = [X,Y]
        Snake_Array_Temp.insert(0,Add_Head)
    if dir1 == 'R':
        X += 1
        Add_Head = [X,Y]
        Snake_Array_Temp.insert(0,Add_Head)
    
    # print(dir1)
    # Check if the snake ate food
    if FoodPos in Snake_Array or FoodPos == None:
        MakeFood()
        Snake_Array = Snake_Array_Temp
    else:
        del Snake_Array_Temp[len(Snake_Array_Temp)-1] #Delete Last element, but if 

    Snake_Array = Snake_Array_Temp
    StampSnake()
    return Add_Head, Snake_Array_Temp



# Start Game #####################################################################################

Draw_Grid()

def UpdateQTXT():
    # print('Writing final Q file')
    global TrainedList
    with open(QtxtPath, 'w') as outfile:
        for line in TrainedList:
            # print(line)
            # for a,b,c,d in line:
            if len(line) != 0:
                # x = str(line[0]) + '|' + str(line[1]) + '|' + str(line[2]) + '|' + str(line[3]) + '|'
                outfile.write(str(line))
                outfile.write('\n')                     
    outfile.close()
    #Create a new file with no empty lines 
    with open(QtxtPath) as infile, open(QtxtPathtemp, 'w') as outfile:
        for line in infile:
            if not line.strip(): continue  # skip the empty line
            outfile.write(line)  # non-empty line. Write it to outp
    os.remove(QtxtPath)
    os.rename(QtxtPathtemp,QtxtPath)


def makerand(N):
    X = randint(1,1000)
    if X <= N:
        return True
    else:
        return False

def getlinelength(pos1,pos2):
    try:
        X = float( (((pos2[0]-pos1[0])**2) + ((pos2[1]-pos1[1])**2))**0.5)
        return X
    except:
        print('Error in def getlinelength(pos1,pos2)')

def AppendToLearnedList(S,A,S1,R,F_pos):
    global TrainedList

    # ADDstr = str( str(S) + '|' + str(A) + '|' + str(S1) + '|' + str(R) + '|' )
    X = list()
    X = [S,A,S1,R,F_pos]
    # print('ADDstr:',ADDstr)
    if X not in TrainedList:
        TrainedList.append(X)
        # print('added line:', X)

def UpdateWeights(TLog,TList):
    global TurnLog,TrainedList
    global SnakeDead
    TLog = TurnLog
    TList = TrainedList
    UpdateNeg = bool()
    UpdateNeg = False
    UpdatePositive = bool()
    UpdatePositive = False
    
    if SnakeDead == True:
        # print('Upating Negative Q Values')
        # tqdm.write('Updating Negative Q Values')
        k = 0
        for Tlog1 in TurnLog:
            k += 1
            for Tlist1 in TrainedList:

                if Tlog1[0] == Tlist1[0] and Tlog1[1] == Tlist1[1] and Tlog1[2] == Tlist1[2] and Tlog1[3] != 15 and Tlog1[3] != -1100:
                    # print('Tlog1 Tlist1 found')
                    RM = []
                    # RM = [Tlist1[0],Tlist1[1],Tlist1[2],Tlist1[3]]
                    RM = Tlist1
                    try:
                        TrainedList.remove(RM)
                        # print('Element deleted!!!!!')
                        ADD = []
                        Neg = -1000 #* Discount_Factor ** k
                        ADD = [Tlist1[0],Tlist1[1],Tlist1[2],Neg,Tlist1[4]]
                        TrainedList.append(ADD)
                        # print('Element Added!!!!!')
                        
                    except:
                        print('Unable to modify Negative TrainedList')
                    # print(Tlog1,Tlist1 )
                    # print(Tlist1[3])
                    
                    # print()
                #     print('Tlog1 Tlist1 NOT found')
        # print('TurnLog',TurnLog)
    # print(TurnLog)
    i = 0
    for line in TurnLog:
        i += 1
        # print(i)
        if i == len(TurnLog) and line[3] == 2000 or i == len(TurnLog) and line[3] == 1800:
            UpdatePositive = True
        else:
            UpdatePositive = False

    PositiveReward = 2000
    if UpdatePositive == True:
        print('Updating Positive Q Values')
        
        j = 0
        for Tlog1 in TurnLog:
            j += 1
            # print(Tlog1)
            
        for Tlog1 in TurnLog:
            j -= 1
            for Tlist1 in TrainedList:
                # print(Tlist1)

                if Tlog1[0] == Tlist1[0] and Tlog1[1] == Tlist1[1] and Tlog1[2] == Tlist1[2] and Tlog1[4] == Tlist1[4]:
                    # print('Tlog1 Tlist1 found')
                    RM = []
                    RM = Tlist1
                    try:
                        TrainedList.remove(Tlist1)
                        # print('Element deleted!!!!!')
                        ADD = []
                        PositiveRewardi = round((PositiveReward) * (Discount_Factor ** j),3)
                        ADD = [Tlist1[0],Tlist1[1],Tlist1[2],PositiveRewardi,Tlist1[4]]
                        TrainedList.append(ADD)
                        # print('Updated Positive Q Values',RM,'=>',ADD)
                        # print('Element Added!!!!!')
                        
                    except:
                        print('Unable to modify Positive TrainedList')
    

        

    
    


def start_train():
    global Snake_Array
    global ActionsCount
    global TrainedList
    global Ifgamewon
    global TurnLog
    global SnakeDead
    global ImReward
    global pbar
    global Iteration
    global WonGamesCount

    ImReward = float()

    SnakeDead = False

    TrainedList = list()
    ActionsCount = 0
    Lineslimit =  '' # to read all file---   #how many lines to read in the pre-trained file, for debugging purposes
    try:
        num_lines = sum(1 for line1 in open(QtxtPath)) #get how many lines the program has
        print('num_lines',num_lines)

        with open(QtxtPath) as inputfile:
            print('Loading Static q file',QtxtPath)
            i = 0 ; j = 0
            for line in inputfile:
                i += 1
                # print('line:',i)
                TrainedLine = line
                try:
                    if len (TrainedLine) !=0:
                        addLine = [TrainedLine[0],TrainedLine[1],TrainedLine[2],TrainedLine[3],TrainedLine[4]]
                except:
                    print('iteration:',i,'Error in loading TrainedList append:',TrainedLine)
                    j += 1
                    
                if addLine not in TrainedList and len(addLine)!=0 :
                    TrainedList.append(line)
                if i == Lineslimit:
                    break
        inputfile.close()
    except:
        print('No Trained file found')
    
    print('Size of trained list:',len(TrainedList))
    # print('TrainedList',TrainedList)
    
    StampSnake()

    
    
    pbar = tqdm(total = TurnsToPlay)
############################################ START TRAINING ############################################

    while TurnsCount <= TurnsToPlay: #################### 
        # pbar.update()
        
        # if WonGamesCount == 100:
        #     break
        
        # print('New iteration')
        Snake_Array_BeforeA = []
        # Snake_Array_BeforeA = Snake_Array[:] #This is to make a duplicate instance of the snake before it moves
        Snake_Array_BeforeA = list(Snake_Array)
        # print('ActionsCount:',ActionsCount)
        ActionsCount += 1
        Iteration += 1
        turtle.update()

        

############################### Get the next heuristic move and keep it ready for when to be used

        # M = random.choice(Get_Available_Moves())
        # print(Snake_Array)
        M1 = Get_Available_Moves()
        # print(M1)
        HeuristicMove = ''

        PredictedActions = list()  # [Action,reward]
        PredictedActions = []
        M2 = Get_Available_Moves()
        
        for M2i in M2:   # Get action - reward history
            for el in TrainedList:
                if Snake_Array == el[0] and M2i == el[1]:
                    PredictedActionsI = []
                    PredictedActionsI = [el[1],el[3]]
                    PredictedActions.append(PredictedActionsI)
# Remove duplicates in case they exist
        PredictedActionsT = []
        for el in PredictedActions:
            if el not in PredictedActionsT:
                PredictedActionsT.append(el)
        PredictedActions = PredictedActionsT

            
        # print('PredictedActionsBefore',PredictedActions) #  [['D', -1000], ['R', -1000]]
        # print('M2',M2)
        TempActions = []
        for PAi in PredictedActions:
            TempActions.append(PAi[0])
        # print('TempActions',TempActions)

        for M2j in M2:   # Get action - reward not in history and add a reward of zero
        
            if M2j not in TempActions or str(M2j) not in TempActions:
                ADD =[]
                ADD = [M2j , 0]
                PredictedActions.append(ADD)
        
# Remove duplicates in case they exist        
        PredictedActionsT = []   #[['U', -1000], ['D', -1000], ['L', -1000], ['R', -1000], ['R', 1458.0], ['R', 1620.0]] 
        for el in PredictedActions:
            if el not in PredictedActionsT:
                PredictedActionsT.append(el)
        PredictedActions = PredictedActionsT
        PredictedActionsT2 = []
        PredictedActionsT2 = PredictedActions
        T2 = []
        T2i = []
        if 'U' in M2:
            for el in PredictedActionsT2:
                if str(el[0]) == 'U':
                    T2i.append(el)
            for el in PredictedActionsT2:
                if str(el[0]) == 'U' and el[1] == max(map(lambda x: x[1],T2i)):
                    T2.append(el)
        T2i = []
        if 'D' in M2:
            for el in PredictedActionsT2:
                if str(el[0]) == 'D':
                    T2i.append(el)
            for el in PredictedActionsT2:
                if str(el[0]) == 'D' and el[1] == max(map(lambda x: x[1],T2i)):
                    T2.append(el)
        T2i = []
        if 'L' in M2:
            for el in PredictedActionsT2:
                if str(el[0]) == 'L':
                    T2i.append(el)
            for el in PredictedActionsT2:
                if str(el[0]) == 'L' and el[1] == max(map(lambda x: x[1],T2i)):
                    T2.append(el)
        T2i = []
        if 'R' in M2:
            for el in PredictedActionsT2:
                if str(el[0]) == 'R':
                    T2i.append(el)
            for el in PredictedActionsT2:
                if str(el[0]) == 'R' and el[1] == max(map(lambda x: x[1],T2i)):
                    T2.append(el)
        # for el in PredictedActions:
        PredictedActions = T2
        PredictedActions.sort(key=lambda y: y[1]) #sort list by the second element


        # print(Snake_Array)
        if len(PredictedActions) != 3 and len(Snake_Array) > 1 or len(PredictedActions) == 4 and len(Snake_Array) != 1 or len(PredictedActions) != 3 and len(Snake_Array) != 1:
            print('Error in PredictedActions',PredictedActions,'len(PredictedActions)' , len(PredictedActions) ,'Len of snake:',len(Snake_Array),'Snake:',Snake_Array)
        # print('PredictedActionsAfter',PredictedActions)   # [['D', -1000], ['R', -1000],['U', 0]]
        # Sort elements in inreasing reward order
        
        # print('PredictedActionsBeforeSort',PredictedActions)   # [['D', -1000], ['R', -1000],['U', 0]]
        
        # print('PredictedActionsAfterSort',PredictedActions)   # [['D', -1000], ['R', -1000],['U', 0]]
        
        FinalAction = str()
        PreferredAction = str()
        ActionI = 0
        # print(Snake_Array,PredictedActions)
        Weights = []
        for el in PredictedActions:  
            Weights.append(el[1])    
        # if len(Weights) == 4 and len(Snake_Array) == 1 and Snake_Array == [[0,0]]:
        if len(Weights) == 4 and len(Snake_Array) == 1:
            if PredictedActions[0][1] == PredictedActions[1][1] == PredictedActions[2][1] == PredictedActions[3][1]:
                # print('4 Equal')
                PreferredAction = random.choice(UDLR)
                # print(PreferredAction)
            if PredictedActions[0][1] != PredictedActions[1][1] and PredictedActions[1][1] == PredictedActions[2][1] == PredictedActions[3][1]:
                # print('3 Equal')
                UDLR_Temp = [ PredictedActions[1][0] , PredictedActions[2][0] , PredictedActions[3][0] ]
                PreferredAction = random.choice(UDLR_Temp)
                # print(PreferredAction)
            if PredictedActions[2][1] == PredictedActions[3][1] and PredictedActions[2][1] != PredictedActions[1][1]:
                # print('2 Equal')
                UDLR_Temp = [ PredictedActions[2][0] , PredictedActions[3][0] ]
                PreferredAction = random.choice(UDLR_Temp)
                # print(PreferredAction)
            if PredictedActions[3][1] > PredictedActions[2][1]:
                # print('1 Max')
                PreferredAction = PredictedActions[3][0]
                # print(PreferredAction)
                        # PreferredAction = HeuristicMove
                # PreferredAction = random.choice(Get_Available_Moves())
            ActionI += 1
            # print('NewBorn:', PredictedActions,PreferredAction)
                        # print('Heuristic Action for level 1 snake')


# In case all actions have same Weights, choose a random action ||||||||| Another way is to choose the heuristic action
        Weights = []
        for el in PredictedActions:   # [['D', -1000], ['R', -1000],['U', -1000]]
            Weights.append(el[1])       # Weights [-1000, -1000, -1000]  
        if float(Weights[0]) == float(Weights[1]) and float(Weights[1]) == float(Weights[2]) and len(Weights) == 3: 
            PreferredAction = random.choice(Get_Available_Moves())
            ActionI += 1
            # print('All actions have equal weights, Randomly chosen:',PredictedActions,Weights, PreferredAction)   


# In case the 2 top actions have same weight, choose a random action ||||||||| Another way is to choose the heuristic action
        Weights = []
        for el in PredictedActions:     # [['D', -1000], ['R', 0],['U', 0]]
            Weights.append(el[1])        # Weights [-1000, 0, 0]
        if Weights[2] == Weights[1] and Weights[1] != Weights[0] and len(Weights) == 3:
            PreferredActionI = []
            PreferredActionI = [ PredictedActions[1][0], PredictedActions[2][0] ]
            PreferredAction = random.choice(PreferredActionI)
            ActionI += 1
            # print('Top 2 actions have the same weights, Randomly chosen:',PredictedActions,Weights, PreferredAction)   

# In case the 1 action has the heighest weight, choose a random action ||||||||| Another way is to choose the heuristic action
        Weights = []
        for el in PredictedActions:     # [['D', -1000], ['R', 0],['U', 900]]
            Weights.append(el[1])        # Weights [-1000, 0, 900]
        if Weights[2] > Weights[1] and len(Weights) == 3:
            PreferredAction = PredictedActions[2][0]
            ActionI += 1
            # print('Action with heighest reward chosen:',PredictedActions,Weights, PreferredAction)   

# Now we should choose the action with the highest reward, if actions have equal rewards, choose a random action
        
        if ActionI != 1:
            print("Error, " , ActionI , " actions were chosen for Snake:",Snake_Array,PredictedActions)


        if PreferredAction not in UDLR:
            print('Serious ERROR !!!!!!!! Preferred action should have been chosen by now !!!!!!!!, Action:',PreferredAction)
        
        FinalAction = PreferredAction
# Now we apply the Exploration vs Exploitation ratio , if below apply 
        Ratio = int() #########################     RATIO IS PER 1000
        if TurnsCount < 15000:
            if len(Snake_Array) >= 3:
                Ratio = 100
            else:
                Ratio = 400

        elif 15000 <= TurnsCount <= 50000:
            if len(Snake_Array) >= 3:
                Ratio = 50
            else:
                Ratio = 100

        else:
            Ratio = 2
        
        if ActionsCount >= 200: #To prevent Time-Consuming infinite loops
            if ActionsCount % 10 == 0:
                print('Trying to terminate infinite loop, ActionsCount',ActionsCount)
                Ratio = 500

        # Ratio = 5
        MR = bool()
        MR = makerand(Ratio) 
        if MR == True:
            if ActionsCount >= 100:
                GAM = Get_Available_Moves()
                GAM.remove(PreferredAction)
            else:
                GAM = Get_Available_Moves()
            
            GAMR = random.choice(GAM)
            FinalAction = GAMR
            print('Random Movement, ActionsCount',ActionsCount,GAM,'Random Action:',GAMR,'PreferredAction was:',PreferredAction, 'Ratio',Ratio)
        else:
            FinalAction = PreferredAction
        
        if ActionsCount >= 250:
            Ifgamewon = 'Draw'
            print('-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-| GAME DRAW - Actions: ' , ActionsCount , '|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-')
            WonGamesCount += 0.5
            ActionsCount = 0
            NewSnake()
        
        
        M = FinalAction
        



######################################################

        Food_PosT = []
        Food_PosT = list(FoodPos)

        

        turtle.update()
        
       
        # print(M)
        # print(str(i) + '----' + str(Snake_Array),str(M),Get_Available_Moves())
        if str(M) not in UDLR:
            print("M NOT IN UDLR", M)
            

        SnakeMove(M)


        Snake_Array_AfterA = []
        Snake_Array_AfterA = list(Snake_Array)
        
        


        
        ImReward = 0 #register a step cost and then it will altered if snake is dead or won
        
        #Check if snake left the grid
        for el in Snake_Array: #If snake is outside grid
            global_GridArray()
            if el not in GridArray:
                # print('el',el)
                Ifgamewon = 'False'
                SnakeDead = True
            
                # pbar.update()          
                ImReward = -1100
                ActionsCount = 0
               
        Snake_Array2 = []
        for el in Snake_Array: #If snake ate itself
            if el not in Snake_Array2:
                Snake_Array2.append(el)
            elif el in Snake_Array2:
                
                SnakeDead = True
                ImReward = -1000
                
                Ifgamewon = 'False'
                ActionsCount += 1
                
            
        if len(Snake_Array_BeforeA) == len(Snake_Array_AfterA) -1:
            ImReward = 15
        
        if len(Snake_Array) == Grid_Size ** 2:
            ImReward = 2000
            Ifgamewon == 'True'
            
        if Ifgamewon == 'True':
            ImReward = 2000
            # UpdateWeights(TurnLog,TrainedList)

        AppendToLearnedList(Snake_Array_BeforeA,M,Snake_Array_AfterA,ImReward,Food_PosT)
        # print(Snake_Array_BeforeA,M,Snake_Array_AfterA,ImReward,Food_PosT)


        TurnLogLine = ''
        TurnLogLine = [Snake_Array_BeforeA,M,Snake_Array_AfterA,ImReward,Food_PosT]
        TurnLog.append(TurnLogLine)

        
        if SnakeDead == True:
            ActionsCount = 0
            print('-------------------------------------------------- GAME LOST - Actions: ' , ActionsCount , '--------------------------------------------------')
            NewSnake()
        if Ifgamewon == 'True':
            
            print('************************************************** GAME WON - Actions: ' , ActionsCount , '**************************************************')
            NewSnake()
        if TurnsCount % 10 == 0 and TurnsCount != 0:
            UpdateQTXT()

    

        
NewSnake()                
start_train()    
print('Final --- Turns:',TurnsCount, 'Won:', WonGamesCount)
    # StampSnake()

print('TrainedList',len(TrainedList))

turtle.update()



print('EOF')
mainloop()
print('EOF')