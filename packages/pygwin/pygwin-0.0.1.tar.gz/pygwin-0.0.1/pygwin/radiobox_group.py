#!/usr/bin/env python3

'''definition of class RadioboxGroup'''


class RadioboxGroup:
    '''a RadioboxGroup is used to group Radiobox nodes that are mutually
    exclusive (like radio buttons): if a Radiobox is selected among
    the group, then others become deselected.  RadioboxGroups are not
    visible on the screen, they are just logical groups of Radiobox
    nodes'''

    def __init__(self):
        '''initialise the group with an empty set of radiobox'''
        self.__selected = None
        self.__values = dict()

    @property
    def value(self):
        '''get the value associated to the box of the group that is currently
        checked, None if none is checked'''
        if self.__selected is None:
            result = None
        else:
            result = self.__values[self.__selected]
        return result

    def add_radiobox(self, box, value):
        '''add Radiobox box to the group and associate the given value'''
        self.__values[box] = value

    def select(self, box):
        '''Radiobox box becomes the selected Radiobox of the group.
        ValueError is raised if the box does not belong to the group'''
        if box not in self.__values:
            raise ValueError('box does not belong to the group values')
        if box != self.__selected:
            if self.__selected is not None:
                self.__selected.set_value(False)
            self.__selected = box
            self.__selected.set_value(True)
