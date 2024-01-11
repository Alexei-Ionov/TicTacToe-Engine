def DoMove(board, move, player):
    """
    Function: returns a new position (new_position), the result of making the move from the position
    """
    rowLen, colLen = len(board), len(board[0])
    
    row, col = move[0], move[1]
    if (row >= 0 and row < rowLen and col < colLen and col >= 0) and board[row][col] == " ":    #if in bourds and the position of the board is empty
        newBoard = [[" " for _ in range(colLen)] for _ in range(rowLen)]
        for r in range(rowLen):
            for c in range(colLen):
                newBoard[r][c] = board[r][c]
        newBoard[row][col] = player                                                                                         
        return newBoard
    else:
        print("ERROR: Invalid Move")
def undoMove(board, move, player):
    rowLen, colLen = len(board), len(board[0])
    row, col = move[0], move[1]
    if (row >= 0 and row < rowLen and col < colLen and col >= 0) and board[row][col] == player:    #if in bourds and the position of the board is empty
        newBoard = [[" " for _ in range(colLen)] for _ in range(rowLen)]
        for r in range(rowLen):
            for c in range(colLen):
                newBoard[r][c] = board[r][c]
        newBoard[row][col] = " "                                                                                         
        return newBoard
    else:
        print("ERROR: Invalid Move")

def GenerateMoves(board): 
    """
    Function: returns the set of moves available from the position
    Requires: position is not a primitive position
    """
    possible_moves = set()
    rowLen, colLen = len(board), len(board[0])
    for row in range(rowLen):
        for col in range(colLen):
            if board[row][col] == " ":
                possible_moves.add((row, col))
    return possible_moves

def PrimitiveValue(board, k, version): 
    Misere = True if version == "Misere" or version == "Misere Only_X" else False
    num_moves = 0
    rowLen, colLen = len(board), len(board[0])
    for row in range(rowLen):
        for col in range(colLen):
            if board[row][col] != " ":
                num_moves += 1
    #player = (num_moves % 2 == 0)
    #if player == 1, then it's chaos's turn, else it's order's turn
    win_on_True = checkWin(board, True, k)
    win_on_False = checkWin(board, False, k)
    ret = checkWin(board, not (num_moves % 2 == 0), k) if version == "Original" else win_on_True if version == "Only_X" else (win_on_True or win_on_False)
    if version == "Only_X":
        if Misere:
            return "W" if ret else -1
        return "L" if ret else -1
    
    if version == "Original":
        if Misere:
            return "W" if ret else 'T' if (num_moves == (rowLen * colLen)) else -1
        return "L" if ret else 'T' if (num_moves == (rowLen * colLen)) else -1
        

    if version == "Order_and_Chaos_Order_First":
        #order's turn
        if num_moves % 2 == 0:
            return "W" if ret else "L" if (num_moves == (rowLen * colLen)) else -1
        #chaos's turn
        else:
            return "L" if ret else "W" if (num_moves == (rowLen * colLen)) else -1
        

    elif version == "Order_and_Chaos_Chaos_First":
       
        #chaos's turn
        if num_moves % 2 == 0:
            return "L" if ret else "W" if (num_moves == (rowLen * colLen)) else -1
        #order's turn
        else:
            return "W" if ret else "L" if (num_moves == (rowLen * colLen)) else -1
    


    
        
    #return Lose if prev player WON. if not true and all moves are made then tie. else NOT PRIMITIVE
def checkDiagnolWin(board, player, k, startRow, startCol, dir):

    #BFS TO FIND ALL DIAGNOL WINS
    rowLen, colLen = len(board), len(board[0])
    seen = {(startRow, startCol)}
    queue = [(startRow, startCol)]
    dirxns = [(-1, 0), (0, 1)] if dir == 'UP' else [(1, 0), (0, 1)]
    while queue:
        temp = []
        cnt = 0
        for node in queue:
            row, col = node[0], node[1]
            for dirxn in dirxns:
                newRow, newCol = row + dirxn[0], col + dirxn[1]
                tup = (newRow, newCol)
                if tup not in seen and newRow >= 0 and newCol >= 0 and newRow < rowLen and newCol < colLen:
                    if board[newRow][newCol] == player:
                        cnt += 1
                    else:
                        cnt = 0
                    seen.add(tup)
                    temp.append(tup)
                if cnt >= k:
                    return True
        queue = temp
    return False

def checkWin(board, player, k):
    """"
    for order and chaos, there can be win with either T or F!
    
    """
    rowLen, colLen = len(board), len(board[0])
    #check all possible horizantal wins
    for row in range(rowLen):
        cnt = 0
        for col in range(colLen):
            if board[row][col] == player:
                cnt += 1
            else:
                cnt = 0
            if cnt >= k:
                return True
    #check all possible vertical wins
    for col in range(colLen):
        cnt = 0
        for row in range(rowLen):
            if board[row][col] == player:
                cnt += 1
            else:
                cnt = 0 
            if cnt >= k:
                return True
    return checkDiagnolWin(board, player, k, rowLen - 1, 0, 'UP') or checkDiagnolWin(board, player, k, 0, 0, 'DOWN')
