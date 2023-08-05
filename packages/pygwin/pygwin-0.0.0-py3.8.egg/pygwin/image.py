#!/usr/bin/env python3

'''definition of class Image'''

import pygame as pg

from . import Node, Util


class Image(Node):
    '''Image nodes are placeholders for pygame surfaces'''

    def __init__(self, surface, **kwargs):
        '''create an Image node holding the given surface'''
        Node.__init__(self, **kwargs)
        Util.check_type(surface, pg.Surface, 'surface')
        self.__surface = surface

    def __str__(self):
        return 'image'

    @property
    def surface(self):
        '''the pygame surface of the image'''
        return self.__surface

    def _compute_inner_size(self):
        return self.__surface.get_size()

    def _draw(self, surface):
        surface.blit(self.__surface, self.inner_pos)
