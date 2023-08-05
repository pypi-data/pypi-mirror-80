#!/usr/bin/env python3

'''@TODO@'''

from . import Window


class Panel(Window):
    '''@TODO@'''

    def open(self, pos=None):
        '''open the panel'''
        self.window_system.open_panel(self, pos=pos)
