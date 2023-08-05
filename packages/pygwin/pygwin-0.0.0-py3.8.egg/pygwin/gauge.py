#!/usr/bin/env python3

'''@TODO@'''

import pygame as pg

from . import Draw, Node


class Gauge(Node):
    '''@TODO@'''

    def __init__(self, min_val, max_val, val, **kwargs):
        '''@TODO@'''
        Node.__init__(self, **kwargs)
        self.__min = min_val
        self.__max = max_val
        self.__val = val
        self.__label = None
        self.__draw_ratio = kwargs.get('draw_ratio', True)
        self.__label_format = kwargs.get('label_format', None)
        self.__set_label()

    @property
    def value(self):
        '''@TODO@'''
        return self.__val

    def set_value(self, val):
        '''@TODO@'''
        self.__val = val
        self.__set_label()
        self.update_manager()

    def set_label_format(self, label_format):
        '''@TODO@'''
        self.__label_format = label_format
        self.__set_label()

    def __set_label(self):
        if not self.__draw_ratio:
            return
        font = self.get_font()
        color = self.get_style('color-gauge-label')
        if self.__label_format is None:
            txt = str(self.__val) + ' / ' + str(self.__max)
        else:
            txt = self.__label_format(self.__min, self.__val, self.__max)
        self.__label = pg.Surface(font.size(txt)).convert_alpha()
        self.__label.fill((0, 0, 0, 0))
        txt = font.render(txt, 1, color)
        self.__label.blit(txt, (0, 0))

    def _compute_inner_size(self):
        return (200, 40)

    def __draw_bar(self, surface, pos):
        w, h = self.inner_size
        color = self.get_style('color')
        x, y = pos
        pts = int(self.__val * w / (self.__max - self.__min))
        rect = (x, y, pts, h)
        Draw.rectangle(surface, color, rect)

    def __draw_label(self, surface, pos):
        width, height = self.size
        x, y = pos
        if self.__label is not None:
            w, h = self.__label.get_size()
            x = x + int((width - w) / 2)
            y = y + int((height - h) / 2)
            surface.blit(self.__label, (x, y))

    def _draw(self, surface):
        self.__draw_bar(surface, self.inner_pos)
        self.__draw_label(surface, self.inner_pos)
