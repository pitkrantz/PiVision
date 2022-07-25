import time
import numpy as np
import cv2

print("Setting up...")

cap = cv2.VideoCapture(0)
time.sleep(1)

while True:
    _, frame = cap.read()


    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurFrame = cv2.GaussianBlur(grayFrame, (15, 15), 0) 

    circles = cv2.HoughCircles(blurFrame, cv2.HOUGH_GRADIENT, 1.2, 100, param1= 100, param2 = 35, minRadius = 30, maxRadius = 150)


    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            cv2.circle(frame, (i[0],i[1]), i[2], (0, 255, 0), 3)

    cross = cv2.line(frame, (int(frame.shape[1]/2), int(frame.shape[0]/2 - 50)), (int(frame.shape[1]/2), int(frame.shape[0]/2 + 50)), (0, 0, 255), 2)
    cross = cv2.line(frame, (int(frame.shape[1]/2 - 50), int(frame.shape[0]/2)), (int(frame.shape[1]/2 + 50), int(frame.shape[0]/2)), (0, 0, 255), 2)
    cv2.imshow("BlurFrame", blurFrame)
    cv2.imshow("Circles", frame)


    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
