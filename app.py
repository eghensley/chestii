#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 21:50:23 2022

@author: ehens86
"""
from constants import TOT_ROWS, TOT_COLS, END_COLOR, BORDER_COLOR, RED_WIN_SCORE, GREEN_WIN_SCORE
import numpy as np
import random
import game
import re
from ai import ai, collect_ai_possible_moves

#test = piece.Knight('white')
#test.get_name()

#test = piece.piece_selector(2, False, 1, 1, 1)


# TODO pawn and knight user input available moves
    

def resolve_input(provided_input):
    pattern = re.compile("^([0-9])\,([0-9]) > ([0-9])\,([0-9])$")
    
    # validate input
    if not pattern.match(provided_input):
        raise Exception('Invalid input provided')
    
    # Parse input
    match = pattern.match(provided_input)
    start_row = int(match.groups()[0])
    start_column = int(match.groups()[1])
    end_row = int(match.groups()[2])
    end_column = int(match.groups()[3])
    
    # Get index of piece in selected cell
    selected_cell = GAME.get_board()[start_row][start_column]
    
    # Validate cell is not empty
    if (selected_cell == 0):
        raise Exception('No piece occupies cell [%s,%s]' % (start_row, start_column))
    
    # Validate cell is not occupied by opposing team
    if (selected_cell < 0):
        raise Exception('Opposing piece occupies cell [%s,%s]' % (start_row, start_column))
    
    GAME.perform_move('GREEN', start_row, start_column, end_row, end_column)
    GAME.print_board()

def perform_cpu_move():
    ai_move = AI.select_move(GAME.ARMIES['RED'], GAME.board)
    (start_row, start_column), (end_row, end_column) = ai_move.get_move()
    cpu_moved_piece = GAME.get_piece_by_coordinates('RED', start_row, start_column)
    cpu_move_summary = 'CPU moved %s from cell [%s,%s] to cell [%s,%s]' % (cpu_moved_piece.get_name(), start_row, start_column, end_row, end_column)
    GAME.perform_move('RED', start_row, start_column, end_row, end_column)
    print()
    GAME.print_board()
    print(cpu_move_summary)


def perfom_user_move():
    
    waiting_for_player = True
    while waiting_for_player:
        try:
            user_move = input('GREEN PLAYER, provide your move in the form of START_ROW,START_COLUMN > END_ROW,END_COLUMN:   ')
            resolve_input(user_move)
            waiting_for_player = False
        except Exception as e:
            print()
            print(e)
            pass


print('Would you like to play a game?')
user_prompt = input('Answer: ')
if user_prompt.upper() not in ['Y', 'YES', 'YEAH', 'SURE', 'YEP', 'OKAY', 'OK']:
    print("I'm very disappointed...")
    exit




print()
print()
print('Awesome!  Let us play CHESS!')
print()
print()


AI = ai()
GAME = game.initialize_game()
GAME.print_board()









game_continue = True
while GAME.POINTS['RED'] > GREEN_WIN_SCORE and GAME.POINTS['GREEN'] > RED_WIN_SCORE:
    perfom_user_move()
    if GAME.POINTS['RED'] <= GREEN_WIN_SCORE or GAME.POINTS['GREEN'] <= RED_WIN_SCORE:
        break
    perform_cpu_move()

print()
print()
if GAME.POINTS['RED'] <= GREEN_WIN_SCORE:
    print("WINNER!  You're smart but I'll get you next time!")

if GAME.POINTS['GREEN'] <= RED_WIN_SCORE:
    print("HA!  You're not quite as smart as you thought!")
    

#selected_soldier= GAME.ARMIES['GREEN'][0]
#board, available_moves, piece_col, piece_row, team = GAME.get_board(), np.zeros((TOT_ROWS, TOT_COLS)), selected_soldier.get_column(), selected_soldier.get_row(), selected_soldier.is_cpu()
#
#for r in reversed(range(piece_row)):
#    # Stop when encountering a piece from the same team
#    if ((team < 0) == (board[r][piece_col] <= 0)):
#        break
#    available_moves[r][piece_col] = 1
#    # If the cell is occupied it, then stop
#    if (board[r][piece_col] != 0):
#        break
#for r in range(piece_row + 1, TOT_ROWS):
#    # Stop when encountering a piece from the same team
#    if ((team < 0) == (board[r][piece_col] <= 0)):
#        break
#    available_moves[r][piece_col] = 1
#    # If the cell is occupied it, then stop
#    if (board[r][piece_col] != 0):
#        break
#
#
#
#
#for s in GAME.ARMIES['RED']:
#    print('~~~~~~~~~~~~~~~')
#    print(s.get_name())
#    print(s.get_row())
#    print(s.get_column())
#    print(s.get_available_moves(GAME.board.get_board()))
#
#
#GAME.ARMIES['RED'][0].get_available_moves(GAME.board.get_board())