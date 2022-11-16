# playingboard.field = [
#     ["/", "/", "/"],
#     ["/", "/", "/"],
#     ["/", "/", "/"]
# ]

class board:
    def __init__(self):
        self.field = [
            ["/", "/", "/"],
            ["/", "/", "/"],
            ["/", "/", "/"]
            ]
        self.gameover = False

playingboard = board

rounds = 0
playing = True

class player:
    def __init__(self, symbol):
        self.symbol = symbol

class 
player1 = player("X")
player2 = player("O")

def checkIfAvailable(coord):
    if 0 <= coord[0] <= 2 and 0 <= coord[1] <= 2:
        if playingboard.field[coord[0]][coord[1]] == "/":
            return True
        else:
            return False
    else:
        return False

def printboard():
    print("   " + str(1) + "  " + str(2) +  "  " + str(3) + "  ")
    for i in range(3):
        print(str(i + 1) + "  " + playingboard.field[i][0] + "  " + playingboard.field[i][1] + "  " + playingboard.field[i][2])

def changeboardValue(player, coord):
    if checkIfAvailable(coord):
        playingboard.field[coord[0]][coord[1]] = player.symbol
    else:
        print("Unable to perform action")
        Coord = getPlayerInput()
        changeplayingboard.fieldValue(player, Coord)
    
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



while playing:
    printboard()
    Coord = getPlayerInput()
    changeboardValue.fieldValue(currentPlayer(), Coord)
    os.system("clear")
    if checkWinner() == 1:
        print("Player 1 has won.")
        playing = False
    if checkWinner() == 2:
        print("Player 2 has won.")
        playing = False
    rounds += 1