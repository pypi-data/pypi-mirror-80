#!/usr/bin/env python3

'''definition of class ItemSelect'''

from . import Select, Style, Util, Label


class ItemSelect(Select):
    '''ItemSelect nodes are Select nodes with values belonging in a set of
    dictionary keys'''

    def __init__(self, items, **kwargs):
        '''create an ItemSelect node containing items.  items must be a
        dictionary mapping ItemSelect values (which can be of any type) to
        strings.  if not None, kwarg value (the initial value of the
        select) must be in items.

        for instance:
        >>> s = ItemSelect({(0, 10): "child",
                            (10, 20): "teenager",
                            (21, 120): "grown up"})
        creates an ItemSelect nodes with 3 values.  initially,
        s.value == (0, 10)'''

        #  check arguments
        Util.check_type(items, dict, name='items')

        style = Style(kwargs.get('style', {}))
        self.__items = []
        label_width = 0
        for item in items:
            self.__items.append(item)
            lbl = Label(items[item], style=style)
            w, _ = lbl.compute_size()
            label_width = max(label_width, w)
        if 'width' not in style:
            style['width'] = label_width
        kwargs['style'] = style

        def get_node(item):
            return items[item]

        def get_prev(item):
            return self.__items[self.__items.index(item) - 1]

        def get_next(item):
            return self.__items[self.__items.index(item) + 1]

        Select.__init__(
            self, self.__items[0], self.__items[-1],
            get_prev, get_next, get_node=get_node, **kwargs)

    @property
    def items(self):
        '''items of the select'''
        return self.__items
