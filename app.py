#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 21:50:23 2022

@author: ehens86
"""
import piece
from constants import PIECES, TOT_ROWS, TOT_COLS, MAX_POINTS, END_COLOR, BORDER_COLOR
import numpy as np
import random
import math

#test = piece.Knight('white')
#test.get_name()

#test = piece.piece_selector(2, False, 1, 1, 1)


class gameboard:

    def __init__(self):
        self._gameboard = np.zeros((TOT_ROWS, TOT_COLS))
    
    def get_board(self):
        return self._gameboard

    def update_board_piece(self, row, col, val):
        self._gameboard[row][col] = val

    def get_board_piece(self, row, col):
        return self._gameboard[row][col]
    
    def to_string(self):
        
        white_square = True
        
        top_bottom = BORDER_COLOR + '_' * TOT_COLS * 10 + END_COLOR
        row_divider = BORDER_COLOR + '-' * TOT_COLS * 10  + END_COLOR
        print(top_bottom)
        print(row_divider)
        for board_row in self._gameboard:
            row_pad = BORDER_COLOR + '||' + END_COLOR
            for col in range(TOT_COLS):
                style = None
                fg = '31'
                bg = None
                if white_square:
                    style = '1'
                    bg = '47'
                else:
                    style = '0'
                    bg = '40'
                row_pad += '\x1b[' + ';'.join([str(style), str(fg), str(bg)]) + 'm' + ' ' * 8 + BORDER_COLOR + END_COLOR + '|' + END_COLOR
            row_pad += BORDER_COLOR + '|' + END_COLOR
            print(row_pad)
            
            
            row_str = BORDER_COLOR + '||' + END_COLOR
            for row_square in board_row:
                
                style = None
                fg = '31'
                bg = None
                color = None

                if white_square:
                    style = '1'
                    bg = '47'
                else:
                    style = '0'
                    bg = '40'
                    
                row_str += '\x1b[' + ';'.join([str(style), str(fg), str(bg)]) + 'm' + ' ' * 3 + END_COLOR
                if row_square < 0:
                    row_str += '\x1b[' + ';'.join([str(style), str(fg), str(bg)]) + 'm' + str(int(row_square)) + END_COLOR
                elif row_square > 0:
                    fg = 32
                    row_str += '\x1b[' + ';'.join([str(style), str(fg), str(bg)]) + 'm' + str(int(row_square)) + END_COLOR
                    row_str += '\x1b[' + ';'.join([str(style), str(fg), str(bg)]) + 'm' + ' ' + END_COLOR
                else:
                    row_str += '\x1b[' + ';'.join([str(style), str(fg), str(bg)]) + 'm' + ' ' * 2 + END_COLOR
                row_str += '\x1b[' + ';'.join([str(style), str(fg), str(bg)]) + 'm' + ' ' * 3 + END_COLOR
                row_str += BORDER_COLOR + '|' + END_COLOR
                
                white_square = not white_square
            row_str += '\x1b[0;30;47m' + '|' + END_COLOR
            print(row_str)
            
            print(row_pad)
            
            print(row_divider)
        print(top_bottom)
    

def create_weights(available_squares, invert = False):
    weights = []
    for square in EMPTY_SQUARES:
        row = math.floor(square / TOT_COLS)
        if (invert):
            row -= (TOT_ROWS - 1)
            row *= -1
        weights.append(row)
    return weights


class game:

    def __init__(self):
        self.POINTS = {
            'RED': 0,
            'BLACK': 0        
        }
        self.ARMIES = {
            'RED': [],
            'BLACK': []       
        }
        self.board = gameboard()
        self.REF_BOARD = np.arange(TOT_ROWS * TOT_COLS).reshape((TOT_ROWS, TOT_COLS))

    def get_board(self):
        return self.board.to_string()

    def set_board_piece(self, row, column, value):
        self.board.update_board_piece(row, column, value)
        
    def get_board_piece(self, row, column):
        return self.board.get_board_piece(row, column)


EMPTY_SQUARES = [i for i in range(TOT_ROWS * TOT_COLS)]


GAME = game()

mult = 1
invert = False
# TODO: enforce peice maxes?
for side in ['RED', 'BLACK']:
    mult *= -1
    invert = not invert
    while GAME.POINTS[side] < MAX_POINTS:
        available_peices = [(k,v) for (k,v) in PIECES.items() if v['value'] <= MAX_POINTS - GAME.POINTS[side]]
        available_peice_weights = [i[1]['weight'] for i in available_peices]
        chosen_piece = random.choices(available_peices, weights = available_peice_weights, k = 1)[0]
        
        starting_weights = create_weights(EMPTY_SQUARES, invert = invert)
        starting_square = random.choices(EMPTY_SQUARES, weights = starting_weights, k = 1)[0]
        row = math.floor(starting_square / TOT_COLS)
        col = starting_square % TOT_COLS

        initialized_piece = piece.piece_selector(chosen_piece[0], mult, starting_square, row, col)
#        deployment = {'name': chosen_piece[1]['name'], 'position': starting_square, 'id': chosen_piece[0], 'row': row, 'column': col}

        GAME.ARMIES[side].append(initialized_piece)
        EMPTY_SQUARES.remove(starting_square)
        GAME.POINTS[side] += chosen_piece[1]['value']


        if (GAME.get_board_piece(row, col) != 0):
            raise Exception("Square already occupied!") 
        GAME.set_board_piece(row, col, initialized_piece.get_index() * mult)


print('Board:')
GAME.get_board()



print(BORDER_COLOR + ' ' * TOT_COLS * 10 + END_COLOR)

print('\x1b[0;31;40m test \x1b[0m')
print('\x1b[1;31;47m test \x1b[0m')

def print_format_table():
    """
    prints table of formatted text format options
    """
    for style in range(8):
        for fg in range(30,38):
            s1 = ''
            for bg in range(40,48):
                format = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
            print(s1)
        print('\n')

print_format_table()
    

class move:
    def __init__(self, from_row, from_col, to_row, to_col, results):
        self.from_row = from_row
        self.from_col = from_col
        self.to_row = to_col
        self.to_col = to_col
        self.results = results
    
    def get_move(self):
        return ((self.from_row, self.from_col), (self.to_row, self.to_col))

    def get_result(self):
        return self.results


all_avail = []
for soldier in GAME.ARMIES['RED']:
    avail = soldier.get_available_moves(GAME.BOARD)
    for row in range(TOT_ROWS):
        for col in range(TOT_COLS):
            if (avail[row][col] == 1):
                
                # TODO only for CPU right now
                # TODO only for next move
                #move_result = {'RED': 
                if GAME.BOARD[row][col] > 0:
                    move_result = GAME.BOARD[row][col]
                potential_move = move(soldier.get_row(), soldier.get_column(), row, col, move_results)
                all_avail.append(potential_move)

random.choice(all_avail).get_move()

GAME.ARMIES['RED']

GAME.ARMIES['RED'][0]
print('Name: %s' % (GAME.ARMIES['RED'][0].get_name()))
print('Position: %s' % (GAME.ARMIES['RED'][0].get_position()))
print('Row: %s' % (GAME.ARMIES['RED'][0].get_row()))
print('Column: %s' % (GAME.ARMIES['RED'][0].get_column()))
print('Available Moves:')
print(GAME.ARMIES['RED'][0].get_available_moves(GAME.BOARD))
















































pawn=True
diagonal = True
vertical = True
horizontal = True
knight = True
available_moves = np.zeros((TOT_ROWS, TOT_COLS))

if (horizontal):
    for c in range(ARMIES['RED'][0]['column'] + 1, TOT_COLS):
        if (BOARD[ARMIES['RED'][0]['row']][c] < 0):
            break
        available_moves[ARMIES['RED'][0]['row']][c] = 1
        if (BOARD[ARMIES['RED'][0]['row']][c] > 0):
            break
    for c in reversed(range(ARMIES['RED'][0]['column'])):
        if (BOARD[ARMIES['RED'][0]['row']][c] < 0):
            break
        available_moves[ARMIES['RED'][0]['row']][c] = 1
        if (BOARD[ARMIES['RED'][0]['row']][c] > 0):
            break

if (vertical):
    for r in reversed(range(ARMIES['RED'][0]['row'])):
        if (BOARD[r][ARMIES['RED'][0]['column']] < 0):
            break
        available_moves[r][ARMIES['RED'][0]['column']] = 1
        if (BOARD[r][ARMIES['RED'][0]['column']] > 0):
            break
    for r in range(ARMIES['RED'][0]['row'] + 1, TOT_ROWS):
        if (BOARD[r][ARMIES['RED'][0]['column']] < 0):
            break
        available_moves[r][ARMIES['RED'][0]['column']] = 1
        if (BOARD[r][ARMIES['RED'][0]['column']] > 0):
            break

if (diagonal):
    start_row = ARMIES['RED'][0].get_row()
    start_col = ARMIES['RED'][0].get_column()
    
    row = start_row
    col = start_col
    while row < TOT_ROWS - 1 and col < TOT_COLS - 1:
        row += 1
        col += 1
        if (BOARD[row][col] < 0):
            break
        available_moves[row][col] = 1
        if (BOARD[row][col] > 0):
            break        

    row = start_row
    col = start_col
    while row > 0 and col < TOT_COLS - 1:
        row -= 1
        col += 1
        if (BOARD[row][col] < 0):
            break
        available_moves[row][col] = 1
        if (BOARD[row][col] > 0):
            break  

if (knight):
    piece_col = ARMIES['RED'][0].get_column()
    piece_row = ARMIES['RED'][0].get_row()
    
    # up
    if (piece_row - 2 > 0):
        if (piece_col - 1 > 0):
            if (BOARD[piece_row - 2][piece_col - 1] == 0 or BOARD[piece_row - 2][piece_col - 1] > 0):
                available_moves[piece_row - 2][piece_col - 1] = 1
        if (piece_col + 1 < TOT_COLS):
            if (BOARD[piece_row - 2][piece_col + 1] == 0 or BOARD[piece_row - 2][piece_col + 1] > 0):
                available_moves[piece_row - 2][piece_col + 1] = 1        
    # down
    if (piece_row + 2 < TOT_ROWS):
        if (piece_col - 1 > 0):
            if (BOARD[piece_row + 2][piece_col - 1] == 0 or BOARD[piece_row + 2][piece_col - 1] > 0):
                available_moves[piece_row + 2][piece_col - 1] = 1
        if (piece_col + 1 < TOT_COLS):
            if (BOARD[piece_row + 2][piece_col + 1] == 0 or BOARD[piece_row + 2][piece_col + 1] > 0):
                available_moves[piece_row + 2][piece_col + 1] = 1

    # right
    if (piece_col + 2 < TOT_COLS):
        if (piece_row - 1 > 0):
            if (BOARD[piece_row - 1][piece_col + 2] == 0 or BOARD[piece_row - 1][piece_col + 2] > 0):
                available_moves[piece_row - 1][piece_col + 2] = 1
        if (piece_row + 1 < TOT_ROWS):
            if (BOARD[piece_row + 1][piece_col + 2] == 0 or BOARD[piece_row + 1][piece_col + 2] > 0):
                available_moves[piece_row + 1][piece_col + 2] = 1

    # left
    if (piece_col - 2 > 0):
        if (piece_row - 1 > 0):
            if (BOARD[piece_row - 1][piece_col - 2] == 0 or BOARD[piece_row - 1][piece_col - 2] > 0):
                available_moves[piece_row - 1][piece_col - 2] = 1
        if (piece_row + 1 < TOT_ROWS):
            if (BOARD[piece_row + 1][piece_col - 2] == 0 or BOARD[piece_row + 1][piece_col - 2] > 0):
                available_moves[piece_row + 1][piece_col - 2] = 1



if (pawn):
    piece_col = ARMIES['RED'][0].get_column()
    piece_row = ARMIES['RED'][0].get_row()
    
    if (piece_row > 0):
        if (BOARD[piece_row - 1][piece_col] == 0):
            available_moves[piece_row - 1][piece_col] = 1
        if (piece_col > 0):
            if (BOARD[piece_row - 1][piece_col - 1] > 0):
                available_moves[piece_row - 1][piece_col - 1] = 1
        if (piece_col < TOT_COLS):
            if (BOARD[piece_row - 1][piece_col + 1] > 0):
                available_moves[piece_row - 1][piece_col + 1] = 1            
    







available_moves[ARMIES['RED'][0]['row']][ARMIES['RED'][0]['column']] = 0

print(BOARD)
print(available_moves)


#class game:
#    
#    def __init__(self, REF_BOARD)


REF_BOARD.flatten()









