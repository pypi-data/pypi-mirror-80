#!/usr/bin/env python3

'''definition of class Window'''

import logging

from . import Box, Coord, Label, Image, Event, Rule, EventManager, Media


class Window(Box, EventManager):  # pylint: disable=R0902
    '''defines Window objects'''

    DEFAULT_BUBBLE_POS = [
        ('relative', (('right', 10), ('bottom', 10))),
        ('relative', (('right', 10), ('top', 10))),
        ('relative', (('left', 10), ('bottom', 10))),
        ('relative', (('left', 10), ('top', 10))),
        ('absolute', (('right', 0), ('top', 0)))
    ]

    def __init__(self, win_sys, node, **kwargs):
        '''create a Window in the win_sys WindowSystem.

        node is the window content (a Node object)

        if not None, kwarg title is the window title (a string or a node)

        kwarg modal specifies if the window is modal (i.e. no other
        window can be accessed as long as this window is opened).
        only modal windows are supported for now'''
        Box.__init__(self, **kwargs)
        self.__win_sys = win_sys
        self.__modal = kwargs.get('modal', True)
        self.__sliding = False
        self.__sliding_init_pos = None
        self.__absolute_pos = None
        self.__popped = None
        title = kwargs.get('title')

        EventManager.__init__(self)
        Box.__init__(self, **kwargs)
        if title is not None:
            def start_sliding(pgevt):
                self.__sliding_init_pos = Coord.diff(
                    pgevt.pos, self.absolute_pos)
                self.__sliding = True
                return True
            def stop_sliding(_):
                self.__sliding = False
                return True
            def move(pgevt):
                if self.__sliding:
                    self.absolute_pos = Coord.diff(
                        pgevt.pos, self.__sliding_init_pos)
                    return True
                return False
            lbl = Label.node_of(title)
            lbl.set_style('valign', 'center')
            lbl.add_processor(Event.ON_CLICKDOWN, start_sliding)
            lbl.add_processor(Event.ON_CLICKUP, stop_sliding)
            self.add_processor(Event.ON_OVER, move)
            self.add_processor(Event.ON_OVERAGAIN, move)
            cross = self.__cross_image()
            if cross is None:
                title_box = lbl
            else:
                cross.set_style('valign', 'center')
                cross.can_grab_focus = lambda: False
                title_box = Box(
                    lbl, cross, style={'orientation': 'horizontal'})
            title_box.set_style('halign', 'center')
            self.pack(title_box)
            self.pack(Rule())
        self.pack(node)
        for child in self.iter_nodes():
            child.set_manager(self)
        self.container_size = self.__win_sys.screen.get_size()
        self.compute_size()

        self.add_processor(Event.ON_CLICKUP, self.__click_event)
        self.add_processor(Event.ON_CLICKUPRIGHT, self.__click_right_event)

    def __str__(self):
        return 'window'

    def __cross_image(self):
        def click_cross():
            self.close()
            return True
        cross = Media.get_image(self.get_style('image-window-cross'))
        if cross is None:
            result = None
        else:
            result = Image(cross, link=click_cross)
        return result

    @property
    def absolute_pos(self):
        '''position of the window in its window system'''
        return self.__absolute_pos

    @property
    def window_system(self):
        '''window system of this window'''
        return self.__win_sys

    @property
    def root_manager(self):
        '''@TODO@'''
        return self

    @property
    def window(self):
        '''@TODO@'''
        return self

    @property
    def modal(self):
        '''is the window modal'''
        return self.__modal

    @property
    def window_pos(self):
        return (0, 0)

    @property
    def content(self):
        return self

    @property
    def popped(self):
        '''popped node.  None if no popped node'''
        return self.__popped

    @absolute_pos.setter
    def absolute_pos(self, absolute_pos):
        '''change the position of the window in its window system'''
        self.__absolute_pos = absolute_pos

    def available_size(self):
        '''@TODO@'''
        return self.inner_size

    def is_root_manager(self):
        '''@TODO@'''
        return True

    def blit(self, surface):
        '''blit the window surface on the argument surface at position
        self.pos'''
        self.draw_content()
        surface.blit(self.surface, self.absolute_pos)

    def open(self, pos=None):
        '''open the window'''
        self.__win_sys.open_window(self, pos=pos)

    def close(self):
        '''close the window'''
        self.__win_sys.close_window(self)

    def move(self, move):
        '''move the window according to the move xy couple'''
        self.absolute_pos = Coord.sum(self.absolute_pos, move)

    def resize(self, size):
        '''resize the window content'''
        self.content.reset_size()
        self.set_style('size', size)
        self.updated = True

    def get_scroll(self):  # pylint: disable=R0201
        '''@TODO@'''
        return 0, 0

    def pop_node(self, popped, rect=None, node=None, candidate_pos=None):
        '''@TODO@'''

        #  find valid position for the popped node or exit
        popped_size = popped.compute_size()
        if candidate_pos is None:
            candidate_pos = Window.DEFAULT_BUBBLE_POS
        if rect is None and node is not None:
            rect = Coord.rect(node.window_pos, node.size)
        win_pos = None
        for pos in candidate_pos:
            try:
                p = None
                if pos[0] == Coord.RELATIVE:
                    if rect is not None:
                        p = Coord.relative_to_coord(pos[1], popped_size, rect)
                elif pos[0] == Coord.ABSOLUTE:
                    p = Coord.absolute_to_coord(pos[1], popped_size, self.size)
            except (TypeError, IndexError):
                pass
            if p is None:
                logging.warning('%s is not a valid position', pos)
                continue

            #  if the top-left and bottom-right corners are in the
            #  window system we return this position
            win_pos = p
            if Coord.ge(win_pos, (0, 0)) and \
               Coord.ge(self.size, Coord.sum(win_pos, popped_size)):
                break

        if win_pos is None:
            return

        #  position found => clear the previous popped node (if any).
        #  the new popped node is set as a floating node
        x, y = win_pos
        self.clear_popped()
        self.__popped = popped
        self.add_floating_node(popped, ((Coord.LEFT, x), (Coord.TOP, y)))

    def clear_popped(self):
        '''@TODO@'''
        if self.__popped is not None:
            self.del_floating_node(self.__popped)
            self.__popped = None
            return True
        return False

    def __click_event(self, _):
        return self.clear_popped()

    def __click_right_event(self, _):
        return self.clear_popped()
