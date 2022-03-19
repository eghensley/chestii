#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 18:29:55 2022

@author: ehens86
"""

TOT_ROWS = 7
TOT_COLS = 5 # was 4, needs to be odd
# TODO update max points to reflect new column
# 39/(64/25)
MAX_POINTS = 15

END_COLOR = '\x1b[0m'
BORDER_COLOR = '\x1b[0;30;47m'
# TODO: use weights?
PIECES = {
    1: {'value': 1, 'max': 6, 'weight': 1, 'name': 'pawn'},
    2: {'value': 3, 'max': 2, 'weight': 1, 'name': 'knight'},
    3: {'value': 3, 'max': 2, 'weight': 1, 'name': 'bishop'},
    4: {'value': 5, 'max': 2, 'weight': 1, 'name': 'rook'},
    5: {'value': 9, 'max': 1, 'weight': 1, 'name': 'queen'}
}