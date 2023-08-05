#!/usr/bin/env python3

'''@TODO@'''

import pygame as pg

from . import StyleClass, Colors, InputText, Window, Node, Checkbox
from . import Gauge, Rule, Frame, Draw, Button


class DefaultStyle:  # pylint: disable=R0903
    '''@TODO@'''

    @classmethod
    def reset(cls):
        '''@TODO@'''
        for c in [Node, Window, Frame, InputText, Checkbox, Gauge, Rule]:
            StyleClass.rem(c)
            StyleClass.new(c)

    @classmethod
    def set_default(cls):
        '''@TODO@'''
        StyleClass.rem(Node)
        StyleClass.new(Node, {
            'selected': {
                'background': 'color',
                'color-background': Colors.BLUE_STEEL
            }
        })

        s = 20
        win_cross = pg.Surface((s, s)).convert_alpha()
        win_cross.fill((0, 0, 0, 0))
        half = int(s / 2) - 1
        for x in [0, half + 2]:
            for y in [0, half + 2]:
                Draw.rectangle(win_cross, Colors.RED_BLOOD, (x, y, half, half))
        Draw.rectangle(win_cross, Colors.BLUE_DARK, (0, 0, s, s), width=4)
        StyleClass.rem(Window)
        StyleClass.new(Window, {
            'base': {
                'padding': 10,
                'border': 'color',
                'border-width': 4,
                'color-border': Colors.BLUE_DARK,
                'background': 'color',
                'color-background': Colors.BLUE_DARK_STRONG,
                'image-window-cross': win_cross
            }
        })

        StyleClass.rem(Frame)
        StyleClass.new(Frame, {
            'base': {
                'padding': 10,
                'border': 'color',
                'border-width': 4,
                'color-border': Colors.BLUE_DARK
            }
        })

        StyleClass.rem(Button)
        StyleClass.new(Button, {
            'base': {
                'background': 'color',
                'border': 'color',
                'border-width': 4,
                'size': (200, 50),
                'color-background': Colors.BLUE_DARK,
                'color-border': Colors.BLUE_STEEL
            },
            'overed': {
                'color-background': Colors.BLUE_NAVY
            },
            'clicked': {
                'color-background': Colors.BLUE_DARK_STRONG
            },
            'focus': {
                'color-background': Colors.BLUE_POWDER
            }
        })

        StyleClass.rem(InputText)
        StyleClass.new(InputText, {
            'base': {
                'padding': 4,
                'border': 'color',
                'border-width': 4,
                'size': (200, None)
            },
            'focus': {
                'color': Colors.GREEN_YELLOW,
                'color-border': Colors.GREEN_YELLOW
            },
            'overed': {
                'color': Colors.BLUE_STEEL,
                'color-border': Colors.BLUE_STEEL
            }
        })

        StyleClass.rem(Checkbox)
        StyleClass.new(Checkbox, {
            'base': {
                'padding': 2,
                'border': 'color',
                'border-width': 4,
                'color': Colors.BLUE_DARK,
                'size': (24, 24)
            },
            'focus': {
                'color-border': Colors.GREEN_YELLOW,
                'color': Colors.GREEN_YELLOW
            },
            'overed': {
                'color': Colors.BLUE_STEEL,
                'color-border': Colors.BLUE_STEEL
            }
        })

        StyleClass.rem(Gauge)
        StyleClass.new(Gauge, {
            'base': {
                'border': 'color',
                'border-width': 3,
                'size': (200, 30),
                'background': 'color',
                'color': Colors.GREEN_DARK,
                'color-background': Colors.RED,
                'color-border': Colors.WHITE,
                'color-gauge-label': Colors.WHITE
            }
        })

        StyleClass.rem(Rule)
        StyleClass.new(Rule, {
            'base': {
                'width': 4,
                'color': Colors.BLUE_DARK,
                'orientation': 'horizontal'
            }
        })
