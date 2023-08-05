#!/usr/bin/env python3

'''@TODO@'''

from . import Box, Label

class Button(Box):  # pylint: disable=R0904,R0902
    '''@TODO@'''

    def __init__(self, node, **kwargs):
        '''@TODO@'''
        node = Label.node_of(node)
        node.set_style('expand', True)
        node.set_style('halign', 'center')
        node.set_style('valign', 'center')
        Box.__init__(self, node, **kwargs)

    @property
    def node(self):
        '''node inside the button'''
        return self.children[0]
