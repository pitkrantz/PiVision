board = [
    # 0    1    2
    ["/", "/", "/"],    #row 0
    ["/", "/", "/"],    #row 1
    ["/", "/", "/"]     #row 2
]

oldboard = [
    # 0    1    2
    ["/", "/", "/"],    #row 0
    ["/", "/", "O"],    #row 1
    ["/", "/", "/"]     #row 2
]

def checkBoard():
    changed = False
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] == oldboard[i][j]:
                pass
            else:
                changed = True
                changedRow = i
                changedColumn = j
    if changed:
        return (changed, changedRow, changedColumn)
    else:
        return (changed, None, None)

boardhasChanged, changedRow, changedColumn = checkBoard()
print(boardhasChanged, changedRow, changedColumn)
