#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 02:47:36 2022

@author: ehens86
"""

from constants import TOT_COLS, TOT_ROWS
import random


class ai:
    def __init__(self, difficulty = 1):
        self.difficulty = difficulty

    def select_move(self, soldiers, board):
        all_available_moves = collect_ai_possible_moves(soldiers, board)
        
        if (self.difficulty == 0):
            return random.choice(all_available_moves)
        elif (self.difficulty == 1):            
            all_results = [potential_move.get_result()['GREEN'] - potential_move.get_result()['RED'] for potential_move in all_available_moves]
            best_result = min(all_results)
            
            best_move = all_available_moves[all_results.index(best_result)]
            return best_move

class move:
    def __init__(self, from_row, from_col, to_row, to_col, resulting_board):
        self.from_row = from_row
        self.from_col = from_col
        self.to_row = to_row
        self.to_col = to_col
        self.resulting_board = resulting_board
    
    def get_move(self):
        return ((self.from_row, self.from_col), (self.to_row, self.to_col))

    def get_result(self):
        return self.resulting_board.get_score()
    
    def get_new_board(self):
        return self.resulting_board


def collect_ai_possible_moves(soldiers, board):
    all_avail = []
    for soldier in soldiers:
        if (soldier.is_alive()):
            avail = soldier.get_available_moves(board.get_board())
            for new_row in range(TOT_ROWS):
                for new_col in range(TOT_COLS):
                    if (avail[new_row][new_col] == 1):
                        
                        # TODO only for CPU right now
                        # TODO only for next move
                        
                        move_board = board.clone()
                        
                        move_board.update_board_piece(new_row, new_col, soldier.get_index() * soldier.is_cpu())
                        move_board.update_board_piece(soldier.get_row(), soldier.get_column(), 0)
                        potential_move = move(soldier.get_row(), soldier.get_column(), new_row, new_col, move_board)
                        all_avail.append(potential_move)
    return all_avail