import math

ai = "X"
human = "O"

currentPlayer = ai


board = [
        ["X","O","/"],
        ["X","O","/"],
        ["/","/","/"]
]

def checkWinner():
    #checkRows
    freespaces = 0
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] == "/":
                    freespaces += 1
    if freespaces == 0:
        return "Tie"

    for i in range(3):
        # check Rows
        if len(set(board[i])) == 1:

            if board[i][0] == "X":
                return ai
            
            if board[i][0] == "O":
                return human

            else:
                return None

        # check Columns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i]:
            if board[0][i] == "X":
                return ai
            
            if board[0][i] == "O":
                return human
            else:
                return None
        
        # check Diagonals

    if board[0][0] == board[1][1] == board[2][2]:
        if board[1][1] == "X":
            return ai

        if board[1][1] == "O":
            return human
        
        else:
            return None
    if board[2][0] == board[1][1] == board[0][2]:
        if board[1][1] == "X":
            return ai

        if board[1][1] == "O":
            return human
        
        else:
            return None
    return None     
    

print(board)

def bestmove():
    bestScore = -math.inf
    for i in range(0,3):
        for j in range(0,3):
            if(board[i][j] == "/"):
                board[i][j] = ai
                score = minimax(True)
                board[i][j] = "/"
                if (score > bestScore):
                    moveRow = i
                    moveCol = j
    board[moveRow][moveCol] = ai
    currentPlayer = human



def minimax( isMaximizing):
 
    result = checkWinner()
    if result != None:
        if result != "Tie":
            if result == ai:
                return 1
            else:
                return -1
        else:
            return 0

    if isMaximizing:
        bestScore = -math.inf
        for i in range(0,3):
            for j in range(0,3):
                if (board[i][j] == "/"):
                    board[i][j] = ai
                    score = minimax(False)
                    board[i][j] = "/"
                    if (score > bestScore):
                        bestScore = score
        return bestScore
    else:
        bestScore = math.inf
        for i in range(0,3): 
            for j in range(0,3):
                if board[i][j] == "/":
                    board[i][j] = human
                    score = minimax(True)
                    board[i][j] = "/"
                    if (score < bestScore):
                        bestScore = score
        return bestScore

if checkWinner() == None:
    bestmove()
    print(board)