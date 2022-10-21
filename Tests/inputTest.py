import time
import cv2
import numpy as np

frame = cv2.imread("PiVisionTest.png")


def findIntersections(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y



#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(frame, 50, 150, apertureSize=3)
 
cv2.imshow("edges", edges)

lines = cv2.HoughLinesP(edges, 1, np.pi/180, 200, maxLineGap = 100)
    
vertical = []
horizontal = []
intersections = []

if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]

        if x2- 150 < x1 < x2 + 150:
            vertical.append([[x1, y1], [x2, y2]])
            cv2.line(frame, (x1, y1), (x2, y2), (255,0,0), 3)
        else:
            horizontal.append([[x1, y1], [x2, y2]])
            cv2.line(frame, (x1, y1), (x2, y2), (0,0,255), 3)
    
for i in range(len(vertical)):
    for j in range(len(horizontal)):
        #first start and endpoint
        A = vertical[i][0]
        B = vertical[i][1]
        #last start and endpoint
        C = horizontal[j][0]
        D = horizontal[j][1]

        try: 
            intersectionx, intersectiony = findIntersections((A,B),(C,D))
            intersections.append([intersectionx, intersectiony])
        except:
            pass
    
for intersection in intersections:
    cirlce = cv2.circle(frame, (int(intersection[0]), int(intersection[1])), 20, (0,255,0), -1)

    




cv2.imshow("Input", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()