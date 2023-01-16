import os


board = [
    ["/", "/", "/"],
    ["/", "/", "/"],
    ["/", "/", "/"]
]


rounds = 0
playing = True

class player:
    def __init__(self, symbol):
        self.symbol = symbol

ai = player("X")
human = player("O")

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


def checkIfAvailable(coord):
    if 0 <= coord[0] <= 2 and 0 <= coord[1] <= 2:
        if board[coord[0]][coord[1]] == "/":
            return True
        else:
            return False
    else:
        return False

def printBoard():
    print("   " + str(1) + "  " + str(2) +  "  " + str(3) + "  ")
    for i in range(3):
        print(str(i + 1) + "  " + board[i][0] + "  " + board[i][1] + "  " + board[i][2])

def changeBoardValue(coord):
    if checkIfAvailable(coord):
        board[coord[0]][coord[1]] = "O"
    else:
        print("Unable to perform action")
        Coord = getPlayerInput()
        changeBoardValue(Coord)

def playerMove():
    if checkWinner() == None:
        changeBoardValue(getPlayerInput())
    
    
def getPlayerInput():
    user = input("What box do you want to check: ")
    # Switching the values in order to use the cartesian system
    coord = [int(user[1]) - 1, int(user[0]) - 1]
    return coord


def currentPlayer():
    if rounds % 2 == 0:
        return ai
    else:
        return human

def bestMove():
    bestScore = -800
    move = [0, 0]
    for i in range(0,3):
        for j in range(0,3):
            if(board[i][j] == "/"):
                board[i][j] = ai.symbol
                score = minimax(board, False)
                board[i][j] = "/"
                if(score > bestScore):
                    bestScore = score
                    move = [i, j]
                
    board[move[0]][move[1]] = ai.symbol
    print(move[0], move[1])



def minimax(playingboard, isMaximizing):
    result = checkWinner()
    if result != None:
        if result == ai.symbol:
            return 1
        elif result == human.symbol:
            return -1
        if result == 0:
            return 0

    
    if (isMaximizing):
        bestScore = -800
        for i in range(0,3):
            for j in range(0,3):
                if(playingboard[i][j] == "/"):
                    playingboard[i][j] = ai.symbol
                    score = minimax(playingboard, False)
                    playingboard[i][j] = "/"
                    if (score > bestScore):
                        bestScore = score
        return bestScore

    else:
        bestScore = 800
        for i in range(0,3):
            for j in range(0,3):
                if(playingboard[i][j] == "/"):
                    playingboard[i][j] = human.symbol
                    score = minimax(playingboard, True)
                    playingboard[i][j] = "/"
                    if (score < bestScore):
                        bestScore = score
        return bestScore

while checkWinner() == None:
    bestMove()
    printBoard()
    playerMove()

if checkWinner() != 0:
    print(checkWinner() + " has won")
else:
    print("Draw")