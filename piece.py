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

def avail_pawn(board, available_moves, piece_col, piece_row):
    if (piece_row > 0):
        if (board[piece_row - 1][piece_col] == 0):
            available_moves[piece_row - 1][piece_col] = 1
        if (piece_col > 0):
            if (board[piece_row - 1][piece_col - 1] > 0):
                available_moves[piece_row - 1][piece_col - 1] = 1
        if (piece_col < TOT_COLS - 1):
            if (board[piece_row - 1][piece_col + 1] > 0):
                available_moves[piece_row - 1][piece_col + 1] = 1      
    return available_moves


def avail_knight(board, available_moves, piece_col, piece_row):
    
    # up
    if (piece_row - 2 > 0):
        if (piece_col - 1 > 0):
            if (board[piece_row - 2][piece_col - 1] == 0 or board[piece_row - 2][piece_col - 1] > 0):
                available_moves[piece_row - 2][piece_col - 1] = 1
        if (piece_col + 1 < TOT_COLS - 1):
            if (board[piece_row - 2][piece_col + 1] == 0 or board[piece_row - 2][piece_col + 1] > 0):
                available_moves[piece_row - 2][piece_col + 1] = 1        
    # down
    if (piece_row + 2 < TOT_ROWS - 1):
        if (piece_col - 1 > 0):
            if (board[piece_row + 2][piece_col - 1] == 0 or board[piece_row + 2][piece_col - 1] > 0):
                available_moves[piece_row + 2][piece_col - 1] = 1
        if (piece_col + 1 < TOT_COLS - 1):
            if (board[piece_row + 2][piece_col + 1] == 0 or board[piece_row + 2][piece_col + 1] > 0):
                available_moves[piece_row + 2][piece_col + 1] = 1

    # right
    if (piece_col + 2 < TOT_COLS - 1):
        if (piece_row - 1 > 0):
            if (board[piece_row - 1][piece_col + 2] == 0 or board[piece_row - 1][piece_col + 2] > 0):
                available_moves[piece_row - 1][piece_col + 2] = 1
        if (piece_row + 1 < TOT_ROWS - 1):
            if (board[piece_row + 1][piece_col + 2] == 0 or board[piece_row + 1][piece_col + 2] > 0):
                available_moves[piece_row + 1][piece_col + 2] = 1

    # left
    if (piece_col - 2 > 0):
        if (piece_row - 1 > 0):
            if (board[piece_row - 1][piece_col - 2] == 0 or board[piece_row - 1][piece_col - 2] > 0):
                available_moves[piece_row - 1][piece_col - 2] = 1
        if (piece_row + 1 < TOT_ROWS - 1):
            if (board[piece_row + 1][piece_col - 2] == 0 or board[piece_row + 1][piece_col - 2] > 0):
                available_moves[piece_row + 1][piece_col - 2] = 1
    return available_moves


def avail_horizontal(board, available_moves, piece_col, piece_row):
    for c in range(piece_col + 1, TOT_COLS):
        if (board[piece_row][c] < 0):
            break
        available_moves[piece_row][c] = 1
        if (board[piece_row][c] > 0):
            break
    for c in reversed(range(piece_col)):
        if (board[piece_row][c] < 0):
            break
        available_moves[piece_row][c] = 1
        if (board[piece_row][c] > 0):
            break
    return available_moves


def avail_vertical(board, available_moves, piece_col, piece_row):
    for r in reversed(range(piece_row)):
        if (board[r][piece_col] < 0):
            break
        available_moves[r][piece_col] = 1
        if (board[r][piece_col] > 0):
            break
    for r in range(piece_row + 1, TOT_ROWS):
        if (board[r][piece_col] < 0):
            break
        available_moves[r][piece_col] = 1
        if (board[r][piece_col] > 0):
            break
    return available_moves


def avail_diagonal(board, available_moves, piece_col, piece_row):
    start_row = piece_row
    start_col = piece_col
    
    row = start_row
    col = start_col
    while row < TOT_ROWS - 1 and col < TOT_COLS - 1:
        row += 1
        col += 1
        if (board[row][col] < 0):
            break
        available_moves[row][col] = 1
        if (board[row][col] > 0):
            break        

    row = start_row
    col = start_col
    while row > 0 and col < TOT_COLS - 1:
        row -= 1
        col += 1
        if (board[row][col] < 0):
            break
        available_moves[row][col] = 1
        if (board[row][col] > 0):
            break

    row = start_row
    col = start_col
    while row < TOT_ROWS - 1 and col > 0:
        row += 1
        col -= 1
        if (board[row][col] < 0):
            break
        available_moves[row][col] = 1
        if (board[row][col] > 0):
            break

    row = start_row
    col = start_col
    while row > 0 and col > 0:
        row -= 1
        col -= 1
        if (board[row][col] < 0):
            break
        available_moves[row][col] = 1
        if (board[row][col] > 0):
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

    def is_valid_move(self, board, start, to):
        return False

    def is_white(self):
        return self.color

    def get_value(self):
        return self.value

    def get_name(self):
        return self.name

    def get_index(self):
        return self.index

    def get_position(self):
        return self.position

    def get_row(self):
        return self.row

    def get_column(self):
        return self.column

    def get_available_moves(self, board, sim = False, sim_col = None, sim_row = None):
        return np.zeros((TOT_ROWS, TOT_COLS))

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
            available_moves = avail_horizontal(board, available_moves, sim_col, sim_row)
            available_moves = avail_vertical(board, available_moves, sim_col, sim_row)
        else:
            available_moves = avail_horizontal(board, available_moves, self.column, self.row)
            available_moves = avail_vertical(board, available_moves, self.column, self.row)
        return available_moves

    def is_valid_move(self, board, start, to):
        if start[0] == to[0] or start[1] == to[1]:
            return check_updown(board, start, to)
        print(incorrect_path)
        return False

