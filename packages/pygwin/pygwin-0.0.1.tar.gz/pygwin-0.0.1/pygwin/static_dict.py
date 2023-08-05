#!/usr/bin/env python3

'''definition of class StaticDict'''

from . import Util


class StaticDict(dict):
    '''StaticDict objects are dictionnaries whose keys can only belong to
    a DEFAULT dictionary.  if a key of a StaticDict d is accessed and
    if key is not in d, then d[key] == DEFAULT[key].  for instance:

    >>> d = StaticDict()
    >>> StaticDict.DEFAULT = {'x': 0, 'y': 0, 'z': 0}
    >>> d['z'] = 26
    >>> d['a'] = 1
    KeyError
    >>> print(d['x'])
    0

    any subclass of StaticDict may redefine the DEFAULT class attribute'''

    DEFAULT = {}

    def __init__(self, d=None):
        '''create a StaticDict initialised with dictionary d'''
        Util.check_type(d, dict, name='d', none_accepted=True)
        dict.__init__(self)
        if d is not None:
            for key in d:
                self[key] = d[key]

    @classmethod
    def get_default(cls, key):
        '''get default value associated with key.  KeyError is raised if key
        is not in the class DEFAULT dictionary'''
        default = cls.DEFAULT
        if key not in default:
            cls.__raise_key_error(key)
        return default[key]

    @classmethod
    def set_default(cls, key, value):
        '''change the value associated to the key of the class DEFAULT
        dictionary.  KeyError is raised if key is not in the class
        DEFAULT dictionary'''
        default = cls.DEFAULT
        if key not in default:
            cls.__raise_key_error(key)
        default[key] = value

    def __setitem__(self, key, value):
        if key not in type(self).DEFAULT:
            type(self).__raise_key_error(key)
        dict.__setitem__(self, key, value)

    def __getitem__(self, key):
        if not type(self).DEFAULT:
            type(self).__raise_key_error(key)
        if key not in self:
            result = type(self).DEFAULT[key]
        else:
            result = dict.__getitem__(self, key)
        return result

    @classmethod
    def __raise_key_error(cls, key):
        raise KeyError('{} is not a valid key for a {} dictionary'.format(
            key, cls))
