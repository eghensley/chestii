#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 21:50:23 2022

@author: ehens86
"""
import piece
from constants import PIECES, TOT_ROWS, TOT_COLS
import numpy as np
import random
import math

#test = piece.Knight('white')
#test.get_name()

test = piece.piece_selector(2, False, 1, 1, 1)

BOARD = np.zeros((TOT_ROWS, TOT_COLS))
REF_BOARD = np.arange(TOT_ROWS * TOT_COLS).reshape((TOT_ROWS, TOT_COLS))

def create_weights(available_squares, invert = False):
    weights = []
    for square in EMPTY_SQUARES:
        row = math.floor(square / TOT_COLS)
        if (invert):
            row -= (TOT_ROWS - 1)
            row *= -1
        weights.append(row)
    return weights


    

EMPTY_SQUARES = [i for i in range(TOT_ROWS * TOT_COLS)]
# 39/(64/25)
MAX_POINTS = 15




POINTS = {
    'RED': 0,
    'BLACK': 0        
}

ARMIES = {
    'RED': [],
    'BLACK': []       
}

mult = 1
invert = False
# TODO: enforce peice maxes?
for side in ['RED', 'BLACK']:
    mult *= -1
    invert = not invert
    while POINTS[side] < MAX_POINTS:
        available_peices = [(k,v) for (k,v) in PIECES.items() if v['value'] <= MAX_POINTS - POINTS[side]]
        available_peice_weights = [i[1]['weight'] for i in available_peices]
        chosen_piece = random.choices(available_peices, weights = available_peice_weights, k = 1)[0]
        
        starting_weights = create_weights(EMPTY_SQUARES, invert = invert)
        starting_square = random.choices(EMPTY_SQUARES, weights = starting_weights, k = 1)[0]
        row = math.floor(starting_square / TOT_COLS)
        col = starting_square % TOT_COLS

        initialized_piece = piece.piece_selector(chosen_piece[0], mult, starting_square, row, col)
#        deployment = {'name': chosen_piece[1]['name'], 'position': starting_square, 'id': chosen_piece[0], 'row': row, 'column': col}

        ARMIES[side].append(initialized_piece)
        EMPTY_SQUARES.remove(starting_square)
        POINTS[side] += chosen_piece[1]['value']


        if (BOARD[row][col] != 0):
            raise Exception("Square already occupied!") 
        BOARD[row][col] = initialized_piece.get_index() * mult


print('Board:')
print(BOARD)


class move:
    def __init__(self, from_row, from_col, to_row, to_col):
        self.from_row = from_row
        self.from_col = from_col
        self.to_row = to_col
        self.to_col = to_col
    
    def get_move(self):
        return ((self.from_row, self.from_col), (self.to_row, self.to_col))


all_avail = []
for soldier in ARMIES['RED']:
    avail = soldier.get_available_moves(BOARD)
    for row in range(TOT_ROWS):
        for col in range(TOT_COLS):
            if (avail[row][col] == 1):
                potential_move = move(soldier.get_row(), soldier.get_column(), row, col)
                all_avail.append(potential_move)


ARMIES['RED']

ARMIES['RED'][0]
print('Name: %s' % (ARMIES['RED'][0].get_name()))
print('Position: %s' % (ARMIES['RED'][0].get_position()))
print('Row: %s' % (ARMIES['RED'][0].get_row()))
print('Column: %s' % (ARMIES['RED'][0].get_column()))
print('Available Moves:')
print(ARMIES['RED'][0].get_available_moves(BOARD))



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









