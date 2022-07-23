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

player1 = player("X")
player2 = player("O")

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

def changeBoardValue(player, coord):
    if checkIfAvailable(coord):
        board[coord[0]][coord[1]] = player.symbol
    else:
        print("Unable to perform action")
        Coord = getPlayerInput()
        changeBoardValue(player, Coord)
    
def getPlayerInput():
    user = input("What box do you want to check: ")
    # Switching the values in order to use the cartesian system
    coord = [int(user[1]) - 1, int(user[0]) - 1]
    return coord

def currentPlayer():
    if rounds % 2 == 0:
        return player1
    else:
        return player2

def checkWinner():
    #checkRows
    for i in range(3):
        # check Rows
        if len(set(board[i])) == 1:

            if board[i][0] == "X":
                return 1
            
            if board[i][0] == "O":
                return 2

            else:
                pass

        # check Columns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i]:
            if board[0][i] == "X":
                return 1
            
            if board[0][i] == "O":
                return 2
            else:
                pass
        
        # check Diagonals

    if board[0][0] == board[1][1] == board[2][2]:
        if board[1][1] == "X":
            return 1

        if board[1][1] == "O":
            return 2
        
        else:
            pass
    if board[2][0] == board[1][1] == board[0][2]:
        if board[1][1] == "X":
            return 1

        if board[1][1] == "O":
            return 2
        
        else:
            pass

while playing:
    printBoard()
    Coord = getPlayerInput()
    changeBoardValue(currentPlayer(), Coord)
    os.system("clear")
    if checkWinner() == 1:
        print("Player 1 has won.")
        playing = False
    if checkWinner() == 2:
        print("Player 2 has won.")
        playing = False
    rounds += 1