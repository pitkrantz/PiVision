circles = [[100, 200, 10], [400, 300, 50], [110, 180, 11], [435,290,10]]



class Circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.number = 1

allcircles = []
for circle in circles:
    newcircle = Circle(circle[0], circle[1], circle[2])
    allcircles.append(newcircle)


def CheckCircles(inputCircles, threshhold = 40):
    #inputCircles = []
    # for i in range(len(circles)):
    #     newCircle = Circle(circles[i][0], circles[i][1], circles[i][2])
    #     inputCircles.append(newCircle)

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

    Copies.reverse()
    for i in Copies:
        inputCircles.pop(i)
    
    return inputCircles

realCircles = CheckCircles(allcircles)

for circle in realCircles:
    print(circle.x)
    print(circle.y)
    print(circle)
    print("\n")
