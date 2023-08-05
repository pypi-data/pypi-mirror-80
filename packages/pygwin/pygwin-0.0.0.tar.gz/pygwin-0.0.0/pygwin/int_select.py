#!/usr/bin/env python3

'''definition of class IntSelect'''

from . import Select, Util


class IntSelect(Select):
    '''IntSelect nodes are Select nodes containing integer values in a
    specific range'''

    def __init__(self, min_val, max_val, **kwargs):
        '''creates an IntSelect node with values ranging from min_val to
        max_val'''

        #  check arguments
        Util.check_type(min_val, int, 'min_val', none_accepted=True)
        Util.check_type(max_val, int, 'max_val', none_accepted=True)

        def get_prev(n):
            return n - 1

        def get_next(n):
            return n + 1

        Select.__init__(self, min_val, max_val, get_prev, get_next, **kwargs)
