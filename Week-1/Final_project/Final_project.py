board = [[" "," "," "],[" "," "," "],[" "," "," "]]

def display_board():
    for row in range(3):
        print(f"  {board[row][0]} | {board[row][1]} | {board[row][2]}")
        if row < 2:
            print(" ---+---+---")


def player_input(player):
    print(f"Player {player}'s turn")
    while True:
        try:
            row = int(input("Enter row (1-3): "))
            column = int(input("Enter column (1-3): "))

            if row not in [1,2,3] or column not in [1,2,3]:
                print("Enter numbers between 1 and 3.")
                continue

            if board[row - 1][column - 1] != " ":
                print("The place is not empty. Try again.")
            else:
                board[row - 1][column - 1] = player
                break
        except:
            print("Invalid input. Try again.")


def check_win(board, player):
    # Rows
    for row in board:
        if row == [player, player, player]:
            return True

    # Columns
    for col in range(3):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True

    # Diagonals
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True

    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True

    return False


def board_full():
    for row in board:
        if " " in row:
            return False
    return True


def players_turn():
    current_player = "X"

    while True:
        display_board()
        player_input(current_player)

        if check_win(board, current_player):
            display_board()
            print(f" Player {current_player} wins!")
            break

        if board_full():
            display_board()
            print("It's a draw!")
            break

        current_player = "O" if current_player == "X" else "X"


players_turn()
