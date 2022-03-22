#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 00:25:29 2022

@author: ehens86
"""

import math
from constants import PIECES, TOT_ROWS, TOT_COLS, MAX_POINTS, EMPTY_SQUARES, TEAM_TOGGLE
import random
from gameboard import gameboard
import piece
import numpy as np

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
            'GREEN': 0        
        }
        self.ARMIES = {
            'RED': [],
            'GREEN': []       
        }
        self.board = gameboard()
        self.REF_BOARD = np.arange(TOT_ROWS * TOT_COLS).reshape((TOT_ROWS, TOT_COLS))

    def get_board(self):
        return self.board.get_board()

    def print_board(self):
        return self.board.to_string()

    def set_board_piece(self, row, column, value):
        self.board.update_board_piece(row, column, value)
        
    def get_board_piece(self, row, column):
        return self.board.get_board_piece(row, column)

    def get_piece_by_coordinates(self, team, row, column):
        for soldier in self.ARMIES[team]:
            if (soldier.is_alive() and soldier.get_row() == row and soldier.get_column() == column):
                return soldier
        raise Exception('No piece found for %s army at coordinates [%s,%s]' % (team, row, column))
        
    def perform_move(self, team, start_row, start_column, end_row, end_column):
        
        # Get the soldier which occupies cell
        selected_soldier = self.get_piece_by_coordinates(team, start_row, start_column)
        
        selected_soldier.get_available_moves(self.get_board())      
        selected_soldier.is_valid_move(self.get_board(), end_row, end_column)

        if self.get_board()[end_row][end_column] != 0:            
            replacing_soldier = self.get_piece_by_coordinates(TEAM_TOGGLE[team], end_row, end_column)
            replacing_soldier.kill()

        # Replace existing piece in cell with new piece
        self.board.update_board_piece(end_row, end_column, selected_soldier.get_atomic_index())
        
        # Replace previous cell with empty
        self.board.update_board_piece(selected_soldier.get_row(), selected_soldier.get_column(), 0)
        
        # Update the piece itself
        selected_soldier.set_cell(end_row, end_column)
        
        self.POINTS = self.board.get_score()
        
        
def initialize_game():
    GAME = game()
    
    mult = 1
    invert = False
    # TODO: enforce peice maxes?
    for side in ['RED', 'GREEN']:
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
    return GAME