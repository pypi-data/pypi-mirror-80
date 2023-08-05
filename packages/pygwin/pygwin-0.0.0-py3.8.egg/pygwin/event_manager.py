#!/usr/bin/env python3

'''@TODO@'''

import pygame as pg

from . import Event, Util, Keys, Coord


class EventManager:  # pylint: disable=R0904,R0902
    '''@TODO@'''

    class NodeFound(Exception):
        '''@TODO@'''

        def __init__(self, node):
            '''@TODO@'''
            Exception.__init__(self)
            self.node = node

    def __init__(self):
        '''@TODO@'''
        self.__updated = True
        self.__surface = None
        self.__focus = None
        self.__overed = set()
        self.__clicked = set()
        self.__registered = {evt: list() for evt in Event}
        self.__floating = dict()

    @property
    def window_system(self):
        '''@TODO@'''

    @property
    def content(self):
        '''@TODO@'''

    @property
    def surface(self):
        '''@TODO@'''
        return self.__surface

    @property
    def updated(self):
        '''@TODO@'''
        return self.__updated

    @property
    def focus(self):
        '''@TODO@'''
        return self.__focus

    @surface.setter
    def surface(self, surface):
        '''@TODO@'''
        self.__surface = surface

    @updated.setter
    def updated(self, updated):
        '''@TODO@'''
        self.__updated = updated

    def draw_content(self):
        '''@TODO@'''
        if self.updated:
            self.content.compute_size()
            size = self.content.size
            if self.surface is None or self.surface.get_size() != size:
                self.surface = pg.Surface(size).convert_alpha()
            self.surface.fill((0, 0, 0, 0))
            self.content.position((0, 0))
            self.content.draw(self.surface)
            self.updated = False

            #  position floating nodes
            psize = self.content.size
            for node in self.__floating:
                nsize = node.compute_size()
                node.position(Coord.absolute_to_coord(
                    self.__floating[node], nsize, psize))

            #  draw all children nodes
            for node in self.iter_nodes():
                node.set_manager(self)
                if not node.is_hidden():
                    node.draw(self.surface)

    def is_root_manager(self):  # pylint: disable=R0201
        '''@TODO@'''
        return False

    def add_floating_node(self, node, pos):
        '''@TODO@'''
        node.set_manager(self)
        self.__floating[node] = pos
        for child in node.iter_tree():
            child.depth = 0
        self.updated = True

    def set_floating_node_pos(self, node, pos):
        '''@TODO@'''
        if node not in self.__floating:
            self.add_floating_node(node, pos)
        self.__floating[node] = pos
        self.updated = True

    def del_floating_node(self, node):
        '''@TODO@'''
        if node in self.__floating:
            node.unref()
            del self.__floating[node]
        self.updated = True

    def remove_focus(self):
        '''@TODO@'''
        focus = self.__focus
        self.__focus = None
        if focus is not None:
            focus.lose_focus()

    def give_focus(self, node):
        '''@TODO@'''
        if node == self.__focus or not node.can_grab_focus():
            return
        self.remove_focus()
        self.__focus = node
        if node is not None:
            node.get_focus()

    def activate_focus(self):
        '''@TODO@'''
        if self.__focus is None:
            return False
        result = self.__focus.activate()
        self.updated = result
        return result

    def move_focus(self, forward):
        '''@TODO@'''
        old_focus = self.__focus
        retry = self.__focus is not None
        try:
            _, previous = self.move_focus_loop(forward, self.__focus, None)
            if retry:
                if forward:
                    self.move_focus_loop(True, None, None)
                else:
                    raise EventManager.NodeFound(previous)
        except EventManager.NodeFound as e:
            self.give_focus(e.node)
        return old_focus != self.__focus

    def move_focus_loop(self, forward, searched, previous):
        '''@TODO@'''
        def loop(node, args):
            searched, previous = args
            if node.can_grab_focus() and not node.is_hidden():
                if forward:
                    if searched is None:
                        raise EventManager.NodeFound(node)
                    if node == searched:
                        searched, previous = None, None
                else:
                    if node != searched:
                        previous = node
                    elif previous is None:
                        searched, previous = node, None
                    else:
                        raise EventManager.NodeFound(previous)
            return node.focus_lookup(forward, searched, previous)
        for node in self.iter_nodes():
            if node != self:
                searched, previous = loop(node, (searched, previous))
        return searched, previous

    def register(self, evt, proc, fun):
        '''@TODO@'''
        self.__registered[evt].append((proc, fun))

    def unregister(self, evt, proc, fun):
        '''@TODO@'''
        self.__registered[evt] = [pf for pf in self.__registered[evt]
                                  if pf != (proc, fun)]

    def unref_proc(self, proc):
        '''@TODO@'''
        for evt in self.__registered:
            self.__registered[evt] = [pf for pf in self.__registered[evt]
                                      if pf[0] != proc]

    def trigger(self, evt, pgevt, proc):
        '''@TODO@'''
        return self.__event(evt, pgevt, check_pos=False, incl={proc})

    def __check_pos_over(self, pos, node):
        if not node.is_over(pos):
            return False
        if any(f.depth < node.depth and f.is_over(pos)
               for f in self.__floating):
            return False
        return True

    def __event(self, evt, pgevt, **kwargs):
        result = False
        check_pos = kwargs.get('check_pos', True)
        incl = kwargs.get('incl', None)
        for proc, fun in self.__registered[evt]:

            #  it may be the case that the manager of proc is not self
            #  anymore if a processor in self.__registered[evt]
            #  removed it (call to fun in this loop).  if so we skip
            #  it
            if proc.manager != self:
                continue

            #  the event has a position and this one is not inside the
            #  node => skip it
            if check_pos and hasattr(pgevt, 'pos') and \
               not self.__check_pos_over(pgevt.pos, proc):
                continue

            #  the node is not in included => skip it
            if incl is not None and proc not in incl:
                continue

            #  the node is hidden => skip it
            if proc.is_hidden():
                continue

            if fun(pgevt):
                result = True
        return result

    def __pg_mouse_motion(self, pgevt):
        result = False

        #  check which nodes are not overed anymore and which are
        #  newly overed.  set the overed flag of these
        not_overed_anymore = {
            n for n in self.__overed
            if not self.__check_pos_over(pgevt.pos, n)
        }
        newly_overed = set(
            (n for n in self.iter_nodes()
             if self.__check_pos_over(pgevt.pos, n)
             and n not in self.__overed))
        self.__overed = self.__overed - not_overed_anymore
        for n in not_overed_anymore:
            n.set_overed(False)
        for n in newly_overed:
            n.set_overed(True)

        #  trigger events
        result = False
        for evt, node_set in [(Event.ON_UNOVER, not_overed_anymore),
                              (Event.ON_OVERAGAIN, self.__overed),
                              (Event.ON_OVER, newly_overed)]:
            result = self.__event(
                evt, pgevt, check_pos=False, incl=node_set) or result

        self.__overed |= set(newly_overed)

        return result

    def __pg_mouse_button_up(self, pgevt):
        if pgevt.button == Util.MOUSEBUTTON_LEFT:
            result = self.__event(Event.ON_CLICKUP, pgevt)
            for n in self.__clicked:
                n.set_clicked(False)
            self.__clicked = set()
            return result
        if pgevt.button == Util.MOUSEBUTTON_RIGHT:
            return self.__event(Event.ON_CLICKUPRIGHT, pgevt)
        if pgevt.button in [Util.MOUSEBUTTON_WHEEL_DOWN,
                            Util.MOUSEBUTTON_WHEEL_UP]:
            return self.__event(Event.ON_MOUSEWHEEL, pgevt)
        return False

    def __pg_mouse_button_down(self, pgevt):
        evt = None
        if pgevt.button == Util.MOUSEBUTTON_LEFT:
            evt = Event.ON_CLICKDOWN
            self.__clicked = {
                n for n in self.iter_nodes()
                if self.__check_pos_over(pgevt.pos, n)
            }
            for n in self.__clicked:
                n.set_clicked(True)
        elif pgevt.button == Util.MOUSEBUTTON_RIGHT:
            evt = Event.ON_CLICKDOWNRIGHT
        else:
            return False

        result = self.__event(evt, pgevt)

        return result

    def __pg_key_down(self, pgevt):
        return self.__event(Event.ON_KEY, pgevt)

    def __bind_key(self, pgevt):
        bind = Keys.action(pgevt.key, pg.key.get_pressed())
        if bind is None:
            return False

        def activate_focus():
            return self.activate_focus()

        def close_window():
            win = self.window_system.top_window()
            if win is not None:
                win.close()
            return True

        def move_focus_forward():
            return self.move_focus(True)

        def move_focus_backward():
            return self.move_focus(False)

        def user_defined(fun):
            def do():
                fun()
                return True
            return do
        act, fun = bind
        acts = {
            Keys.ACT_ACTIVATE_FOCUS: activate_focus,
            Keys.ACT_CLOSE_WINDOW: close_window,
            Keys.ACT_MOVE_FOCUS_FORWARD: move_focus_forward,
            Keys.ACT_MOVE_FOCUS_BACKWARD: move_focus_backward,
            Keys.ACT_USER_DEFINED: user_defined(fun)
        }
        if act in acts:
            return acts[act]()
        return False

    def process_pg_event(self, pgevt):
        '''@TODO@'''
        result = False
        if pgevt.type == pg.MOUSEBUTTONDOWN:
            result = self.__pg_mouse_button_down(pgevt)
        elif pgevt.type == pg.MOUSEBUTTONUP:
            result = self.__pg_mouse_button_up(pgevt)
        elif pgevt.type == pg.MOUSEMOTION:
            if not self.is_root_manager() or pgevt.pos == pg.mouse.get_pos():
                result = self.__pg_mouse_motion(pgevt)
        elif pgevt.type == pg.KEYDOWN:
            result = self.__pg_key_down(pgevt)
            if self.is_root_manager() and not result:
                result = self.__bind_key(pgevt)
        if result:
            self.updated = True

            #  since size of content may have been reset we have to
            #  recompute it
            self.content.compute_size()
        return result

    def iter_nodes(self):
        '''iterate on all the nodes of the manager'''
        for node in self.content.iter_tree():
            yield node
        for floating in self.__floating:
            for node in floating.iter_tree():
                yield node

    def clear(self):
        '''@TODO@'''
        result = self.__event(
            Event.ON_UNOVER, None, check_pos=False, incl=self.__overed)
        for n in self.__clicked:
            result = n.set_clicked(False) or result
        for n in self.__overed:
            result = n.set_overed(False) or result
        self.__clicked = set()
        self.__overed = set()
        return result