class Knight(Piece):
    def __init__(self, color,  position, row, column):
        super().__init__(color, PIECES[2], 2,  position, row, column)

    def get_available_moves(self, board, sim = False, sim_col = None, sim_row = None):
        available_moves = np.zeros((TOT_ROWS, TOT_COLS))
        if sim:
            available_moves = avail_knight(board, available_moves, sim_col, sim_row)
        else:
            available_moves = avail_knight(board, available_moves, self.column, self.row)
        return available_moves

    def is_valid_move(self, board, start, to):
        if abs(start[0] - to[0]) == 2 and abs(start[1] - to[1]) == 1:
            return True
        if abs(start[0] - to[0]) == 1 and abs(start[1] - to[1]) == 2:
            return True
        print(incorrect_path)
        return False

class Bishop(Piece):
    def __init__(self, color,  position, row, column):
        super().__init__(color, PIECES[3], 3,  position, row, column)

    def get_available_moves(self, board, sim = False, sim_col = None, sim_row = None):
        available_moves = np.zeros((TOT_ROWS, TOT_COLS))
        if sim:
            available_moves = avail_diagonal(board, available_moves, sim_col, sim_row)
        else:
            available_moves = avail_diagonal(board, available_moves, self.column, self.row)
        return available_moves

    def is_valid_move(self, board, start, to):
        return check_diag(board, start, to)

class Queen(Piece):
    def __init__(self, color,  position, row, column):
        super().__init__(color, PIECES[5], 5,  position, row, column)

    def get_available_moves(self, board, sim = False, sim_col = None, sim_row = None):
        available_moves = np.zeros((TOT_ROWS, TOT_COLS))
        if sim:
            available_moves = avail_horizontal(board, available_moves, sim_col, sim_row)
            available_moves = avail_vertical(board, available_moves, sim_col, sim_row)
            available_moves = avail_diagonal(board, available_moves, sim_col, sim_row)
        else:
            available_moves = avail_diagonal(board, available_moves, self.column, self.row)
            available_moves = avail_horizontal(board, available_moves, self.column, self.row)
            available_moves = avail_vertical(board, available_moves, self.column, self.row)
        return available_moves

    def is_valid_move(self, board, start, to):
        # diagonal
        if abs(start[0] - to[0]) == abs(start[1] - to[1]):
            return check_diag(board, start, to)

        # up/down
        elif start[0] == to[0] or start[1] == to[1]:
            return check_updown(board, start, to)
        print(incorrect_path)
        return False

class Pawn(Piece):
    def __init__(self, color,  position, row, column):
        super().__init__(color, PIECES[1], 1,  position, row, column)

    def get_available_moves(self, board, sim = False, sim_col = None, sim_row = None):
        available_moves = np.zeros((TOT_ROWS, TOT_COLS))
        if sim:
            available_moves = avail_pawn(board, available_moves, sim_col, sim_row)
        else:
            available_moves = avail_pawn(board, available_moves, self.column, self.row)
        return available_moves

    def is_valid_move(self, board, start, to):
        if self.color:
            # diagonal move
            if start[0] == to[0] + 1 and (start[1] == to[1] + 1 or start[1] == to[1] - 1):
                if board.board[to[0]][to[1]] != None:
                    self.first_move = False
                    return True
                print("Cannot move diagonally unless taking.")
                return False

            # vertical move
            if start[1] == to[1]:
                if (start[0] - to[0] == 2 and self.first_move) or (start[0] - to[0] == 1):
                    for i in range(start[0] - 1, to[0] - 1, -1):
                        if board.board[i][start[1]] != None:
                            print(blocked_path)
                            return False
                    # insert a GhostPawn
                    if start[0] - to[0] == 2:
                        board.board[start[0] - 1][start[1]] = GhostPawn(self.color)
                        board.white_ghost_piece = (start[0] - 1, start[1])
                    self.first_move = False
                    return True
                print("Invalid move" + " or " + "Cannot move forward twice if not first move.")
                return False
            print(incorrect_path)
            return False

        else:
            if start[0] == to[0] - 1 and (start[1] == to[1] - 1 or start[1] == to[1] + 1):
                if board.board[to[0]][to[1]] != None:
                    self.first_move = False
                    return True
                print(blocked_path)
                return False
            if start[1] == to[1]:
                if (to[0] - start[0] == 2 and self.first_move) or (to[0] - start[0] == 1):
                    for i in range(start[0] + 1, to[0] + 1):
                        if board.board[i][start[1]] != None:
                            print(blocked_path)
                            return False
                    # insert a GhostPawn
                    if to[0] - start[0] == 2:
                        board.board[start[0] + 1][start[1]] = GhostPawn(self.color)
                        board.black_ghost_piece = (start[0] + 1, start[1])
                    self.first_move = False
                    return True
                print("Invalid move" + " or " + "Cannot move forward twice if not first move.")
                return False
            print(incorrect_path)
            return False

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