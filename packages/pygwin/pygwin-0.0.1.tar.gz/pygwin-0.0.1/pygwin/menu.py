#!/usr/bin/env python3

'''definition of class Menu'''

from . import Event, Rule, Util, Box, Empty


class Menu(Box):
    '''Menu nodes are collection of item nodes.  each item node is
    associated with one header node.  only one item is visible at any
    time.  activation of one of the headers shows its associated item
    and hides the others'''

    def __init__(self, items, **kwargs):
        '''create a Menu node.  items is a dictionary mapping header nodes to
        children nodes'''
        def on_mouse_wheel(pgevt):
            if pgevt.button is Util.MOUSEBUTTON_WHEEL_DOWN:
                self.__prev_tab()
            elif pgevt.button is Util.MOUSEBUTTON_WHEEL_UP:
                self.__next_tab()
            return True

        def switch_tab(i):
            def result(i):
                self.switch_tab(i)
                return True
            return lambda: result(i)

        Util.check_type(items, dict, 'items')

        Box.__init__(self, **kwargs)
        self.__items = dict()
        for i, item in enumerate(items):
            item.set_link(switch_tab(i))
            self.__items[item] = items[item]
        self.__curr = None
        if self.get_style('orientation') == 'vertical':
            orientation = 'horizontal'
        else:
            orientation = 'vertical'
        head_box = Box(style={'orientation': orientation,
                              'halign': 'center',
                              'valign': 'center'})
        for item in self.__items:
            head_box.pack(item)
        self.pack(head_box)
        self.pack(Rule(style={'orientation': orientation}))
        self.pack(Empty())

        head_box.add_processor(Event.ON_MOUSEWHEEL, on_mouse_wheel)
        self.switch_tab(0)

    @property
    def items(self):
        '''items of the menu'''
        return self.__items

    def get_selected(self):
        '''index of the item currently selected'''
        for i, item in enumerate(self.__items):
            if item == self.__curr:
                return i
        raise IndexError('item not found')

    def switch_tab(self, i):
        '''ith child becomes the current node'''
        if self.__curr is not None:
            self.__curr.set_selected(False)
            if self.manager is not None:
                self.manager.trigger(Event.ON_UNSELECT, None, self.__curr)
        self.__curr = self.__item_at_index(i)
        self.__curr.set_selected(True)
        node = self.__items[self.__curr]
        self.replace(2, node)
        if self.manager is not None:
            self.manager.trigger(Event.ON_SELECT, None, self.__curr)
        self.update_manager()

    def __item_at_index(self, idx):
        for i, item in enumerate(self.__items):
            if i == idx:
                return item
        raise IndexError('item not found')

    def __item_index(self, item):
        for i, it in enumerate(self.__items):
            if it == item:
                return i
        raise IndexError('item not found')

    def __next_tab(self):
        self.switch_tab(
            (self.__item_index(self.__curr) + 1) % len(self.__items))

    def __prev_tab(self):
        self.switch_tab(
            (self.__item_index(self.__curr) - 1) % len(self.__items))
