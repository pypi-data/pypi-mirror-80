#!/usr/bin/env python3

'''@TODO@'''

import logging
import pygame as pg

from . import Colors, StaticDict


class Style(StaticDict):
    '''@TODO@'''

    DEFAULT = {
        'background': None,
        'bold': False,
        'border': 'color',
        'border-width': 0,
        'color': Colors.WHITE,
        'color-background': Colors.BLACK,
        'color-border': Colors.BLUE_DARK,
        'color-frame-bar': Colors.acolor(Colors.BLUE_STEEL, 150),
        'color-frame-bar-container': Colors.acolor(Colors.BLUE_DARK, 150),
        'color-gauge-label': Colors.WHITE,
        'cursor': None,
        'expand': False,
        'font': pg.font.get_default_font(),
        'font-size': 16,
        'frame-bar-wheel-pt-units': 20,
        'frame-bar-width': 8,
        'halign': 'left',
        'hspacing': 10,
        'image-background': None,
        'image-border': None,
        'image-checkbox': None,
        'image-frame-vscroll-bar': None,
        'image-frame-vscroll-container': None,
        'image-hrule': None,
        'image-select': None,
        'image-vrule': None,
        'image-window-cross': None,
        'italic': False,
        'orientation': 'vertical',
        'padding': 0,
        'size': None,
        'sound': None,
        'underline': False,
        'valign': 'top',
        'vspacing': 10,
        'width': None
    }

    INHERITED = {
        'color',
        'font',
        'font-size',
        'hspacing',
        'vspacing'
    }

    def __init__(self, d=None):
        '''@TODO@'''
        StaticDict.__init__(self, d)

    def __setitem__(self, key, value):
        try:
            StaticDict.__setitem__(self, key, value)
        except KeyError:
            logging.warning('undefined style: %s', key)

    def __getitem__(self, key):
        try:
            return StaticDict.__getitem__(self, key)
        except KeyError:
            logging.warning('undefined style: %s', key)
            return None
