
board = [
    ["X", "O", "X"],
    ["X", "O", "O"],
    ["X", "/", "O"]
]
def checkWinner():
    #checkRows
    for i in range(3):
        # check Rows
        if len(set(board[i])) == 1:

            if board[i][0] == "X":
                print("Player 1 has won")
            
            if board[i][0] == "O":
                print("Player 2 has won.")

            else:
                pass

        # check Columns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i]:
            if board[0][i] == "X":
                print("Player 1 has won.")
            
            if board[0][i] == "O":
                print("Player 2 has won.")
            else:
                pass
        
        # check Diagonals

    if board[0][0] == board[1][1] == board[2][2]:
        if board[1][1] == "X":
            print("Player 1 has won.")

        if board[1][1] == "O":
            print("Player 2 has won.")
        
        else:
            pass
    if board[2][0] == board[1][1] == board[0][2]:
        if board[1][1] == "X":
            print("Player 1 has won.")

        if board[1][1] == "O":
            print("Player 2 has won.")
        
        else:
            pass
checkWinner()