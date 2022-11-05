import cv2
import numpy as np
from time import sleep

print("Starting...")

counter = 0

board = [
    # 0    1    2
    ["/", "/", "/"],    #row 0
    ["/", "/", "/"],    #row 1
    ["/", "/", "/"]     #row 2
]

cap = cv2.VideoCapture(0)
sleep(1.5)

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

print(len(rows), len(columns))

def checkWinner():
    #checkRows
    for i in range(3):
        # check Rows
        if len(set(board[i])) == 1:

            if board[i][0] == "X":
                return 1
            
            if board[i][0] == "O":
                return 2

            else:
                pass

        # check Columns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i]:
            if board[0][i] == "X":
                return 1
            
            if board[0][i] == "O":
                return 2
            else:
                pass
        
        # check Diagonals

    if board[0][0] == board[1][1] == board[2][2]:
        if board[1][1] == "X":
            return 1

        if board[1][1] == "O":
            return 2
        
        else:
            pass
    if board[2][0] == board[1][1] == board[0][2]:
        if board[1][1] == "X":
            return 1

        if board[1][1] == "O":
            return 2
        
        else:
            pass

def checkboard():
    for circle in realCircles:
        for i in range(0, len(rows)):
            if rows[i].yi < circle.y and circle.y < rows[i].yf:
                circle.row = i
            if columns[i].xi < circle.x and circle.x < columns[i].xf:
                circle.column = i

def updateboard():
    changed = False
    for circle in realCircles:
        if board[circle.row][circle.column] == "/":
            board[circle.row][circle.column] = "O"
            changedField = [circle.row, circle.column]
            changed = True
        else:
            print("No changes")
            #print("Error, something has gone wrong while updating the board!")

    if changed == True:
        print("Bot reaction")
    
    return changed
    print(board)


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



def mousePoints(event, x, y, flags, params):
    global counter
    if event == cv2.EVENT_LBUTTONDOWN:
        if counter < 4:
            points[counter][0] = x
            points[counter][1] = y

            counter += 1
        elif counter == 4:
            counter = 0
        else:
            counter = 0

        #print(x,y)

def text(text, position):
    cv2.putText(frame, str(text),position,cv2.FONT_HERSHEY_SIMPLEX, 5, (0,0,0), 5, cv2.LINE_AA)

def caption(active):

    if active:
        cv2.putText(frame, "ACTIVE", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    else:
        cv2.putText(frame, "INACTIVE", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

#1920x1080 fir emmer 100 vum rand fort ze sinn
points = np.array([[100,100],[1820,100],[1820,980],[100,980]], np.int32)

detectedCircles = 0
frames = 0

numberofCircles = 0

CombinedCircles = []
realCirlces = []

while True:
    CirclesDuringFrame = []

    _, frame  = cap.read()
 
    cv2.setMouseCallback("Frame", mousePoints)

    blank = np.zeros(frame.shape[:2], dtype="uint8")
    polymask = cv2.fillPoly(blank, [points], 255)

    masked = cv2.bitwise_and(frame, frame, mask=polymask)

    for i in range(len(points)):
        if i < 3:
            lines = cv2.line(frame, (points[i][0], points[i][1]), (points[i+1][0], points[i+1][1]), (255, 220, 5), 2)
        else:
            lines = cv2.line(frame, (points[i][0], points[i][1]), (points[0][0], points[0][1]), (255, 220, 5), 2)
        rectangle = cv2.rectangle(frame, (int(points[i][0] - 10), int(points[i][1] - 10)), (int(points[i][0] + 10), int(points[i][1] + 10)), (255, 220, 5), -1)
    
    # Mask preview
    # cv2.imshow("Masked", masked)

    shadow = 40
    light = 100

    # Methode 1°: MASK mat luucht, ganz ofhängeg vun der belichtung

    lowerLimit = (shadow, shadow, shadow)
    upperLimit = (light, light, light)
    mask = cv2.inRange(masked, lowerLimit, upperLimit)

    # Methode 2°: Bessen besser mengen ech wei Methode 1°   !!!!AKTIV!!!!

    grayFrame = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
    blurFrame = cv2.GaussianBlur(grayFrame, (13, 13), 0)

    if counter == 4:
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

            realCircles = CheckCircles(CombinedCircles)
            
            for circle in realCircles:
                if circle.number <= 19:
                    realCircles.remove(circle)

            
            checkboard()
            if updateboard():
                print("Bot makes moves")



            for i in range(0, len(realCircles)):
                print(realCircles[i].row)

            numberofCircles = len(realCircles)
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
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()