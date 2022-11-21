class Circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.number = 1
        self.row = None
        self.column = None

newcircle = Circle(33, 21, 10)
realCircles = [newcircle]

rows = [10, 20 ,30]

for circle in realCircles:
        for i in range(0, len(rows)):
            if 10 < circle.y and circle.y < 20:
                circle.row = i
            else:
                circle.row = None
            if 30 < circle.x and circle.x < 40:
                circle.column = i
            else:
                circle.column = None
            print(circle.row, circle.column)