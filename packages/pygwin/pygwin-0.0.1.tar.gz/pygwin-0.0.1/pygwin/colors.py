#!/usr/bin/env python3

'''definition of class Colors'''


class Colors:  # pylint: disable=R0903
    '''an enumeration of different colors'''

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    GRAY = (128, 128, 128)
    YELLOW = (255, 255, 0)

    GREEN_DARK = (0, 100, 0)
    GREEN_YELLOW = (173, 255, 47)
    GRAY_LIGHT = (168, 168, 168)
    GRAY_LIGHT_VERY = (212, 212, 212)
    GRAY_DARK = (84, 84, 84)
    BLUE_DARK = (0, 30, 60)
    BLUE_DARK_STRONG = (0, 2, 30)
    BLUE_STEEL = (70, 130, 180)
    BLUE_NAVY = (0, 0, 128)
    BLUE_LIGHT = (173, 216, 230)
    BLUE_SKY = (135, 206, 235)
    BLUE_POWDER = (176, 224, 230)
    PURPLE_MEDIUM = (147, 112, 219)
    INDIGO = (75, 0, 130)
    CRIMSON = (220, 20, 60)
    LAVENDER = (230, 230, 250)
    RED_BLOOD = (170, 0, 0)

    @classmethod
    def acolor(cls, color, alpha):
        '''get an RGB color and alpha value and return an rgba color'''
        r, g, b = color
        return r, g, b, alpha
