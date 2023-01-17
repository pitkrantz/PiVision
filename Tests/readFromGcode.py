import os
import cv2
import numpy

#4 Standard Points for Calibration, so middle of playing field
centerPoints = [[0,0], [0,0], [0,0], [0,0]]


# Configure the board with the coordinates here:

# Configure PlayingField
# Select 4 Points -> detect, where they are located (top left, top right, bottom left, bottom right)

def calibrate_playingfield(event, x, y, flags, params):
    global counter
    if event == cv2.EVENT_LBUTTONDOWN:
        if counter < 4:                            
            centerPoints[counter][0] = x      
            centerPoints[counter][1] = y    
            
            counter += 1

        elif counter == 4:
            counter = 0
        else:
            counter = 0

def test():
    distances = []
    for i in range(0,10):
        distances.append([i, i+1])
    print(distances)

# cv2.setMouseCallback("Frame", calibrate_playingfield)


# def create_gcode(nextMove):
#     print(nextMove[1])

test()