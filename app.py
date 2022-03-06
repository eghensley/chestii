#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 21:50:23 2022

@author: ehens86
"""

import numpy as np
import random
import math

TOT_ROWS = 7
TOT_COLS = 4
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


# TODO: use weights?
PEICES = {
    1: {'value': 1, 'max': 6, 'weight': 1, 'name': 'pawn'},
    2: {'value': 3, 'max': 2, 'weight': 1, 'name': 'knight'},
    3: {'value': 3, 'max': 2, 'weight': 1, 'name': 'bishop'},
    4: {'value': 5, 'max': 2, 'weight': 1, 'name': 'rook'},
    5: {'value': 9, 'max': 1, 'weight': 1, 'name': 'queen'}
}

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
        available_peices = [(k,v) for (k,v) in PEICES.items() if v['value'] <= MAX_POINTS - POINTS[side]]
        available_peice_weights = [i[1]['weight'] for i in available_peices]
        chosen_peice = random.choices(available_peices, weights = available_peice_weights, k = 1)[0]
        
        starting_weights = create_weights(EMPTY_SQUARES, invert = invert)
        starting_square = random.choices(EMPTY_SQUARES, weights = starting_weights, k = 1)[0]
        row = math.floor(starting_square / TOT_COLS)
        col = starting_square % TOT_COLS

        deployment = {'name': chosen_peice[1]['name'], 'position': starting_square, 'id': chosen_peice[0], 'row': row, 'column': col}
        

        
        ARMIES[side].append(deployment)
        EMPTY_SQUARES.remove(starting_square)
        POINTS[side] += chosen_peice[1]['value']


        if (BOARD[row][col] != 0):
            raise Exception("Square already occupied!") 
        BOARD[row][col] = deployment['id'] * mult


print(BOARD)



ARMIES['RED']

ARMIES['RED'][0]
ARMIES['RED'][0]['position'] 



pawn=False
diagonal = True
vertical = True
horizontal = True
knight = False
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
    start_row = ARMIES['RED'][0]['row']
    start_col = ARMIES['RED'][0]['column']
    
    row = start_row
    col = start_col
    while row < TOT_ROWS and col < TOT_COLS:
        row += 1
        col += 1
        if (BOARD[row][col] < 0):
            break
        available_moves[row][col] = 1
        if (BOARD[row][col] > 0):
            break        

    row = start_row
    col = start_col
    while row > 0 and col < TOT_COLS:
        row -= 1
        col += 1
        if (BOARD[row][col] < 0):
            break
        available_moves[row][col] = 1
        if (BOARD[row][col] > 0):
            break  

available_moves[ARMIES['RED'][0]['row']][ARMIES['RED'][0]['column']] = 0

print(available_moves)


#class game:
#    
#    def __init__(self, REF_BOARD)


REF_BOARD.flatten()









