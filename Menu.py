from solver6 import *
from tictactoe6 import *
import copy 

message = "WELCOME to Alexei's TicTacToe!"
space = "   "
print(message)
def menu():
    print("What variant of TicTacToe would you like to play/solve?")
    print("[1] Original")
    print("[2] Only_X")
    print("[3] Misere")
    print("[4] Misere Only X")
    print("[5] Order and Chaos, Order First")
    print("[6] Order and Chaos, Chaos First")
    print("[0] EXIT")
    print('\n')

def convert_variant(variant_int):

    # #version = "Original"
    # #version = "Only_X"
    # #version = "Order_and_Chaos_Order_First"
    # version = "Order_and_Chaos_Chaos_First"
    # Misere = False
    mapping = {
                "1": "Original",
                "2": "Only_X",
                "3": "Misere", 
                "4": "Misere Only_X",
                "5": "Order_and_Chaos_Order_First",
                "6": "Order_and_Chaos_Chaos_First"
            }
    return mapping[variant_int]


def options():
    print("What would you like to do?")
    print("[S] Solve the game!")
    print("[P] Play the game!")

def instructions():
    print("A quick note about how to play:")
    print("1.) Players will take turns marking the board")
    print("2.) If at any point, you'd like to undo a move press [U] and then confirm the undo on the next player's turn")
    print('\n')

def play_game_menu():
    print("How would you like to play the game?")
    print("[0] Human vs. Human")
    print("[1] Human vs. Computer")
    print('\n')

def who_goes_first():
    print("Would you like to start first?")
    print("[Y] Yes")
    print("[No] No")
    print('\n')


def solveGame(board, k, variant):
    #version = "Original"
    #version = "Only_X"
    #version = "Order_and_Chaos_Order_First"
    #version = "Order_and_Chaos_Chaos_First"
    #Misere = False
    #more_symmetries_removed = True
    """
    KEY:
    [1] Original
    [2] Only_X
    [3] Misere
    [4] Misere Only_X
    [5] Order_and_Chaos_Order_First
    [6] Order_and_Chaos_Chaos_First
    [0] EXIT

    """
    
    print(Solve(board, k, variant, True, False))

def print_tic_tac_toe_board(board):
    printed_board = copy.deepcopy(board)
    def colorize(symbol):
        if symbol == 'X':
            return "\033[91mX\033[0m"  # Red X
        elif symbol == 'O':
            return "\033[93mO\033[0m"  # Yellow O
        return symbol

    for i in range(3):
        for j in range(3):
            printed_board[i][j] = colorize(board[i][j])

    for i in range(3):
        row = " {} | {} | {} ".format(printed_board[i][0], printed_board[i][1], printed_board[i][2])
        print(row)
        if i < 2:
            print("\u2501"*11)  # Use em-dashes to create filled horizontal lines without spaces
    print('\n' * 1)
        
def win_screen(player):
    print("GAME OVER!")
    print(f"{player} won the game!")
def tie_screen():
    print("GAME OVER")
    print("TIE GAME!")
def determine_mark_by_variant(variant, player_turn):
    if variant == "Original" or variant == "Misere":
        return "X" if player_turn else "O"
    elif variant == "Only_X" or variant == "Misere Only_X":
        return "X"
    else: #order and chaos
        mark = ""
        player = "Order" if ((variant == "Order_and_Chaos_Order_First" and player_turn) or (variant == "Order_and_Chaos_Chaos_First" and not player_turn)) else "Chaos"
        while mark != "X" and mark != "O":
            mark = input(f"{player}, Please choose whether you'd like to be 'X' or 'O' for this turn!")
        return mark


def convert_board_for_solver(board):
    rowLen, colLen = len(board), len(board[0])
    new_board = [[" " for _ in range(colLen)] for _ in range(rowLen)]
    for r in range(rowLen):
        for c in range(colLen):
            if board[r][c] == "X":
                new_board[r][c] = True
            if board[r][c] == "O":
                new_board[r][c] = False
    return new_board
def getPlayer(game_option, player_turn):
    if game_option == "Human vs. Computer":
        player  = "Human" if player_turn else "Computer"
    else:
        player = "Player 1" if player_turn else "Player 2"
    return player

def printPrediction(board, player, variant):
    solver_board = convert_board_for_solver(board)
    prediction = Solve(solver_board, 3, variant, False, False, True)
    print("PREDICTION", prediction)
    res, num = prediction[0], prediction[1]
    if res == "W":
        print(f"{player} should Win in {num}")
    elif res == "T":
        print(f"{player} should Tie in {num}")
    else:
        print(f"{player} will Lose in {num}")
    print('\n')

