"""
Tic Tac Toe Player
"""

import math
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
    # Count number of Xs and Os on the board
    x_count = 0
    o_count = 0

    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                x_count += 1
            elif board[i][j] == O:
                o_count += 1

    # If both counts equal, then it is X's turn as X starts first
    if x_count == o_count:
        return X

    # If X count is greater than O count, then it is O's turn as O starts second
    elif x_count > o_count:
        return O

    # Otherwise, board state is invalid
    else:
        raise ValueError("Current board state is not permitted.")


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = set()

    # Determine which spaces are EMPTY
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_moves.add((i, j))

    return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Copy of board before the move
    modified_board = copy.deepcopy(board)

    # Check if move is allowed, otherwise raise an exception
    possible_moves = actions(board)
    if not action in possible_moves:
        raise ValueError("Move not allowed as space is already full.")

    # If move is allowed, move is updated on board copy
    else:
        i, j = action
        modified_board[i][j] = player(board)

    return modified_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Set 2 counters for downward slanting and upward slanting diagonals
    x_diagonal_count1 = 0
    o_diagonal_count1 = 0
    x_diagonal_count2 = 0
    o_diagonal_count2 = 0

    # Count diagonals
    for i in range(3):
        if board[i][i] == X:
            x_diagonal_count1 += 1
        elif board[i][i] == O:
            o_diagonal_count1 += 1

        if board[2 - i][i] == X:
            x_diagonal_count2 += 1
        elif board[2 - i][i] == O:
            o_diagonal_count2 += 1

    # Check if any diagonal has a winner
    if x_diagonal_count1 == 3 or x_diagonal_count2 == 3:
        return X
    elif o_diagonal_count1 == 3 or o_diagonal_count2 == 3:
        return O

    # Count rows and columns
    for i in range(3):
        x_column_count = 0
        o_column_count = 0
        x_row_count = 0
        o_row_count = 0

        for j in range(3):
            if board[j][i] == X:
                x_column_count += 1
            elif board[j][i] == O:
                o_column_count += 1

            if board[i][j] == X:
                x_row_count += 1
            elif board[i][j] == O:
                o_row_count += 1

        # Check if any row or column has a winner
        if x_column_count == 3 or x_row_count == 3:
            return X
        elif o_column_count == 3 or o_row_count == 3:
            return O

    # If no winner found, return None
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check if winner has been found
    if winner(board) != None:
        return True

    # Otherwise, check if all spaces are filled
    else:
        if len(actions(board)) > 0:
            return False
        else:
            return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Return respective integer value for winner
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # Game has ended, so no optmial moves
    if terminal(board):
        return None

    # If game still continues
    else:
        current_player = player(board)
        optimal_action = None

        # Using MAX method if current player is X
        if current_player == X:
            best_v = -math.inf

            # Check every possible action or scenario
            for action in actions(board):
                v = min_value(result(board, action))

                # Determine optimal action from highest value
                if v > best_v:
                    best_v = v
                    optimal_action = action

        # Finding min from max method if current player is O
        elif current_player == O:
            best_v = math.inf

            # Check every possible action or scenario
            for action in actions(board):
                v = max_value(result(board, action))

                # Determine optimal action from highest value
                if v < best_v:
                    best_v = v
                    optimal_action = action

        return optimal_action


def max_value(board):
    """
    Returns the maximum value of all actions.
    """
    # If game has ended, action value is the value of the winner
    if terminal(board):
        return utility(board)

    # Otherwise, find the action with highest possible value
    else:
        # Initialize value to lowest possible.
        v = -math.inf

        # Recursively check every action for maximum value
        for action in actions(board):
            v = max(v, min_value(result(board, action)))

    return v


def min_value(board):
    """
    Returns the minimum value of all actions.
    """
    # If game has ended, action value is the value of the winner
    if terminal(board):
        return utility(board)

    # Otherwise, find the action with lowest possible value
    else:
        # Initialize value to highest possible.
        v = math.inf

        # Recursively check every action for minimum value
        for action in actions(board):
            v = min(v, max_value(result(board, action)))

    return v
