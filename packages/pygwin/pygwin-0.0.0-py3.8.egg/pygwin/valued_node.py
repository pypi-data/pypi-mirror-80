#!/usr/bin/env python3

'''definition of class ValuedNode'''

from . import Node, Event


class ValuedNode(Node):
    '''a ValuedNode is any node that is associated a value (e.g.,
    checkboxes, lists, input texts)'''

    def __init__(self, **kwargs):
        '''create a ValuedNode initialised with kwarg value'''
        Node.__init__(self, **kwargs)
        self.__value = kwargs.get('value')

    @property
    def value(self):
        '''the value of the node'''
        return self.__value

    def set_value(self, value, trigger=True):
        '''change the value of the node.  if trigger is True, the ON_CHANGE
        event of the node is triggered'''
        self.__value = value
        if trigger and self.manager is not None:
            self.manager.trigger(Event.ON_CHANGE, None, self)
        self.update_manager()

    def trigger_on_change(self):
        '''trigger the ON_CHANGE event of the node'''
        if self.manager is not None:
            self.manager.trigger(Event.ON_CHANGE, None, self)
