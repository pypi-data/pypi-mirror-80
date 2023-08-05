#!/usr/bin/env python3

'''@TODO@'''

class EnumType(type):
    '''@TODO@'''

    def __iter__(cls):
        for key in cls.__dict__:
            val = cls.__dict__[key]
            if not key.startswith('__') and isinstance(val, str):
                yield val
