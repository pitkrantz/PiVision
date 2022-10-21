
intersections = []

def simplify():
    intersections.sort(key=lambda intersections:intersections[0])
    print(len(intersections))
    uselessPoints = []

    for i in range (len(intersections) - 1):
        if intersections[i + 1][0] - 50 <= intersections[i][0] <= intersections[i + 1][0] + 50 and intersections[i + 1][1] - 50 <= intersections[i][1] <= intersections[i + 1][1] + 50:
            uselessPoints.append(intersections[i])
    #print(uselessPoints)
    for point in uselessPoints:
        intersections.remove(point)

    uselessPoints = []
    intersections.sort(key=lambda intersections:intersections[1])

    for i in range (len(intersections) - 1):
        if intersections[i + 1][0] - 50 <= intersections[i][0] <= intersections[i + 1][0] + 50 and intersections[i + 1][1] - 50 <= intersections[i][1] <= intersections[i + 1][1] + 50:
            uselessPoints.append(intersections[i])
    #print(uselessPoints)
    for point in uselessPoints:
        intersections.remove(point)
    
    #print(intersections)
    #print(len(intersections))


def CleanIntersections():
    delete = []
    for i in range(len(intersections)):
        if intersections[i][0] > 0 and intersections[i][0] < 1920 and intersections[i][1] > 0 and intersections[i][1] < 1080:
            pass

        else:
            delete.append(i)

    delete = deleteDuplicates(delete)
    for i in reversed(delete):
        intersections.pop(i)