import cv2
import numpy as np
from time import sleep
from math import sqrt


#notes i could use distance between the found circles and the calibration points to find matching square
# count how many of the calibrations are possible if 1 corner next to it if 2 midle between them else middle

print("Starting...")

counter = 0

class player:
    def __init__(self, symbol):
        self.symbol = symbol

ai = player("X")
human = player("O")

diagonal = 420

# make the program not do circle detection when inactive until button is pressed keybin

show = False

starting = True #If True bot starts else player starts however player always stays O

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

cap = cv2.VideoCapture(0)
sleep(3)

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

columns = []
x0 = 100
x1 = 580
x2 = 1160
x3 = 1740

xboard = [x0,x1,x2,x3]

rows = []
y0 = 100
y1 = 300
y2 = 600
y3 = 900

yboard = [y0,y1,y2,y3]

for i in range(0,3):
    newcolumn = column(i, xboard[i], xboard[i+1])
    columns.append(newcolumn)

    newrow = row(i, yboard[i], yboard[i+1])
    rows.append(newrow)

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

# def updateBoard():
#     for circle in realCircles:
#         for i in range(0, len(rows)):
#             if rows[i].yi < circle.y and circle.y < rows[i].yf:
#                 circle.row = i
#             if columns[i].xi < circle.x and circle.x < columns[i].xf:
#                 circle.column = i
#     for circle in realCircles:
#         board[circle.row][circle.column] = "O"
#         print(board)

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

    # for circle in realCircles:
    #     distances = [] 
    #     closePoints = 0
    #     for point in centerPoints:
    #         PointToCircle = distance((circle.x, circle.y), point)
    #         distances.append(PointToCircle)
    #        # print("This is a distance" + str(distances[0]), str(distances[1]), str(distances[2]), str(distances[3]))  
    #         if PointToCircle < diagonal + 20:
    #             closePoints += 1




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

# def mousePoints(event, x, y, flags, params):
#     global counter
#     if event == cv2.EVENT_LBUTTONDOWN:
#         if counter < 4:
#             points[counter][0] = x
#             points[counter][1] = y
#             counter += 1
#         elif counter == 4:
#             counter = 0
#         else:
#             counter = 0

def calibrate_playingfield(event, x, y, flags, params):
    global counter
    global diagonal
    if event == cv2.EVENT_LBUTTONDOWN: 
        if counter < 4:                            
            centerPoints[counter][0] = x      
            centerPoints[counter][1] = y     
            counter += 1
            diagonal = distance(centerPoints[0], centerPoints[2])
            print(diagonal)

        elif counter == 4:
            for point in centerPoints:
                point[0] = -10 
                point[1] = -10 
            counter = 0
        else:
            counter = 0

def text(text, position):
    cv2.putText(frame, str(text),position,cv2.FONT_HERSHEY_SIMPLEX, 5, (0,0,0), 5, cv2.LINE_AA)

def caption(active):

    if active:
        cv2.putText(frame, "ACTIVE", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    else:
        cv2.putText(frame, "INACTIVE", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

#1920x1080 fir emmer 100 vum rand fort ze sinn
#net mei benotzt well keng mask mei fir ze kucken
points = np.array([[100,100],[1820,100],[1820,980],[100,980]], np.int32)

detectedCircles = 0
frames = 0

numberofCircles = 0

CombinedCircles = []
realCirlces = []


if starting:
    bestMove()

while True:
    CirclesDuringFrame = []

    _, frame  = cap.read()
 
    cv2.setMouseCallback("Frame", calibrate_playingfield)

    blank = np.zeros(frame.shape[:2], dtype="uint8")
   # polymask = cv2.fillPoly(blank, [points], 255)

   # masked = cv2.bitwise_and(frame, frame, mask=polymask)

    # for i in range(len(points)):
    #     if i < 3:
    #         lines = cv2.line(frame, (points[i][0], points[i][1]), (points[i+1][0], points[i+1][1]), (255, 220, 5), 2)
    #     else:
    #         lines = cv2.line(frame, (points[i][0], points[i][1]), (points[0][0], points[0][1]), (255, 220, 5), 2)
    #     rectangle = cv2.rectangle(frame, (int(points[i][0] - 10), int(points[i][1] - 10)), (int(points[i][0] + 10), int(points[i][1] + 10)), (255, 220, 5), -1)


    # draw calibration rectangles to find center
    for point in centerPoints:
        rectangle = cv2.rectangle(frame, ((int(point[0] - 5)), int(point[1] - 5)), (int(point[0] + 5), int(point[1] + 5)), (0, 255, 0), -1)

    # Mask preview
    # cv2.imshow("Masked", masked)

    shadow = 40
    light = 100

    # Methode 1°: MASK mat luucht, ganz ofhängeg vun der belichtung

    lowerLimit = (shadow, shadow, shadow)
    upperLimit = (light, light, light)
   # mask = cv2.inRange(masked, lowerLimit, upperLimit)
    mask = cv2.inRange(frame, lowerLimit, upperLimit)
    # Methode 2°: Bessen besser mengen ech wei Methode 1°   !!!!AKTIV!!!!

   # grayFrame = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurFrame = cv2.GaussianBlur(grayFrame, (13, 13), 0)

    if show:
        caption(True)
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

    else:
        caption(False)

    #boardview = cv2.putText(frame, str(board),(100, 200),cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2, cv2.LINE_AA)
    numberofCirclesView = cv2.putText(frame, "Number of Circles: " + str(numberofCircles),(100, 250),cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2, cv2.LINE_AA)

    cv2.imshow("Mask", mask)
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 32:
        show = not show
    elif key == 27:
        break

cap.release()
cv2.destroyAllWindows()