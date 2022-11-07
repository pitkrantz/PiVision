# board = [
#     ["O", "/", "/"],
#     ["/", "O", "/"],
#     ["/", "/", "/"]
# ]

board = [
    ["O", "X", "O"],
    ["X", "O", "O"],
    ["X", "X", "X"]
]

def checkDraw():
    freespaces = 0
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] == "/":
                freespaces += 1
    if freespaces == 0 :
        return True
    else:
        return False

def checkWinner():
    if board[0][0] == board[0][1] and board[0][1] == board[0][2] and board[0][2] == "X":
        return "X"
    if board[0][0] == board[0][1] and board[0][1] == board[0][2] and board[0][2] == "O":
        return "O"

    if board[1][0] == board[1][1] and board[1][1] == board[1][2] and board[1][2] == "X":
        return "X"
    if board[1][0] == board[1][1] and board[1][1] == board[1][2] and board[1][2] == "O":
        return "O"
        
    if board[2][0] == board[2][1] and board[2][1] == board[2][2] and board[2][2] == "X":
        return "X"
    if board[2][0] == board[2][1] and board[2][1] == board[2][2] and board[2][2] == "O":
        return "O"

    
    if board[0][0] == board[1][0] and board[1][0] == board[2][0] and board[2][0] == "X":
        return "X"
    if board[0][0] == board[1][0] and board[1][0] == board[2][0] and board[2][0] == "O":
        return "O"

    if board[0][1] == board[1][1] and board[1][1] == board[2][1] and board[2][1] == "X":
        return "X"
    if board[0][1] == board[1][1] and board[1][1] == board[2][1] and board[2][1] == "O":
        return "O"
        
    if board[0][2] == board[1][2] and board[1][2] == board[2][2] and board[2][2] == "X":
        return "X"
    if board[0][2] == board[1][2] and board[1][2] == board[2][2] and board[2][2] == "O":
        return "O"


    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[2][2] == "X":
        return "X"
    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[2][2] == "O":
        return "O"

    if board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[2][0] == "X":
        return "X"
    if board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[2][0] == "O":
        return "O"

    if checkDraw():
        return 0
    return None

print(checkWinner())