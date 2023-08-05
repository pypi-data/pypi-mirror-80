#!/usr/bin/env python3

'''definition of class Radiobox'''

from . import Checkbox


class Radiobox(Checkbox):
    '''@TODO@'''

    def __init__(self, group, group_value, **kwargs):
        '''kwarg value is True if the radiobox is initially checked.

        kwarg group is the CheckboxGroup this checkbox belongs to.

        kwarg group_value is the value (of any possible type) that
        will be associated to this radiobox in the group.  this means
        that if the radiobox is checked, then group.value will return
        group_value'''
        Checkbox.__init__(self, **kwargs)
        self.__group = group
        self.__group.add_radiobox(self, group_value)
        if self.value:
            self.__group.select(self)

    def activate(self):
        '''activate checkbox which is equivalent to having the user clicking
        on it'''
        if not self.value:
            if Checkbox.activate(self):
                self.__group.select(self)
                return True
        return False
