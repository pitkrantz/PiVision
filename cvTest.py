import cv2
from time import sleep
cap = cv2.VideoCapture(0)
sleep(2.5)

while True:
    _, frame  = cap.read()
    cv2.imshow("Frame", frame)

cap.release()
cv2.destroyAllWindows()