import cv2 as cv

capture = cv.VideoCapture(1)

while True:
    isTrue, frame = capture.read()

    cv.imshow("Video", frame)
    
    if cv.waitKey(20) & 0xFF==ord("Q"):
        break

capture.release()
cv.destroyAllWindows()