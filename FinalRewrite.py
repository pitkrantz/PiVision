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

# Offsets will  probably not work because the x and y Offsets are in the main scope and are only updated for the subprocess at the start of the program

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

def main(shared_array, connected):
    print("Starting...🚀")
    # Webcam -> 1
    #Gopro -> 2
    cap = cv2.VideoCapture(1)
    sleep(2)
    
    if shared_array[0] == 0:
        ready = True

    class modes():
        menu = 0
        calibrate = 1
        offset = 2
        play = 3
        inProgess = 4
        cancel = 5
        testing = 6
        inProgress = 7

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
        bestScore = -800
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
        return move

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
                print("Error cirlce isn't located in playingfield")

    class Circle:
        def __init__(self, x, y, r):
            self.x = x
            self.y = y
            self.r = r
            self.number = 1
            self.row = None
            self.cloumn = None


    def deleteCopies(inputCircles, threshhold = 40):
        Copies = []
        for i in range(0, len(inputCircles)):
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

        for i in range(0, len(inputCircles)):
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

    points = np.array([[100,100],[1820,100],[1820,980],[100,980]], np.int32)
    
    detectedCircles = 0
    frames = 0

    numberofCircles = 0

    CombinedCircles = []
    realCircles = []
    
    while True:
        CirclesDuringFrame = []

        _, frame = cap.read()
        
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurFrame = cv2.GaussianBlur(grayFrame, (13,13), 0)
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
        if currentMode == modes.testing:
            drawTesting()

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
                    cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 3)

            if frames == 20:

                realCircles = CheckCircles(CombinedCircles, 100)

                for circle in realCircles:
                    if circle.number <= 19:
                        realCircles.remove(circle)
        
                updateBoard()

                changed, row, column = checkBoard()
                oldboard = board

                if changed:
                    nextMove = bestMove()

                    print(nextMove)
                    print("Bot makes move at " + str(nextMove[0]) + " and " + str(nextMove[1]))
                    print("Please wait... ")


                    ## basically just taking the field where the cross should be placed and passing it onto the io manager who converts
                    # it into a Gcode instructions which is then send to the Arduino to be executed
                    ################# here comes the new part i still have to write

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

        ########## menu mode

        if currentMode == modes.menu:
            if key == 49:
                currentMode = modes.calibrate
        
            if key == 50:
                currentMode = modes.offset
        
            if key == 51:
                currentMode = modes.play

            if key == 52:
                currentMode = modes.testing

            if key == 27:
                break 
        
        ########### offset mode

        if currentMode == modes.offset:
            cv2.setMouseCallback("Frame", offsetPoint)

            if key == 27:
                currentMode = modes.menu

            if key == 13:
                if connected.value:

                    # still has to be implemented

                    shared_array[0] = 5
                else:
                    print("Not Connected")
            if key == 32:
                if connected.value:
                    shared_array[0] = 5
                else:
                    print("Not Connected")
        
        ############# calibration mode

        if currentMode == modes.calibrate:
            if key == 13:
                if connected.value:
                    print("Calibration starting")
                    generator.calibrate()
                    # readyToSend.Value = True
                else:
                    print("Not Connected")
        
            if key == 27:
                currentMode = modes.menu

        ############### playing mode

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


        ############# in progress mode

        if currentMode == modes.inProgress:
            if key == 27:
                currentMode = modes.cancel
            if key == 32:
                show = not show 

        ############### testing mode

        if currentMode == modes.testing:
            BotManager.InstructionsArr = []
            if key == 27:
                currentMode = modes.menu

            if key == 49:
                if connected.value:
                    # Pen down action
                    print("Pen should go down")
                else:
                    print("Not Connected")

            if key == 50:
                if connected.value:
                   shared_array[0] = 3 
                else:
                    print("Not Connected")

        if currentMode == modes.cancel:
            if key == 89 or key == 121:
                currentMode = modes.menu
                board = [
                            # 0    1    2
                            ["/", "/", "/"],    #row 0
                            ["/", "/", "/"],    #row 1
                            ["/", "/", "/"]     #row 2
                        ]

                show = False

            if key == 78 or key == 110:
                currentMode = modes.inProgress

################ Sub Process ############################

def com(shared_array, connected):
    print("COM starting")
    # GArray = []
    
    generator = BotManager.GcodeGenerator()
 
    try:
        serial = BotManager.SerialManager()
        connected.value = 1
    except:
        print("Error initialising Serial Manager")

    while True:
        if shared_array[0] != 0:

            # 1 Draw playing field
            if shared_array[0] == 1:
                generator.drawPlayingField()
                print(BotManager.InstructionsArr[:])
                serial.executeArr()
                shared_array[0] = 0

            # 2 Drawing Cross at coords
            if shared_array[0] == 2:
                generator.cross(0,1)
                print(BotManager.InstructionsArr[:])
                serial.executeArr()
                shared_array[0] = 0

            # 3 LineTest 
            if shared_array[0] == 3 :
                generator.lineTest()
                print(BotManager.InstructionsArr[:])
                serial.executeArr()
                shared_array[0] = 0

            # 4 calibrate Motors
            if shared_array[0] == 4:
                generator.calibrate()
                print(BotManager.InstructionsArr[:])
                serial.executeArr()
                shared_array[0] = 0

            # 5 Draw point at x and y offset
            if shared_array[0] == 5:
                generator.drawPoint(xOffset, yOffset)
                serial.executeArr()
                shared_array[0] = 0

##################################################

if __name__ == "__main__":
    
    Array = multiprocessing.Array("i", 3)
    isConnected = multiprocessing.Value("i", 0)
    isConnected.value = 0

    # The first number communicates the mode or what should be done
    # 0 -> is used as an indicator, which shows that the robot is ready to receive new data (replaces readyToSend value)
    # 1 -> draw new playing field, 
    # 2 -> draw cross at the following coordinates
    # 3 -> lineTest
    # 4 -> calibrate motors
    # 5 -> draw Point for calibration with camera
   
    main_process = multiprocessing.Process(target=main, args=(Array, isConnected, ))
    io_process = multiprocessing.Process(target=com, args=(Array, isConnected, ))

    main_process.start()
    io_process.start()

    main_process.join()
    io_process.join()
