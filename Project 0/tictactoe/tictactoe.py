"""
Tic Tac Toe Player
"""

import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] != EMPTY:
                count += 1
    
    if board == initial_state():
        return X
    if count % 2 == 1:
        return O
    else:
        return X
    

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                moves.add((i, j))
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Invalid Action!!!")

    b2 = copy.deepcopy(board)
    b2[action[0]][action[1]] = player(board)
    
    return b2


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if checkRows(board, X) or checkColumns(board, X) or checkTopToBottomDiagonal(board, X) or checkBottomToTopDiagonal(board, X):
        return X
    elif checkRows(board, O) or checkColumns(board, O) or checkTopToBottomDiagonal(board, O) or checkBottomToTopDiagonal(board, O):
        return O
    else:
        return None


def checkRows(board, player):
    for i in range(len(board)):
        count = 0
        for j in range(len(board[0])):
            if board[i][j] == player:
                count += 1
        if count == len(board[0]):
            return True 
    return False


def checkColumns(board, player):
    for j in range(len(board[0])):
        count = 0
        for i in range(len(board)):
            if board[i][j] == player:
                count += 1
        if count == len(board):
            return True
    return False


def checkTopToBottomDiagonal(board, player):
    count = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if i == j and board[i][j] == player:
                count += 1
    return count == len(board[0])


def checkBottomToTopDiagonal(board, player):
    count = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if (len(board) - i - 1) == j and board[i][j] == player:
                count += 1
    return count == len(board[0])


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if (winner(board) == X):
        return True
    elif (winner(board) == O):
        return True
        
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if (winner(board) == X):
        return 1
    elif (winner(board) == O):
        return -1
    else:
        return 0


def minimax(board):
    """
    Retorna a jogada ótima para o jogador atual no tabuleiro.
    """
    if terminal(board):
        return None

    if player(board) == X:
        return max_value(board)[1]  
    else:
        return min_value(board)[1]  


def max_value(board):
    """
    Retorna o melhor valor e a melhor jogada para X no tabuleiro.
    """
    if terminal(board):
        return utility(board), None  

    max_val = float('-inf')
    best_move = None

    for action in actions(board):
        # Avalia o movimento atual e calcula o valor para o próximo jogador (O)
        val = min_value(result(board, action))[0]
        
        if val > max_val:
            max_val = val
            best_move = action

    return max_val, best_move


def min_value(board):
    """
    Retorna o melhor valor e a melhor jogada para O no tabuleiro.
    """
    if terminal(board):
        return utility(board), None  

    min_val = float('inf')
    best_move = None

    for action in actions(board):
        # Avalia o movimento atual e calcula o valor para o próximo jogador (X)
        val = max_value(result(board, action))[0]
        
        if val < min_val:
            min_val = val
            best_move = action

    return min_val, best_move
