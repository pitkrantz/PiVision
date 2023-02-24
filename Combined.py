import cv2
import numpy as np
from time import sleep
from math import sqrt
import BotManager

print("Starting...")

cap = cv2.VideoCapture(1)
sleep(2.5)

connected = False

try:
    configFile = open("config.txt", "r")
    offsets = configFile.readlines()

    # offset[0] -> xOffset
    # offset[1] -> yOffset
    xOffset = int(offsets[0])
    yOffset = int(offsets[1])

    # print(offsets[0].strip())
    # print(offsets[1].strip())

except:
    print("Error with config file")
    xOffset = 0
    yOffset = 0

generator = BotManager.GcodeGenerator

try:
    serial = BotManager.serialmanager
    connected = True

except:
    print("Serial error")
    connected = False

# modes = ["menu", "calibrate", "offset", "play"]
class modes():
    menu = 0
    calibrate = 1 
    offset = 2
    play = 3
    inProgress = 4
    cancel = 5

modes = modes()

currentMode = modes.menu

gameStarted = False

counter = 0

def drawMenu():
    cv2.putText(frame, "MENU", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "1. Calibrate", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA) 
    cv2.putText(frame, "2. Offset", (50, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "3. Playing", (50, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "ESC Quit", (50, 170), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

def drawCalibrate():
    cv2.putText(frame, "CALIBRATE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "Press Enter to calibrate", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

def drawOffset():
    cv2.putText(frame, "OFFSET", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "Press Enter to draw calibration", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "Press Space to check", (50, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "xoffset: " + str(xOffset), (900, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "yoffset: " + str(yOffset), (900, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.rectangle(frame, (xOffset-2, yOffset-2), (xOffset + 2, yOffset + 2), (255, 0, 255), -1)

def drawPlay():
    cv2.putText(frame, "PLAY", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA) 
    cv2.putText(frame, "P. Player starts", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA) 
    cv2.putText(frame, "C. Computer starts", (50, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA) 

def drawInProgress():
    cv2.putText(frame, "PLAYING", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA) 

def drawCancel():
    cv2.putText(frame, "Do you really want to cancel (y/n)", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA) 

class player:
    def __init__(self, symbol):
        self.symbol = symbol

ai = player("X")
human = player("O")

diagonal = 420

# make the program not do circle detection when inactive until button is pressed keybin

show = False

starting = True     #If True bot starts else player starts however player always stays O

board = [
    # 0    1    2
    ["/", "/", "/"],    #row 0
    ["/", "/", "/"],    #row 1
    ["/", "/", "/"]     #row 2
]

oldboard = [
    # 0    1    2
    ["/", "/", "/"],    #row 0
    ["/", "/", "/"],    #row 1
    ["/", "/", "/"]     #row 2
]

# xOffset = 0
# yOffset = 0

xRobot = 100
yRobot = 100

constant = 1

class row:
    def __init__(self, id, yi, yf):
        self.id = id
        self.yi = yi
        self.yf = yf

class column:
    def __init__(self, id, xi, xf):
        self.id = id
        self.xi = xi
        self.xf = xf

# playing field 300x300 per square so 900x900 in total which means that the points should 
# respect the resolution and form a 900x900 matrix in the middle
# A = (810, 390) B = (1110, 390) C = (810, 690) D = (810, 690)
centerPoints = [[810,390], [1110, 390], [1110, 690], [810, 690]]

def offsetPoint(event, x, y, flags, params):
    global xOffset
    global yOffset 
    if event == cv2.EVENT_LBUTTONDOWN:
        xOffset = x
        yOffset = y
        configFile = open("config.txt", "w")
        configFile.write(str(xOffset) + "\n" + str(yOffset))

def checkDraw():
    freespaces = 0
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] == "/":
                freespaces += 1
    if freespaces == 0 :
        return True
    else:
        return False

def distance(point1, point2):
    return int(sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2))

def checkWinner():
    if board[0][0] == board[0][1] and board[0][1] == board[0][2] and board[0][2] == "X":
        return "X"
    if board[0][0] == board[0][1] and board[0][1] == board[0][2] and board[0][2] == "O":
        return "O"

    if board[1][0] == board[1][1] and board[1][1] == board[1][2] and board[1][2] == "X":
        return "X"
    if board[1][0] == board[1][1] and board[1][1] == board[1][2] and board[1][2] == "O":
        return "O"
        
    if board[2][0] == board[2][1] and board[2][1] == board[2][2] and board[2][2] == "X":
        return "X"
    if board[2][0] == board[2][1] and board[2][1] == board[2][2] and board[2][2] == "O":
        return "O"

    
    if board[0][0] == board[1][0] and board[1][0] == board[2][0] and board[2][0] == "X":
        return "X"
    if board[0][0] == board[1][0] and board[1][0] == board[2][0] and board[2][0] == "O":
        return "O"

    if board[0][1] == board[1][1] and board[1][1] == board[2][1] and board[2][1] == "X":
        return "X"
    if board[0][1] == board[1][1] and board[1][1] == board[2][1] and board[2][1] == "O":
        return "O"
        
    if board[0][2] == board[1][2] and board[1][2] == board[2][2] and board[2][2] == "X":
        return "X"
    if board[0][2] == board[1][2] and board[1][2] == board[2][2] and board[2][2] == "O":
        return "O"


    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[2][2] == "X":
        return "X"
    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[2][2] == "O":
        return "O"

    if board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[2][0] == "X":
        return "X"
    if board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[2][0] == "O":
        return "O"

    if checkDraw():
        return 0
    return None

def bestMove():
    bestScore = -800
    move = [0, 0]
    for i in range(0,3):
        for j in range(0,3):
            if(board[i][j] == "/"):
                board[i][j] = ai.symbol
                score = minimax(board, False)
                board[i][j] = "/"
                if(score > bestScore):
                    bestScore = score
                    move = [i, j]
                
    board[move[0]][move[1]] = ai.symbol

def minimax(playingboard, isMaximizing):
    result = checkWinner()
    if result != None:
        if result == ai.symbol:
            return 1
        elif result == human.symbol:
            return -1
        if result == 0:
            return 0

    if (isMaximizing):
        bestScore = -800
        for i in range(0,3):
            for j in range(0,3):
                if(playingboard[i][j] == "/"):
                    playingboard[i][j] = ai.symbol
                    score = minimax(playingboard, False)
                    playingboard[i][j] = "/"
                    if (score > bestScore):
                        bestScore = score
        return bestScore

    else:
        bestScore = 800
        for i in range(0,3):
            for j in range(0,3):
                if(playingboard[i][j] == "/"):
                    playingboard[i][j] = human.symbol
                    score = minimax(playingboard, True)
                    playingboard[i][j] = "/"
                    if (score < bestScore):
                        bestScore = score
        return bestScore

def checkBoard():
    changed = False
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] == oldboard[i][j]:
                pass
            else:
                changed = True
                changedRow = i
                changedColumn = j
    if changed:
        return (changed, changedRow, changedColumn)
    else:
        return (changed, None, None)

def updateBoard():
    #I'm going to sleep now, i have enough of this error even though i have done this 1000000 times wihtout problems and now something goes wrong :( 
    #AttributeError: 'NoneType' object has no attribute 'append'
    for circle in realCircles:
        distances = []
        closePoints = []
        #numberOfClosePoints = 0
        for point in centerPoints:
            PointToCircle = distance((circle.x, circle.y), point)
            #distances.append([PointToCircle,point])
            if PointToCircle < (diagonal + 20):
                #numberOfClosePoints += 1
                closePoints.append(point)
        print(closePoints)
        #For this to work it is important that all the points are set TR, TL, BR, BL in this order
        
       #check corners
        if len(closePoints) == 1:
            PointA = centerPoints.index(closePoints[0])
            if PointA == 0:
                board[0][0] = "O"
            if PointA == 1:
                board[0][2] = "O"   
            if PointA == 2:
                board[2][2] = "O" 
            if PointA == 3:
                board[2][0] = "O"   
            
            print("corner")
        # check edges        
        elif len(closePoints) == 2:
            PointA = centerPoints.index(closePoints[0])
            PointB = centerPoints.index(closePoints[1])

            if (PointA == 0 and PointB == 1) or (PointA == 1 and PointB == 0):
                board[0][1] = "O" 

            if (PointA == 2 and PointB == 1) or (PointA == 1 and PointB == 2):
                board[1][2] = "O" 

            if (PointA == 2 and PointB == 3) or (PointA == 3 and PointB == 2):
                board[2][1] = "O" 

            if (PointA == 0 and PointB == 3) or (PointA == 3 and PointB == 0):
                board[1][0] = "O" 

            print("edge")
        #check center
        elif len(closePoints) >= 3:
            board[1][1] = "O"
            print("center") 
        else:
            print("Error")

class Circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.number = 1
        self.row = None
        self.column = None

def deleteCopies(inputCircles, threshhold = 40):
    Copies = []

    for i in range(0,len(inputCircles)):
        if i == len(inputCircles)-1:
            pass
        else:
            for j in range(i, len(inputCircles)):
                if j == len(inputCircles)-1:
                    pass
                else:
                    if inputCircles[j+1].x - threshhold < inputCircles[i].x and inputCircles[i].x < inputCircles[j+1].x + threshhold and inputCircles[j+1].y - threshhold < inputCircles[i].y and inputCircles[i].y < inputCircles[j+1].y + threshhold:
                        Copies.append(j+1)

    Copies.reverse()
    for i in Copies:
        inputCircles.pop(i)
    
    return inputCircles

def CheckCircles(inputCircles, threshhold = 40):
    Copies = []

    for i in range(0,len(inputCircles)):
        if i == len(inputCircles)-1:
            pass
        else:
            for j in range(i, len(inputCircles)):
                if j == len(inputCircles)-1:
                    pass
                else:
                    if inputCircles[j+1].x - threshhold < inputCircles[i].x and inputCircles[i].x < inputCircles[j+1].x + threshhold and inputCircles[j+1].y - threshhold < inputCircles[i].y and inputCircles[i].y < inputCircles[j+1].y + threshhold:
                        inputCircles[i].number += 1
                        Copies.append(j+1)

    if len(Copies) != 0:
        realCopies = []
        for i in Copies:
            if i not in realCopies:
                realCopies.append(i)

        realCopies.sort()
        realCopies.reverse()
        for i in realCopies:
            inputCircles.pop(i)
    
    return inputCircles

# def calibrate_playingfield(event, x, y, flags, params):
#     global counter
#     global diagonal
#     if event == cv2.EVENT_LBUTTONDOWN: 
#         if counter < 4:                            
#             centerPoints[counter][0] = x      
#             centerPoints[counter][1] = y     
#             counter += 1
#             diagonal = distance(centerPoints[0], centerPoints[2])
#             print(diagonal)

#         elif counter == 4:
#             for point in centerPoints:
#                 point[0] = -10 
#                 point[1] = -10 
#             counter = 0
#         else:
#             counter = 0

# def caption(active):
#     if active:
#         cv2.putText(frame, "ACTIVE", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
#     else:
#         cv2.putText(frame, "INACTIVE", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

#1920x1080 fir emmer 100 vum rand fort ze sinn
#net mei benotzt well keng mask mei fir ze kucken
points = np.array([[100,100],[1820,100],[1820,980],[100,980]], np.int32)

detectedCircles = 0
frames = 0

numberofCircles = 0

CombinedCircles = []
realCirlces = []

# if starting:
#     bestMove()

while True:
    CirclesDuringFrame = []

    _, frame  = cap.read()
 
    # draw calibration rectangles to find center
    # for point in centerPoints:
    #     rectangle = cv2.rectangle(frame, ((int(point[0] - 5)), int(point[1] - 5)), (int(point[0] + 5), int(point[1] + 5)), (0, 255, 0), -1)
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurFrame = cv2.GaussianBlur(grayFrame, (13, 13), 0)

    #draw interface
    if currentMode == modes.menu:
        drawMenu()
    if currentMode == modes.calibrate:
        drawCalibrate()
    if currentMode == modes.offset:
        drawOffset()
    if currentMode == modes.play:
        drawPlay()
    if currentMode == modes.cancel:
        drawCancel()
    if currentMode == modes.inProgress:
        drawInProgress()
     
        if show:
           circles = cv2.HoughCircles(blurFrame, cv2.HOUGH_GRADIENT, 1.2, 100, param1= 100, param2 = 45, minRadius = 20, maxRadius = 150)
           if circles is not None:
               detectedCircles += 1
               circles = np.uint16(np.around(circles))

               for circle in circles[0, :]:
                   newcircle = Circle(circle[0], circle[1], circle[2])
                   CirclesDuringFrame.append(newcircle)
                   CirclesDuringFrame = deleteCopies(CirclesDuringFrame)

                   for circle in CirclesDuringFrame:
                       CombinedCircles.append(circle)

               for i in circles[0, :]:
                   cv2.circle(frame, (i[0],i[1]), i[2], (0, 255, 0), 3)

           if frames == 20:

               realCircles = CheckCircles(CombinedCircles, 100)
               
               for circle in realCircles:
                   if circle.number <= 19:
                       realCircles.remove(circle)

               #have to change the entire updating system to implement the new circle detection mode using the center points
               # this one uses presets with fixed values defined at the beginning of the file 
               updateBoard()

               # i should be able to keep this the same as i'm comparing the old with the new board to see changes, as i need to see when the board has actually changed or the person has drawn a second invalid circle
               changed, row, column = checkBoard()
               oldboard = board

               if changed:
                   bestMove()
                   print("Bot makes moves")

                   #here comes the code which makes the robot do its moves

               numberofCircles = len(realCircles)

               try:
                   print("Found circles" + CombinedCircles[0].x, CombinedCircles[0].y, CombinedCircles[0].r)
               except:
                   print("No circles")
               CombinedCircles = []
               realCircles = []
               frames = 0
               
           frames += 1

    numberofCirclesView = cv2.putText(frame, "Number of Circles: " + str(numberofCircles),(1500, 50),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 1, cv2.LINE_AA)
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)

    if currentMode == modes.menu:
        if key == 49:
            currentMode = modes.calibrate
        
        if key == 50:
            currentMode = modes.offset
        
        if key == 51:
            currentMode = modes.play

        if key == 27:
            break

    if currentMode == modes.offset:
        cv2.setMouseCallback("Frame", offsetPoint)

        if key == 27:
            currentMode = modes.menu

        if key == 13:
            if connected:
                generator.offsetCalibration()
                serial.executeArr()
            else:
                print("Not Connected")
        if key == 32:
            if connected:
                generator.drawPoint(xOffset, yOffset)
                serial.executeArr()
            else:
                print("Not Connected")

    if currentMode == modes.calibrate:
        if key == 13:
            if connected:
                print("Calibration starting")
                generator.calibrate()
                serial.executeArr() 
            else:
                print("Not Connected")
        
        if key == 27:
            currentMode = modes.menu

    if currentMode == modes.play:
        if gameStarted == False:
            #bot starts
            if key == 67 or key == 99:
                starting = True
                currentMode = modes.inProgress
            # player starts
            if key == 80 or key == 112:
                starting = False
                currentMode = modes.inProgress

    if currentMode == modes.inProgress:
        if key == 27:
            currentMode = modes.cancel
        if key == 32:
            show = not show 
        
    if currentMode == modes.cancel:
        if key == 89 or key == 121:
            currentMode = modes.menu
            board = [
                        # 0    1    2
                        ["/", "/", "/"],    #row 0
                        ["/", "/", "/"],    #row 1
                        ["/", "/", "/"]     #row 2
                    ]
        if key == 78 or key == 110:
            currentMode = modes.inProgress

cap.release()
cv2.destroyAllWindows()