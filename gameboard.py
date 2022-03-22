#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 00:21:18 2022

@author: ehens86
"""

import piece
from constants import TOT_ROWS, TOT_COLS, END_COLOR, BORDER_COLOR
import numpy as np
from copy import deepcopy


def create_full_row(symbol):
    return BORDER_COLOR + symbol * int(TOT_COLS * 8.5 + 3) + END_COLOR 

class gameboard:

    def __init__(self):
        self._gameboard = np.zeros((TOT_ROWS, TOT_COLS))
        self._red_score = 0
        self._green_score = 0

    def get_board(self):
        return self._gameboard

    def update_board_piece(self, row, col, index):
        # Update score for replaced piece
        if (self._gameboard[row][col] != 0):
            if (self._gameboard[row][col] > 0):
                self._green_score -= piece.resolve_value(self._gameboard[row][col])
            else:
                self._red_score -= piece.resolve_value(self._gameboard[row][col])

        # Add piece
        self._gameboard[row][col] = index

        # Update score for added piece
        if (index != 0):
            if (index > 0):
                self._green_score += piece.resolve_value(index)
            else:
                self._red_score += piece.resolve_value(index)

    def get_board_piece(self, row, col):
        return self._gameboard[row][col]
    
    def clone(self):
        return deepcopy(self)

    def get_score(self):
        return {'RED': self._red_score, 'GREEN': self._green_score}

    def to_string(self):
        
        white_square = True
        
        top_bottom = create_full_row('_')
        row_divider = create_full_row('-')
        top_pad = create_full_row(' ')

       
        
        
        siding = BORDER_COLOR + ' ' * 9 + END_COLOR
        white_space =  '\x1b[1;37;47m' + ' ' * 9 + END_COLOR     
        score_board = '\x1b[1;%s;47m%s%s' + END_COLOR

        
        print(top_pad)
        print(siding + white_space * 3 + siding)
        print(siding + white_space + score_board % (31, 'RED:   ', str(self._red_score)) + white_space + siding)
        print(siding + white_space + score_board % (32, 'GREEN: ', str(self._green_score)) + white_space + siding)
        print(siding + white_space * 3 + siding)


        print(top_bottom)
        
        column_numbers = BORDER_COLOR + '| |'
        for col in range(TOT_COLS):
            column_numbers += '   %s   |' % (col)
        column_numbers += ' |' + END_COLOR
        
        print(column_numbers)

        print(row_divider)
        for row_number, (board_row) in enumerate(self._gameboard):
            
            row_pad_white = white_square
            
            row_pad = BORDER_COLOR + '| |' + END_COLOR
            for col in range(TOT_COLS):
                style = None
                fg = '31'
                bg = None
                if row_pad_white:
                    style = '1'
                    bg = '47'
                else:
                    style = '0'
                    bg = '40'
                row_pad += '\x1b[' + ';'.join([str(style), str(fg), str(bg)]) + 'm' + ' ' * 7 + END_COLOR + BORDER_COLOR + '|' + END_COLOR
                
                row_pad_white = not row_pad_white

            row_pad += BORDER_COLOR + ' |' + END_COLOR
            print(row_pad)
            
            
            row_str = BORDER_COLOR + '|%s|' % (row_number) + END_COLOR
            for row_square in board_row:
                
                style = None
                fg = '31'
                bg = None

                if white_square:
                    style = '1'
                    bg = '47'
                else:
                    style = '0'
                    bg = '40'
                    
                row_str += '\x1b[' + ';'.join([str(style), str(fg), str(bg)]) + 'm' + ' ' * 3 + END_COLOR
                
                # CPU piece, negative, red
                if row_square < 0:
                    row_str += '\x1b[' + ';'.join([str(style), str(fg), str(bg)]) + 'm' + piece.resolve_symbol(row_square) + END_COLOR
                
                # User piece, positive, green
                elif row_square > 0:
                    fg = 32
                    row_str += '\x1b[' + ';'.join([str(style), str(fg), str(bg)]) + 'm' + piece.resolve_symbol(row_square) + END_COLOR
                else:
                    row_str += '\x1b[' + ';'.join([str(style), str(fg), str(bg)]) + 'm' + ' ' * 1 + END_COLOR
                row_str += '\x1b[' + ';'.join([str(style), str(fg), str(bg)]) + 'm' + ' ' * 3 + END_COLOR
                row_str += BORDER_COLOR + '|' + END_COLOR
                
                white_square = not white_square
            row_str += '\x1b[0;30;47m' + '%s|' % (row_number) + END_COLOR
            print(row_str)
            
            print(row_pad)
            
            print(row_divider)
        print(column_numbers)
        print(top_bottom)