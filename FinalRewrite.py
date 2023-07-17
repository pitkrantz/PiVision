import multiprocessing
import cv2
import numpy as np
import ctypes
from time import sleep
from math import sqrt
import BotManager

#really M4S(degree) but 90 is 180 haven't changed that yet
#PIN 11
#!!!!!!! M4 S100 -> HIGH
# M5 -> LOW

diagonal = 420
squareLength = 297

ports = ["/dev/tty.usbmodem212101", "/dev/tty.usbmodem112301", "/dev/tty.usbmodem212301"]

try:
    configFile = open("config.txt", "r")
    offsets = configFile.readlines()
    # offset[0] -> xOffset
    # offset[1] -> yOffset
    xOffset = int(offsets[0])
    yOffset = int(offsets[1])

except:
    print("Error with config file, setting offsets to 0")
    xOffset = 0
    yOffset = 0

################ Main Process ################

def main(InstructionsArray):
    print("Starting...🚀")
    # 1 Webcam
    # 2 Gopro
    cap = cv2.VideoCapture(1)
    sleep(2)

    class modes():
        menu = 0
        calibrate = 1
        offset = 2
        play = 3
        inProgess = 4
        cancel = 5
        testing = 6

    modes = modes()

    currentMode = modes.menu
    gameStarted = False

    def drawMenu():
        cv2.putText(frame, "MENU", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "1. Calibrate", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA) 
        cv2.putText(frame, "2. Offset", (50, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "3. Playing", (50, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "4. Testing", (50, 170), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "ESC Quit", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

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

    def drawTesting():
        cv2.putText(frame, "TESTING", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "1. Pen Down/Up", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA) 
        cv2.putText(frame, "2. XY movement", (50, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        # cv2.putText(frame, "3. Check datalines", (50, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    class player:
        def __init__(self, symbol):
            self.symbol = symbol
    
    ai = player("X")
    human = player("O")

    show = False

    starting = True  # True means the bot starts else the human player starts
    
    board = [
        # 0    1    2
        ["/", "/", "/"], #row 0
        ["/", "/", "/"], #row 1
        ["/", "/", "/"]  #row 
    ]
    oldboard = [
        # 0    1    2
        ["/", "/", "/"], #row 0
        ["/", "/", "/"], #row 1
        ["/", "/", "/"]  #row 
    ]

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
        if freespaces == 0:
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
        besteScore = -800
        move = [0, 0] 
        for i in range(0,3):
            for j in range(0,3):
                if(board[i][j] == "/"):
                    board[i][j] = ai.symbol
                    score = minimax(board, False) 
                    board[i][j] = "/"
                    if (score > bestScore):
                        bestScore = score
                        move = [i, j]
        board[move[0]][move[1]] = ai.symbol

    def minimax(playingboard, isMaximizing):
        result = checkWinner()
        if result != None:
            if result == ai.symbol:
                return 1
            elif result == human.symbol:
                return 0
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
                        if (score > bestScore):
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
        for circle in realCircles:
            distances = []
            closePoints = []
        
            for point in centerPoints:
                PointToCircle = distance((circle.x, circle.y), point)
                if PointToCircle < (diagonal +20):
                    closePoints.append(point)
            print(closePoints)

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

        elif len(closePoints) >= 3:
            board[1][1] = "O"
            print("center")
        
        else:
            print("Error")







    while True:
        _, frame = cap.read()

        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)

################ Sub Process ############################

def com(InstructionsArray):
    print("COM starting")        
    
    generator = BotManager.GcodeGenerator()

    try:
        def executeManager():
            serial = BotManager.SerialManager()
            while True:
                if InstructionsArray[0] == 0:
                    print("executing")
    except:
        print("Error with execution")

##################################################

if __name__ == "__main__":
    
    shared_array = multiprocessing.Array("i", 3)
    # The first number communicates the mode or what should be done
    # 0 -> is used as an indicator, which shows that the robot is ready to receive new data (replaces readyToSend value)
    # 1 -> draw new playing field, 
    # 2 -> draw cross at the following coordinates
    # 3 -> lineTest
    # 4 -> calibrate motors
    # 5 -> draw Point for calibration with camera


    main_process = multiprocessing.Process(target=main, args=(shared_array, ))
    io_process = multiprocessing.Process(target=com, args=(shared_array, ))

    main_process.start()
    io_process.start()

    main_process.join()
    io_process.join()
