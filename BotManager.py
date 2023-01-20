import os
import serial
from time import sleep
from math import sqrt


#!!!!!!! M4 S100 -> HIGH
# M5 -> LOW

board = [
    # 0    1    2
    ["/", "/", "/"],    #row 0
    ["/", "/", "/"],    #row 1
    ["/", "/", "/"]     #row 2
]
# array with center points of all squares in order to know how to draw everything
boardcoords = [
    [[0,0], [0,0], [0,0]],
    [[0,0], [0,0], [0,0]],
    [[0,0], [0,0], [0,0]]
]

diagonal = 420
squareLength = diagonal/sqrt(2)
# this approach uses a temporary gcode file, which might not be the best for your harddrive (SSD) 
# so I might implement a version where you just save them in a long string or an array or something stored in memory
#robotPort = "/dev/cu.usbserial-A10JYZY0"
robotPort = "/dev/tty.usbmodem212301"

class SerialManager:
    def __init__(self):
        self.ser = serial.Serial(robotPort, 115200)
        sleep(3)
        response = self.ser.readline()
        if response == b"\r\n":
            response = self.ser.readline()
        #print(response)
        print("Connected")
        # self.ser.write(b'G28 \r\n')
        # output = self.ser.readline()
        # if output == b"ok\r\n":
        #     print("ok") 
        #     pass
        # else:
        #     print("Error")
        #     return



        #!!!!! Always close a file before reading it somewhere else, because this saves the acutal data
    def executeFile(self):
        currentFile = open("Instructions.gcode", "r")
        instructions = currentFile.readlines()
        print("file is being read")
        print(len(instructions))
        #print(instructions)
        #print(bytes(instructions[2], "utf-8"))
        for i in range(0, (len(instructions))):
            print(i)
            print(bytes(instructions[i], "utf-8"))
            self.ser.write(bytes(instructions[i], "utf-8"))
            output = self.ser.readline()
            if output == b"ok\r\n":
                print("ok")
            else:
                print(output)     
            sleep(2) 
        # print("deleting file")
        # os.remove("Instructions.gcode")
    
    def closeSerial(self):
        self.ser.close()

class GcodeGenerator:

    def __init__(self):
        self.Connection = serialmanager

    def lineTest(self):
        file = open("Instructions.gcode", "w")
        file.write("G0 X100 Y100\r\n") # move the pen of to the middle a bit
        file.write("M4 S100\r\n")#pen down
        file.write("G4 P1000\r\n")
        file.write("G1 X20\r\n")
        file.write("G1 Y20\r\n")
        file.write("M5\r\n")
        print("Testline File created")
        file.close()

    
    def penDown(self):
        print("Starting Pen Down")
        file = open("Instructions.gcode", "w")
        file.write("M4 S100\r\n")
        file.write("M5\r\n")
        print("File created")
        file.close()

    def calibrate(self):
        print("calibrating...")
        file = open("Instructions.gcode", "w")
        file.write("G28 \r\n")
        file.write("G0 \r\n")
        print("Calibration File created")
        file.close() 

    def cross(self, row, column):
         
        centerPoint = boardcoords[row][column] 
        print("Cross")
        # this function draws a cross starting TL to BR -> BL to TR
        half_squareLength = squareLength/2
        file = open("Intructions.gcode", "w")
        file.write("G0 X" + str(centerPoint[0] - half_squareLength)+ " Y" + str(centerPoint[1] + half_squareLength) + "\r\n")
        file.write("M4") # set pen down
        file.write("G1 X" + str(centerPoint[0] + (half_squareLength)) + " Y" + str(centerPoint[1] - half_squareLength) + "\r\n")
        file.write("M3") # lift pen move to lower left corner 
        file.write("G0 X" + str(centerPoint[0] - half_squareLength) + " Y" + str(centerPoint[1] - half_squareLength) + "\r\n")
        file.write("M4")# set pen down
        file.write("G1 X" + str(centerPoint[0]+ half_squareLength) + " Y" + str(centerPoint[1] + half_squareLength) + "\r\n")
        file.write("M3") # lift pen up
        file.write("G0 X0 Y0" + "\r\n") 
        print("Cross file created")     
        file.close()
    
    def drawPlayingField():
        print("Setting up...")


class player:
    def __init__(self, symbol):
        self.symbol = symbol

ai = player("X") 
human = player("O")


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

serialmanager = SerialManager()

os.remove("Instructions.gcode")

generator = GcodeGenerator()
generator.penDown()
#generator.calibrate()
#generator.lineTest()
serialmanager.executeFile()
sleep(1)
serialmanager.closeSerial()