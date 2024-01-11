from tictactoe6 import *
from random import seed
from random import randint
def Solve(position, k, version, print_table, get_optimal_AI_move, predictions_on): 
    """"
    position is the current state of the board
    Function: returns the value of (position) based on exhaustively searching the tree. It will call DoMove, GenerateMoves, and PrimitiveValue as needed.
    """
    more_symmetries_removed = True
    AI_optimal_moves = {"W": [], "T": [], "L": []}   
    prediction = {"W": None, "T": None, "L": None}
    num_moves = 0 
    rowLen, colLen = len(position), len(position[0])
    player = 0
    for row in range(rowLen):
        for col in range(colLen):
            if position[row][col] != " ":
                if position[row][col] == True:
                    player += 1
                else:
                    player -= 1
                num_moves += 1
    #even moves == player1 --> true, else player2--> false
    def rotate(board):
        rowLen, colLen = len(board), len(board[0])
        #rotates board cc 90 degrees
        newBoard = [[" " for _ in range(rowLen)] for _ in range(colLen)]
        newCol, newRow = 0, 0
        for col in range(colLen - 1, -1, -1):
            newCol = 0
            for row in range(rowLen):
                newBoard[newRow][newCol] = board[row][col]
                newCol += 1
            newRow += 1
        return newBoard
    
    def reflectHorizantal(board):
        rowLen, colLen = len(board), len(board[0])
        for col in range(colLen):
            for row in range(rowLen//2):
                board[row][col], board[-(row + 1)][col] = board[-(row + 1)][col], board[row][col]
        return board

    def reflectVertical(board):
        rowLen, colLen = len(board), len(board[0])
        for row in range(rowLen):
            for col in range(colLen // 2):
                board[row][col], board[row][-(col + 1)] = board[row][-(col + 1)], board[row][col]
        return board
    def flip(board):
        rowLen, colLen = len(board), len(board[0])
        flipped_board = [[" " for _ in range(colLen)] for _ in range(rowLen)]
        for row in range(rowLen):
            for col in range(colLen):
                if board[row][col] != " ":
                    flipped_board[row][col] = not board[row][col]

        return flipped_board
    def reflect(board):
        rowLen, colLen = len(board), len(board[0])
        reflected_board = [[" " for _ in range(colLen)] for _ in range(rowLen)]

        for i in range(rowLen):
            for j in range(colLen):
                reflected_board[i][j] = board[j][i]
        return reflected_board

    
    mem = {}
    def check_canonical(player, board):
        rotations = (90, 180, 270, 360)
        temp = board
        for _ in rotations:         #Deals with only rotations
            temp = rotate(temp)
            strBoard = str(temp)
            if (player, strBoard) in mem:
                return (player, strBoard)
        
        #at this point the board should be back to its OG position            
        
        for _ in rotations:     #rotations + reflection
            temp = rotate(temp)
            newBoard = reflect(temp)   #deep copy is made 
            strBoard = str(newBoard)
            if (player, strBoard) in mem:
                return (player, strBoard)
        return -1

    def canonical(player, board):
        strBoard = str(board)
        if (player, strBoard) in mem:
            return (player, strBoard)
     
        if len(board) != len(board[0]):
            for num in range(4):
                if num % 2 == 0:
                    board = reflectVertical(board)
                else:
                    board = reflectHorizantal(board)
                strBoard = str(board)
                if (player, strBoard) in mem:
                    return (player, strBoard)
        else:
            if (version == "Order_and_Chaos_Order_First" or version == "Order_and_Chaos_Chaos_First") and more_symmetries_removed:
                temp = board
                ret = check_canonical(player, board)
                if ret != -1:
                    return ret
                ret =  check_canonical(player, flip(temp))
                if ret != -1:
                    return ret
            
            else:
                ret = check_canonical(player, board)
                if ret != -1:
                    return ret
        return (player, str(board)) #canonical form hasn't been added yet 
    remove_symmetries = True
    def solver(board, player, intital_board):  
        key = canonical(player, board) if remove_symmetries else (player, str(board))
     
        if key in mem:
            return mem[key]        
        primVal = PrimitiveValue(board, k, version)
        if primVal != -1:
            mem[key] = [primVal, 0]
            return mem[key]
        possible_moves = GenerateMoves(board)
        tie_seen = False
        lost_seen = False
        min_remoteness_W, max_remoteness_L, min_remoteness_T = float('inf'), float('-inf'), float('inf')
        marks = {True, False}

        for move in possible_moves:
            if version == "Order_and_Chaos_Order_First" or version == "Order_and_Chaos_Chaos_First":
                for mark in marks:      #in this version of the game, the player can decide to mark down an X or O (T or F)
                    newBoard = DoMove(board, move, mark)        
                    ret = solver(newBoard, not player, intital_board)
                    result, remoteness = ret[0], ret[1]
                    if result == 'L':
                        if remoteness < min_remoteness_W:
                            min_remoteness_W = remoteness
                            if board == intital_board:
                                AI_optimal_moves['W'] = [move]
                            if predictions_on:
                                prediction["W"] = min_remoteness_W
                        elif remoteness == min_remoteness_W and board == intital_board:
                            AI_optimal_moves["W"].append(move)        
                        lost_seen = True
                    elif result == 'T':
                        if remoteness < min_remoteness_T:
                            min_remoteness_T = remoteness
                            if board == intital_board:
                                AI_optimal_moves["T"] = [move]
                            if predictions_on:
                                prediction["T"] = min_remoteness_T
                        elif remoteness == min_remoteness_T and board == intital_board:
                            AI_optimal_moves["T"].append(move)
                        tie_seen = True
                    else:
                        if remoteness > max_remoteness_L:
                            max_remoteness_L = remoteness
                            if board == intital_board:
                                AI_optimal_moves["L"] = [move]
                            if predictions_on:
                                prediction["L"] = max_remoteness_L
                        elif remoteness == max_remoteness_L and board == intital_board:
                            AI_optimal_moves["L"].append(move)
                    
            else:#not order and chaos (ttl)
                newBoard = DoMove(board, move, player)
                ret = solver(newBoard, True, intital_board) if version == "Only_X" else solver(newBoard, not player, intital_board)
                result, remoteness = ret[0], ret[1]
                if result == 'L':
                    if remoteness < min_remoteness_W:
                        min_remoteness_W = remoteness
                        if board == intital_board:
                            AI_optimal_moves['W'] = [move]
                        if predictions_on:
                            prediction["W"] = min_remoteness_W
                    elif remoteness == min_remoteness_W and board == intital_board:
                        AI_optimal_moves["W"].append(move)        
                    lost_seen = True
                elif result == 'T':
                    if remoteness < min_remoteness_T:
                        min_remoteness_T = remoteness
                        if board == intital_board:
                            AI_optimal_moves["T"] = [move]
                        if predictions_on:
                            prediction["T"] = min_remoteness_T
                    elif remoteness == min_remoteness_T and board == intital_board:
                        AI_optimal_moves["T"].append(move)
                    tie_seen = True
                else:
                    if remoteness > max_remoteness_L:
                        max_remoteness_L = remoteness
                        if board == intital_board:
                            AI_optimal_moves["L"] = [move]
                        if predictions_on:
                            prediction["L"] = max_remoteness_L
                    elif remoteness == max_remoteness_L and board == intital_board:
                        AI_optimal_moves["L"].append(move)
                
        if lost_seen:
            mem[key] = ['W', min_remoteness_W + 1]
            
        elif tie_seen:
            mem[key] = ['T', min_remoteness_T + 1]

        else:
            mem[key] = ['L', max_remoteness_L + 1]
        return mem[key]
        
        
    player = (num_moves % 2 == 0) if version == "Original" else True
    value = solver(position, player, position)
    
    if print_table:
        hashmap = {}
        for board in mem:
            result, remoteness = mem[board][0], mem[board][1]
            if remoteness not in hashmap:
                hashmap[remoteness] = [0, 0, 0] #WIN, LOSS, TIE
            if result == 'W':
                hashmap[remoteness][0] += 1
            elif result == 'L':
                hashmap[remoteness][1] += 1
            else:
                hashmap[remoteness][2] += 1
        ret = ""
        miniSpace = '   '
        space = '         '
        ret += '______________________________________\n'
        ret += 'Remote' + miniSpace + 'Win' + '     ' + 'Lose' + '     ' + 'Tie' + '    ' + 'Total\n'
        total_wins, total_losses, total_ties = 0, 0, 0
        sorted_map = sorted(hashmap.items(), key = lambda x: x)
        for index in range(len(sorted_map) -1, -1, -1):
            remoteness = sorted_map[index][0]
            lst = hashmap[remoteness]
            win, lose, tie = lst[0], lst[1], lst[2]
            total_wins += win
            total_losses += lose
            total_ties += tie
            ret += (f"{remoteness}" + space + f"{win}" + '       ' + f"{lose}" + '      ' + f"{tie}" + '      ' + f"{win + lose + tie}\n")
        ret += '______________________________________\n'
        ret += ('Total' + '    ' + f"{total_wins}" + '      ' + f"{total_losses}" + '      ' + f"{total_ties}" + '     ' + f"{total_wins + total_losses + total_ties}\n")
        return ret
    if get_optimal_AI_move: #for computer vs. human
        seed(1)
        win_moves, lose_moves, tie_moves = AI_optimal_moves["W"],  AI_optimal_moves["L"],  AI_optimal_moves["T"]
        if win_moves:
            rand_index = randint(0, len(win_moves) - 1)
            return win_moves[rand_index]
        elif tie_moves:
            rand_index = randint(0, len(tie_moves) - 1)
            return tie_moves[rand_index]
        else:
            rand_index = randint(0, len(lose_moves) - 1)
            return lose_moves[rand_index]
    if predictions_on:
        hashmap = {}

        for board in mem:
            result, remoteness = mem[board][0], mem[board][1]
            if remoteness not in hashmap:
                hashmap[remoteness] = [0, 0, 0] #WIN, LOSS, TIE
            if result == 'W':
                hashmap[remoteness][0] += 1
            elif result == 'L':
                hashmap[remoteness][1] += 1
            else:
                hashmap[remoteness][2] += 1
        print(hashmap)
        print(max(hashmap))
        max_remoteness = max(hashmap)
        res = hashmap[max_remoteness]
        return f"W{max_remoteness}" if res[0] else f"T{max_remoteness}" if res[2] else f"L{max_remoteness}" 
    return value


