#!/usr/bin/env python3

'''definition of class ContextStyle'''

from . import Style


class ContextStyle(dict):
    '''@TODO@'''

    def get_attr(self, ctx, attr):
        '''@TODO@'''
        if ctx in self and attr in self[ctx]:
            result = self[ctx][attr]
        else:
            result = None
        return result

    def set_attr(self, ctx, attr, value, update=True):
        '''@TODO@'''
        if ctx not in self:
            self[ctx] = Style()
        if update or attr not in self[ctx]:
            self[ctx][attr] = value
            result = True
        else:
            result = False
        return result

    def update(self, ctx, style):
        '''@TODO@'''
        if ctx not in self:
            self[ctx] = Style()
        self[ctx] = {**self[ctx], **style}
