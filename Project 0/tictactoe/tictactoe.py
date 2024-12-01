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
                moves.add((i,j))
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
    if checkRows(board, X)  or checkColumns(board, X) or checkTopToBottomDiagonal(board, X) or checkBottomToTopDiagonal(board, X):
        return X
    elif checkRows(board, O)  or checkColumns(board, O) or checkTopToBottomDiagonal(board, O) or checkBottomToTopDiagonal(board, O):
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
            if  board[i][j] == None:
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
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    Max = float("-inf")
    Min = float("inf")

    if player(board) == X:
        return Max_Value(board, Max, Min)[1]
    else:
        return Min_Value(board, Max, Min)[1]

def Max_Value(board, Max, Min):
    move = None
    if terminal(board):
        return [utility(board), None];
    v = float('-inf')
    for action in actions(board):
        test = Min_Value(result(board, action), Max, Min)[0]
        Max = max(Max, test)
        if test > v:
            v = test
            move = action
        if Max >= Min:
            break
    return [v, move];

def Min_Value(board, Max, Min):
    move = None
    if terminal(board):
        return [utility(board), None];
    v = float('inf')
    for action in actions(board):
        test = Max_Value(result(board, action), Max, Min)[0]
        Min = min(Min, test)
        if test < v:
            v = test
            move = action
        if Max >= Min:
            break
    return [v, move];