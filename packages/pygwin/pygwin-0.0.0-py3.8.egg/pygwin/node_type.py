#!/usr/bin/env python3

'''@TODO@'''

from . import StyleClass


class NodeType(type):
    '''@TODO@'''

    def __init__(cls, name, bases, dic):
        '''@TODO@'''
        type.__init__(cls, name, bases, dic)

        #  create a new style class for this node class
        StyleClass.new(cls)
