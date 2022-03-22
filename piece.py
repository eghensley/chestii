#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 18:22:22 2022

@author: ehens86
"""


from constants import PIECES, TOT_COLS, TOT_ROWS
import numpy as np


blocked_path = "There's a piece in the path."
incorrect_path = "This piece does not move in this pattern."


#TODO account for human player moves

def avail_pawn(board, available_moves, piece_col, piece_row, team):
    # User's pawns' rules: moving up the baard descending rows
    if (team > 0 and piece_row > 0):
        if (board[piece_row - 1][piece_col] == 0):
            available_moves[piece_row - 1][piece_col] = 1
        if (piece_col > 0):
            if (board[piece_row - 1][piece_col - 1] < 0):
                available_moves[piece_row - 1][piece_col - 1] = 1
        if (piece_col < TOT_COLS - 1):
            if (board[piece_row - 1][piece_col + 1] < 0):
                available_moves[piece_row - 1][piece_col + 1] = 1
    # CPU's pawns' rules: moving down the baard ascending rows
    elif (team < 0 and piece_row < TOT_ROWS - 1):
        if (board[piece_row + 1][piece_col] == 0):
            available_moves[piece_row + 1][piece_col] = 1
        if (piece_col > 0):
            if (board[piece_row + 1][piece_col - 1] > 0):
                available_moves[piece_row + 1][piece_col - 1] = 1
        if (piece_col < TOT_COLS - 1):
            if (board[piece_row + 1][piece_col + 1] > 0):
                available_moves[piece_row + 1][piece_col + 1] = 1
    return available_moves


def avail_knight(board, available_moves, piece_col, piece_row, team):
    
    # up
    if (piece_row - 2 >= 0):
        if (piece_col - 1 > 0):
            if ((team < 0) != (board[piece_row - 2][piece_col - 1] < 0)):
#            if (board[piece_row - 2][piece_col - 1] == 0 or board[piece_row - 2][piece_col - 1] > 0):
                available_moves[piece_row - 2][piece_col - 1] = 1
        if (piece_col + 1 < TOT_COLS):
            if ((team < 0) != (board[piece_row - 2][piece_col + 1] < 0)):
#            if (board[piece_row - 2][piece_col + 1] == 0 or board[piece_row - 2][piece_col + 1] > 0):
                available_moves[piece_row - 2][piece_col + 1] = 1        
    # down
    if (piece_row + 2 < TOT_ROWS):
        if (piece_col - 1 > 0):
            if ((team < 0) != (board[piece_row + 2][piece_col - 1] < 0)):
#            if (board[piece_row + 2][piece_col - 1] == 0 or board[piece_row + 2][piece_col - 1] > 0):
                available_moves[piece_row + 2][piece_col - 1] = 1
        if (piece_col + 1 < TOT_COLS):
            if ((team < 0) != (board[piece_row + 2][piece_col + 1] < 0)):
#            if (board[piece_row + 2][piece_col + 1] == 0 or board[piece_row + 2][piece_col + 1] > 0):
                available_moves[piece_row + 2][piece_col + 1] = 1

    # right
    if (piece_col + 2 < TOT_COLS):
        if (piece_row - 1 > 0):
            if ((team < 0) != (board[piece_row - 1][piece_col + 2] < 0)):
#            if (board[piece_row - 1][piece_col + 2] == 0 or board[piece_row - 1][piece_col + 2] > 0):
                available_moves[piece_row - 1][piece_col + 2] = 1
        if (piece_row + 1 < TOT_ROWS):
            if ((team < 0) != (board[piece_row + 1][piece_col + 2] < 0)):
#            if (board[piece_row + 1][piece_col + 2] == 0 or board[piece_row + 1][piece_col + 2] > 0):
                available_moves[piece_row + 1][piece_col + 2] = 1

    # left
    if (piece_col - 2 >= 0):
        if (piece_row - 1 > 0):
            if ((team < 0) != (board[piece_row - 1][piece_col - 2] < 0)):
#            if (board[piece_row - 1][piece_col - 2] == 0 or board[piece_row - 1][piece_col - 2] > 0):
                available_moves[piece_row - 1][piece_col - 2] = 1
        if (piece_row + 1 < TOT_ROWS):
            if ((team < 0) != (board[piece_row + 1][piece_col - 2] < 0)):
#            if (board[piece_row + 1][piece_col - 2] == 0 or board[piece_row + 1][piece_col - 2] > 0):
                available_moves[piece_row + 1][piece_col - 2] = 1
    return available_moves


def avail_horizontal(board, available_moves, piece_col, piece_row, team):
    for c in range(piece_col + 1, TOT_COLS):
        # Stop when encountering a piece from the same team
        if board[piece_row][c] != 0 and ((team < 0) == (board[piece_row][c] < 0)):
            break      
        available_moves[piece_row][c] = 1
        # If the cell is occupied it, then stop
        if (board[piece_row][c] != 0):
            break
    for c in reversed(range(piece_col)):
        # Stop when encountering a piece from the same team
        if board[piece_row][c] != 0 and ((team < 0) == (board[piece_row][c] < 0)):
            break
        available_moves[piece_row][c] = 1
        # If the cell is occupied it, then stop
        if (board[piece_row][c] != 0):
            break
    return available_moves


def avail_vertical(board, available_moves, piece_col, piece_row, team):
    for r in reversed(range(piece_row)):
        # Stop when encountering a piece from the same team
        if board[r][piece_col] != 0 and ((team < 0) == (board[r][piece_col] < 0)):
            break
        available_moves[r][piece_col] = 1
        # If the cell is occupied it, then stop
        if (board[r][piece_col] != 0):
            break
    for r in range(piece_row + 1, TOT_ROWS):
        # Stop when encountering a piece from the same team
        if board[r][piece_col] != 0 and ((team < 0) == (board[r][piece_col] < 0)):
            break
        available_moves[r][piece_col] = 1
        # If the cell is occupied it, then stop
        if (board[r][piece_col] != 0):
            break
    return available_moves


def avail_diagonal(board, available_moves, piece_col, piece_row, team):
    start_row = piece_row
    start_col = piece_col
    
    row = start_row
    col = start_col
    while row < TOT_ROWS - 1 and col < TOT_COLS - 1:
        row += 1
        col += 1
        # Stop when encountering a piece from the same team
        if board[row][col] != 0 and ((team < 0) == (board[row][col] < 0)):
            break
        available_moves[row][col] = 1
        # If the cell is occupied it, then stop
        if (board[row][col] != 0):
            break      

    row = start_row
    col = start_col
    while row > 0 and col < TOT_COLS - 1:
        row -= 1
        col += 1
        # Stop when encountering a piece from the same team
        if board[row][col] != 0 and ((team < 0) == (board[row][col] < 0)):
            break
        available_moves[row][col] = 1
        # If the cell is occupied it, then stop
        if (board[row][col] != 0):
            break  

    row = start_row
    col = start_col
    while row < TOT_ROWS - 1 and col > 0:
        row += 1
        col -= 1
        # Stop when encountering a piece from the same team
        if board[row][col] != 0 and ((team < 0) == (board[row][col] < 0)):
            break
        available_moves[row][col] = 1
        # If the cell is occupied it, then stop
        if (board[row][col] != 0):
            break  

    row = start_row
    col = start_col
    while row > 0 and col > 0:
        row -= 1
        col -= 1
        # Stop when encountering a piece from the same team
        if board[row][col] != 0 and ((team < 0) == (board[row][col] < 0)):
            break
        available_moves[row][col] = 1
        # If the cell is occupied it, then stop
        if (board[row][col] != 0):
            break  

    return available_moves


class Piece():
    """
    A class to represent a piece in chess
    
    ...
    Attributes:
    -----------
    name : str
        Represents the name of a piece as following - 
        Pawn -> P
        Rook -> R
        Knight -> N
        Bishop -> B
        Queen -> Q
        King -> K
    color : bool
        True if piece is white
    Methods:
    --------
    is_valid_move(board, start, to) -> bool
        Returns True if moving the piece at `start` to `to` is a legal
        move on board `board`
        Precondition: [start] and [to] are valid coordinates on the board.board
    is_white() -> bool
        Return True if piece is white
    """
    def __init__(self, color, conf, index, position, row, column):
        self.name = conf['name']
        self.color = color
        self.value = conf['value']
        self.index = index
        self.position = position
        self.row = row
        self.column = column
        self.alive = True

    def is_alive(self):
        return self.alive

    def kill(self):
        self.alive = False

    def is_cpu(self):
        return self.color

    def get_value(self):
        return self.value

    def get_name(self):
        return self.name

    def get_index(self):
        return self.index

    def get_atomic_index(self):
        return self.index * self.color

#    def get_position(self):
#        return self.position

    def get_row(self):
        return self.row

    def get_column(self):
        return self.column

    def get_available_moves(self, board, sim = False, sim_col = None, sim_row = None):
        return np.zeros((TOT_ROWS, TOT_COLS))

    def is_valid_move(self, board, target_row, target_column):
        # Validate the requested move is valid for piece and board
        valid_moves = self.get_available_moves(board)
        if (valid_moves[target_row][target_column] == 0):
            raise Exception('Cell [%s,%s] is not a valid move for %s in cell [%s,%s]' % (target_row, target_column, self.get_name(), self.get_row(), self.get_column()))
        else:
            return True

    def set_cell(self, new_row, new_column):
        self.row = new_row
        self.column = new_column

    def __str__(self):
        if self.color:
            return self.name
        else:
            return '\033[94m' + self.name + '\033[0m'

class Rook(Piece):
    def __init__(self, color, position, row, column):
        super().__init__(color, PIECES[4], 4, position, row, column)

    def get_available_moves(self, board, sim = False, sim_col = None, sim_row = None):
        available_moves = np.zeros((TOT_ROWS, TOT_COLS))
        if sim:
            available_moves = avail_horizontal(board, available_moves, sim_col, sim_row, self.color)
            available_moves = avail_vertical(board, available_moves, sim_col, sim_row, self.color)
        else:
            available_moves = avail_horizontal(board, available_moves, self.column, self.row, self.color)
            available_moves = avail_vertical(board, available_moves, self.column, self.row, self.color)
        return available_moves


class Knight(Piece):
    def __init__(self, color,  position, row, column):
        super().__init__(color, PIECES[2], 2,  position, row, column)

    def get_available_moves(self, board, sim = False, sim_col = None, sim_row = None):
        available_moves = np.zeros((TOT_ROWS, TOT_COLS))
        if sim:
            available_moves = avail_knight(board, available_moves, sim_col, sim_row, self.color)
        else:
            available_moves = avail_knight(board, available_moves, self.column, self.row, self.color)
        return available_moves


class Bishop(Piece):
    def __init__(self, color,  position, row, column):
        super().__init__(color, PIECES[3], 3,  position, row, column)

    def get_available_moves(self, board, sim = False, sim_col = None, sim_row = None):
        available_moves = np.zeros((TOT_ROWS, TOT_COLS))
        if sim:
            available_moves = avail_diagonal(board, available_moves, sim_col, sim_row, self.color)
        else:
            available_moves = avail_diagonal(board, available_moves, self.column, self.row, self.color)
        return available_moves


class Queen(Piece):
    def __init__(self, color,  position, row, column):
        super().__init__(color, PIECES[5], 5,  position, row, column)

    def get_available_moves(self, board, sim = False, sim_col = None, sim_row = None):
        available_moves = np.zeros((TOT_ROWS, TOT_COLS))
        if sim:
            available_moves = avail_horizontal(board, available_moves, sim_col, sim_row, self.color)
            available_moves = avail_vertical(board, available_moves, sim_col, sim_row, self.color)
            available_moves = avail_diagonal(board, available_moves, sim_col, sim_row, self.color)
        else:
            available_moves = avail_diagonal(board, available_moves, self.column, self.row, self.color)
            available_moves = avail_horizontal(board, available_moves, self.column, self.row, self.color)
            available_moves = avail_vertical(board, available_moves, self.column, self.row, self.color)
        return available_moves


class Pawn(Piece):
    def __init__(self, color,  position, row, column):
        super().__init__(color, PIECES[1], 1,  position, row, column)

    def get_available_moves(self, board, sim = False, sim_col = None, sim_row = None):
        available_moves = np.zeros((TOT_ROWS, TOT_COLS))
        if sim:
            available_moves = avail_pawn(board, available_moves, sim_col, sim_row, self.color)
        else:
            available_moves = avail_pawn(board, available_moves, self.column, self.row, self.color)
        return available_moves


def piece_selector(index, color, position, row, column):
    if index == 1:
        return Pawn(color, position, row, column)
    elif index == 2:
        return Knight(color, position, row, column)
    elif index == 3:
        return Bishop(color, position, row, column)
    elif index == 4:
        return Rook(color, position, row, column)
    elif index == 5:
        return Queen(color, position, row, column)
    else:
        raise Exception("Index [%s] not supported", index)

def resolve_symbol(index):
    return PIECES[abs(index)]['symbol']

def resolve_value(index):
    return PIECES[abs(index)]['value']