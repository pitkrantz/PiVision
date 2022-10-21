circles = [[100, 200, 10], [400, 300, 50], [110, 180, 11], [435,290,10]]

class Circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

def CheckCircles(circles):
    allCircles = []
    for i in range(len(circles)):
        newCircle = Circle(circles[i][0], circles[i][1], circles[i][2])
        allCircles.append(newCircle)

    Copies = []

    for i in range(0,len(allCircles)):
        if i == len(allCircles)-1:
            pass
        else:
            for j in range(i, len(allCircles)):
                if j == len(allCircles)-1:
                    pass
                else:
                    if allCircles[j+1].x - 30 < allCircles[i].x and allCircles[i].x < allCircles[j+1].x + 30:
                        Copies.append(j+1)

    Copies.reverse()
    for i in Copies:
        allCircles.pop(i)
    
    return allCircles

realCircles = CheckCircles(circles)

for circle in realCircles:
    print(circle.x)
    print(circle.y)
    print("\n")
