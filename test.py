def print_tic_tac_toe_board(board, prediction):
    color_codes = {
        'X': '\x1b[31m',  # Red for X
        'O': '\x1b[33m',  # Orange for O
    }

    for row in range(3):
        for col in range(3):
            cell = board[row][col]
            if cell == ' ':
                print(f'{row * 3 + col + 1}', end=' ')
            else:
                color_code = color_codes.get(cell, '')  # Get the color code
                print(f'{color_code}{cell}\x1b[0m', end=' ')

            if col < 2:
                print('|', end=' ')
        print()
        if row < 2:
            print('— — — — — — — — —')

    print(f'\nPrediction: Player {prediction[0]} Will Win in {prediction[1]}')



board = [['X', 'O', ' '], ['X', ' ', 'O'], [' ', 'X', 'O']]
prediction = 'Player 1 Will Win in 5'
print_tic_tac_toe_board(board, prediction)


