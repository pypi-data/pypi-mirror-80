#!/usr/bin/env python3

'''definition of class Select'''

from . import Box, Event, Label, Util, ValuedNode, Context


class Select(Box, ValuedNode):  # pylint: disable=R0902
    '''Select nodes are comparable to select HTML elements.  they contain a
    fixed list of items the user can navigate through.  a select consist
    of a label and two links (or possibly more) allowing to navigate
    backward or forward in the list.  unlike select elements, it is
    only possible to navigate sequentially through the list.

    note that the IntSelect and ItemSelect classes inheriting from Select
    should be prefered for most cases.'''

    NEXT = 1
    PREV = -1

    def __init__(self, first, last, get_prev, get_next, **kwargs):
        '''create a Select node ranging from first to last.  first and last
        can be of any type.  get_prev and get_next are mapping from a
        select value to its predecessor or successor.

        kwarg value is the initial value of the select (default=first)

        kwarg wheel_units corresponds to the number of steps done on
        the select when the a single mousewheel is used on it.  a
        value of 0 disable mouse wheeling on the select (default=1).

        kwarg cyclic states if the select is cyclic (default=False)

        kwarg get_node is a function from select values to anything
        that can str-ed

        kwarg prev_node (resp. next_node) is the node that will be
        used as the previous (next) link

        for instance:
        >>> Select(0, 100, lambda n: n - 1, lambda n: n + 1, value=50)
        creates a list with values ranging from 0 to 100 and
        initialised to 50.  (note that for int Select, IntSelect
        should be used instead)'''
        def handler(step):
            return lambda: self.__move(step)

        def create_navigation_links():
            has_imgs = self.style.get_attr('base', 'image-select') is None
            for idx, name, lbl in [(0, 'prev', '&lt;'), (1, 'next', '&gt;')]:
                node = kwargs.get(name + '_node')
                if node is None:
                    if has_imgs:
                        node = Label(lbl)
                    else:
                        node = Box()
                        for ctx in Context:
                            img = self.style.get_attr(ctx, 'image-select')
                            if img is not None:
                                node.set_style(
                                    'background', 'image', ctx=ctx)
                                node.set_style(
                                    'image-background', img[idx], ctx=ctx)
                yield node
        value = kwargs.get('value', first)
        kwargs['value'] = value
        Box.__init__(self, **kwargs)
        ValuedNode.__init__(self, **kwargs)
        self.set_style('orientation', 'horizontal')
        self.__first = first
        self.__last = last
        self.__get_prev = get_prev
        self.__get_next = get_next
        self.__prev_node, self.__next_node = create_navigation_links()
        self.__get_node = kwargs.get('get_node', str)
        self.__cyclic = kwargs.get('cyclic', False)
        self.__wheel_units = kwargs.get('wheel_units', 1)
        self.__lbl = Label(str(self.__get_node(value)))
        if self.__wheel_units > 0:
            self.add_processor(Event.ON_MOUSEWHEEL, self.__mouse_wheel_event)
        lbl_box = Box(style={'size': (self.get_style('width'), None),
                             'valign': 'center'})
        lbl_box.pack(self.__lbl)

        self.__prev_node.set_link(handler(Select.PREV))
        self.__next_node.set_link(handler(Select.NEXT))
        self.__links = {
            Select.PREV: self.__prev_node,
            Select.NEXT: self.__next_node
        }
        self.pack(self.__links[Select.PREV])
        self.pack(lbl_box)
        self.pack(self.__links[Select.NEXT])
        self.set_value(value, trigger=False)

    def __str__(self):
        return 'select({})'.format(','.join(list(map(str, self.children))))

    def set_value(self, value, trigger=True):
        '''set value of the select to value.  if trigger is True, the ON_CHANGE
        event of the select is triggered'''
        self.__lbl.set_text(str(self.__get_node(value)))
        if not self.__cyclic:
            fun = self.disable_move if value == self.__first \
                else self.enable_move
            fun(Select.PREV)
            fun = self.disable_move if value == self.__last \
                else self.enable_move
            fun(Select.NEXT)
        ValuedNode.set_value(self, value, trigger=trigger)

    def disable_move(self, move):
        '''disable navigation link of move (Select.NEXT or Select.PREV)'''
        if move not in [Select.NEXT, Select.PREV]:
            raise ValueError('move must be in {}'.format(
                [Select.NEXT, Select.PREV]))
        self.__links[move].disable()

    def enable_move(self, move):
        '''enable navigation link of move (Select.NEXT or Select.PREV)'''
        if move not in [Select.NEXT, Select.PREV]:
            raise ValueError('move must be in {}'.format(
                [Select.NEXT, Select.PREV]))
        self.__links[move].enable()

    def reset(self, first, last, value):
        '''set the first, last and current value of the select'''
        self.__first = first
        self.__last = last
        self.set_value(value)

    def __move(self, move):
        if self.__links[move].is_disabled():
            return False
        if move == Select.PREV:
            if self.value == self.__first:
                new = self.__last if self.__cyclic else None
            else:
                new = self.__get_prev(self.value)
        else:
            if self.value == self.__last:
                new = self.__first if self.__cyclic else None
            else:
                new = self.__get_next(self.value)
        if new is not None:
            self.set_value(new)
        return new is not None

    def __mouse_wheel_event(self, evt):
        move = None
        if evt.button == Util.MOUSEBUTTON_WHEEL_DOWN:
            move = Select.NEXT
        elif evt.button == Util.MOUSEBUTTON_WHEEL_UP:
            move = Select.PREV
        if move is not None:
            for _ in range(self.__wheel_units):
                self.__move(move)
        return True
