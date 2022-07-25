from distutils.log import info
import numpy as np
import cv2 as cv2
from time import sleep

print("Setting up...")

counter = 0

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

        print(x,y)

def text(text, offset):
    cv2.putText(frame, str(text), (int(frame.shape[1]/2) - offset,int(frame.shape[0]/2)),cv2.FONT_HERSHEY_SIMPLEX, 5, (0,0,0), 5, cv2.LINE_AA)

def caption(active):

    if active:
        cv2.putText(frame, "ACTIVE", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    else:
        cv2.putText(frame, "INACTIVE", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
#1920x1080 fir emmer 100 vum rand fort ze sinn
points = np.array([[100,100],[1820,100],[1820,980],[100,980]], np.int32)

cap = cv2.VideoCapture(0)
sleep(1.5)

while True:
    _, frame  = cap.read()
    
    blank = np.zeros(frame.shape[:2], dtype="uint8")
    polymask = cv2.fillPoly(blank, [points], 255)

    masked = cv2.bitwise_and(frame, frame, mask=polymask)

    for i in range(len(points)):
        if i < 3:
            lines = cv2.line(frame, (points[i][0], points[i][1]), (points[i+1][0], points[i+1][1]), (255, 220, 5), 2)
        else:
            lines = cv2.line(frame, (points[i][0], points[i][1]), (points[0][0], points[0][1]), (255, 220, 5), 2)
        rectangle = cv2.rectangle(frame, (int(points[i][0] - 10), int(points[i][1] - 10)), (int(points[i][0] + 10), int(points[i][1] + 10)), (255, 220, 5), -1)

    cv2.imshow("Masked", masked)

    shadow = 40
    light = 100

    # Methode 1°: MASK mat luucht, ganz ofhängeg vun der belichtung

    lowerLimit = (shadow, shadow, shadow)
    upperLimit = (light, light, light)
    mask = cv2.inRange(masked, lowerLimit, upperLimit)

    # Methode 2°: Bessen besser mengen ech wei Methode 1°

    grayFrame = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
    blurFrame = cv2.GaussianBlur(grayFrame, (13, 13), 0)

    if counter == 4:
        caption(True)
        circles = cv2.HoughCircles(blurFrame, cv2.HOUGH_GRADIENT, 1.2, 100, param1= 100, param2 = 45, minRadius = 30, maxRadius = 150)

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                cv2.circle(frame, (i[0],i[1]), i[2], (0, 255, 0), 3)
    
    else:
        caption(False)

    #contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    

    cv2.imshow("Mask", mask)
    cv2.imshow("Frame", frame)

    cv2.setMouseCallback("Frame", mousePoints)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()