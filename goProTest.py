import cv2
import time

cap = cv2.VideoCapture(0)
time.sleep(1)

while True:
    _, frame = cap.read()

    cv2.imshow("GoPro", frame)

    key = cv2.waitKey(0)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()