def playGame(game_option, player_turn, variant, predictions_on):
    board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
    game_over = False
    possible_points = {"0", "1", "2"}
    num_moves = 0
    print_tic_tac_toe_board(board)
    prev_move = None
    while not game_over:
        newBoard = []

        player = getPlayer(game_option, player_turn)
        if predictions_on:
            printPrediction(board, player, variant)
        while not newBoard:
            if game_option == "Human vs. Computer" and not player_turn:
                #computer needs to make optimal move to win, if many optimal moves are available, computer chooses one of them at rando
                mark = determine_mark_by_variant(variant, player_turn)
                solver_board = convert_board_for_solver(board)
                ai_optimal_move = Solve(solver_board, 3, variant, False, True)
                newBoard = DoMove(board, ai_optimal_move, mark)

            else:   #two players
                row, col = "", ""
                while row not in possible_points:
                    player = "Player 1" if player_turn else "Player 2"
                    mark = determine_mark_by_variant(variant, player_turn)
                    row = input(f"{player}, please enter the row (0-2) of where you'd like to move:" + space)
                    if row == "U":
                        if prev_move:
                            prev_player = "Player 1" if player == "Player 2" else "Player 2"
                            prev_mark = determine_mark_by_variant(variant, not player_turn)
                            ip = input(f"{prev_player}, please confirm if you'd like to undo the last move, [Y/N]:" + space + '\n')
                            if ip == "Y":
                                newBoard = undoMove(board, prev_move, prev_mark)
                                board = newBoard
                                print_tic_tac_toe_board(board)
                                player_turn = not player_turn
                                prev_move = None #ensures that you cannot undo multiple moves at once
                        else:
                            print("First Move Hasn't Been Made or Can't Undo Multiple Moves!\n")
        
                while col not in possible_points:
                    col = input(f"{player}, please enter the column (0-2) of where you'd like to move:" + space)
                print('\n')
                row, col = int(row, 10), int(col, 10)
                prev_move = (row, col)
                newBoard = DoMove(board, (row, col), mark)
        board = newBoard
        print_tic_tac_toe_board(board)
        if predictions_on:
            printPrediction(board, player, variant)
        num_moves += 1 
        if variant == "Original":
            game_over = checkWin(board, mark, 3)
        elif variant == "Only_X":
            game_over = checkWin(board, "X", 3)
        elif variant == "Misere" or variant == "Misere Only_X": #game over here means you lost
            if variant == "Misere":
                game_over = checkWin(board, mark, 3)  
            else:
                game_over = checkWin(board, "X", 3)
            if game_over:
                player_turn = not player_turn
                #the winner is the player not making the move!
                player = getPlayer(game_option, player_turn)
                win_screen(player)
                break
            
        elif variant == "Order_and_Chaos_Order_First" or variant == "Order_and_Chaos_Chaos_First":
            game_over = checkWin(board, "X", 3) or checkWin(board, "O", 3)  
            if game_over:
                player = "Order"     
            if num_moves == 9:
                win_screen("Chaos")
                break

        if game_over:
            win_screen(player)
            break 
        if num_moves == 9:
            tie_screen()
            break
        player_turn = not player_turn
    

def main():
    menu()
    variant = ""
    possible_variants = {f"{num}" for num in range(7)}
    while variant not in possible_variants:
        variant = input()
    variant = convert_variant(variant)
    options()
    option = ""
    while option != "S" and option != "P":
        option = input()
    if option == "S":
        new_board = [[" " for _ in range(3)] for _ in range(3)]
        solveGame(new_board, 3, variant) #basic 3x3 tic tac toe
    else:   #option == P
        instructions()
        play_game_menu()
        game_option = ""
        while game_option != "0" and game_option != "1":
            game_option = input()
        goes_first = ""
        if game_option == "1":
            who_goes_first()
            while goes_first != "Y" and goes_first != "N":
                goes_first = input()
        predictions_on = ""
        while predictions_on != "Y" and predictions_on != "N":
            predictions_on = input("Would you like predictions on? [Y/N]:" + space)

        game_option = "Human vs. Computer" if game_option == "1" else "Human vs. Human"
        goes_first = False if goes_first == "N" else True
        playGame(game_option, goes_first, variant, predictions_on)
main()




"""
NOTES:
- currently have working implementation for Human vs. Human on original

need to implement variants for HUman vs. Human as well as for human vs. AI.  ******DONE******
also need to implement how human vs. AI will work using the solver.          ******DONE******

need to rewrite solver6.py so as to work with "X" and "O" instead of T/F     ******DONE****** 

need to work add undo button                                                 ******DONE******

"""
