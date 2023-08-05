#!/usr/bin/env python3

'''definition of class TextBoard'''

from . import Box, Util, Image


class TextBoard(Box):
    '''@TODO@'''

    PUSH_AT_BOTTOM = 'push-at-bottom'
    PUSH_AT_TOP = 'push-at-top'

    def __init__(self, **kwargs):
        '''@TODO@'''
        Box.__init__(self, **kwargs)
        self.__text = list()
        self.__pending = list()
        self.__text_width = None
        self.__rows = kwargs.get('rows', 100)
        self.__push_where = kwargs.get('push_where', TextBoard.PUSH_AT_BOTTOM)

    def push_text(self, text):
        '''@TODO@'''
        self.__text.append(text)
        self.__pending.append(text)

    def _compute_inner_size(self):
        if self.width is None:
            return 0, 0
        if self.__text_width != self.width:
            self.__text_width = self.width
            self.empty()
            text_list = self.__text
        elif self.__pending != []:
            text_list = self.__pending
        else:
            text_list = []
        self.__pending = []

        for text in text_list:
            lines = list(Util.split_lines(
                text, self.get_font(), self.get_style('color'),
                width=self.__text_width))
            if self.__push_where == TextBoard.PUSH_AT_TOP:
                lines.reverse()
            for line in lines:
                lbl = Image(line)
                if self.__push_where == TextBoard.PUSH_AT_TOP:
                    self.insert(lbl, 0)
                else:
                    self.pack(lbl)

        while len(self.children) > self.__rows:
            if self.__push_where == TextBoard.PUSH_AT_TOP:
                self.remove(self.__rows)
            else:
                self.remove(0)

        return Box._compute_inner_size(self)
