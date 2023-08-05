#!/usr/bin/env python3

'''@TODO@'''

import logging

from . import ContextStyle


class StyleClass:
    '''@TODO@'''

    CLASSES = {
    }

    @classmethod
    def new(cls, name, new=None):
        '''@TODO@'''
        if name in StyleClass.CLASSES:
            logging.warning('class already exists: %s', name)
        else:
            if new is None:
                StyleClass.CLASSES[name] = ContextStyle()
            else:
                StyleClass.CLASSES[name] = ContextStyle(new)
        return StyleClass.CLASSES[name]

    @classmethod
    def exists(cls, name):
        '''@TODO@'''
        return name in StyleClass.CLASSES

    @classmethod
    def get(cls, name):
        '''@TODO@'''
        if name not in StyleClass.CLASSES:
            logging.warning('class does not exist: %s', name)
            result = None
        else:
            result = StyleClass.CLASSES[name]
        return result

    @classmethod
    def rem(cls, name):
        '''@TODO@'''
        if name not in StyleClass.CLASSES:
            logging.warning('class does not exist: %s', name)
        else:
            del StyleClass.CLASSES[name]
