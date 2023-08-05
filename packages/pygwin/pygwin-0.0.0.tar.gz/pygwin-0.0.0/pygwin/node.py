#!/usr/bin/env python3

'''@TODO@'''

import re
import inspect

from . import Media, Style, Event, Cursor, Coord, Draw, Util, NodeType
from . import Context, ContextStyle, StyleClass


class Node(metaclass=NodeType):  # pylint: disable=R0904,R0902
    '''@TODO@'''

    HIDDEN = 1
    FOCUS = 2
    SELECTED = 4
    DISABLED = 8
    OVERED = 16
    CLICKED = 32

    __PERCENT_EXPR = re.compile(r'\d+%')

    def __init__(self, **kwargs):
        '''@TODO@'''
        style = kwargs.get('style', {})
        cls = kwargs.get('cls', [])
        if not isinstance(cls, list):
            cls = [cls]
        self.__style = ContextStyle()
        self.__style['base'] = Style(style)
        self.__events = dict()
        self.__procs = dict()
        self.__manager = None
        self.__size = None
        self.__pos = None
        self.__parent = None
        self.__container_size = None
        self.__flags = 0
        self.__depth = 1
        self.__link = None
        self.__link_proc = None
        self.set_link(kwargs.get('link'))

        #  make the node inherit from the styles of its style-classes
        for c in cls + list(inspect.getmro(type(self))[:-1]):
            if StyleClass.exists(c):
                style = StyleClass.get(c)
                for ctx in style:
                    for attr in style[ctx]:
                        self.set_style(
                            attr, style[ctx][attr], ctx=ctx, update=False)

    @property
    def parent(self):
        '''@TODO@'''
        return self.__parent

    @property
    def style(self):
        '''@TODO@'''
        return self.__style

    @property
    def manager(self):
        '''@TODO@'''
        return self.__manager

    @property
    def container_size(self):
        '''@TODO@'''
        return self.__container_size

    @property
    def size(self):
        '''@TODO@'''
        return self.__size

    @property
    def width(self):
        '''@TODO@'''
        if self.__size is None:
            return None
        return self.__size[0]

    @property
    def height(self):
        '''@TODO@'''
        if self.__size is None:
            return None
        return self.__size[1]

    @property
    def pos(self):
        '''@TODO@'''
        return self.__pos

    @property
    def inner_size(self):
        '''@TODO@'''
        if self.size is None:
            return None
        w, h = self.size
        wdiff, hdiff = self._inner_diff()
        result = (None if w is None else w - wdiff,
                  None if h is None else h - hdiff)
        return result

    @property
    def inner_pos(self):
        '''@TODO@'''
        if self.pos is None:
            return None
        wdiff, hdiff = self._inner_diff()
        return Coord.sum(self.__pos, (int(wdiff / 2), int(hdiff / 2)))

    @property
    def depth(self):
        '''@TODO@'''
        return self.__depth

    @property
    def root_manager(self):
        '''@TODO@'''
        if self.manager is None:
            result = None
        else:
            result = self.manager.root_manager
        return result

    @property
    def absolute_pos(self):
        '''position of the node in the window system'''
        result = Coord.sum(self.pos, self.manager.absolute_pos)
        result = Coord.diff(result, self.manager.get_scroll())
        return result

    @property
    def window_pos(self):
        '''@TODO@'''
        result = self.manager.window_pos
        result = Coord.sum(result, self.pos)
        result = Coord.diff(result, self.manager.get_scroll())
        return result

    @property
    def window_system(self):
        '''@TODO@'''
        return self.manager.window_system

    @property
    def window(self):
        '''@TODO@'''
        return self.manager.window

    @property
    def bg_img(self):
        '''@TODO@'''
        if self.get_style('background') == 'image':
            return Media.get_image(self.get_style('image-background'))
        return None

    @container_size.setter
    def container_size(self, size):
        '''@TODO@'''
        if size != self.__container_size:
            self.__container_size = size
            if self.has_relative_size():
                for node in self.iter_tree():
                    node.reset_size()
                self.compute_size()

    @parent.setter
    def parent(self, parent):
        '''@TODO@'''
        self.__parent = parent

    @depth.setter
    def depth(self, depth):
        '''@TODO@'''
        self.__depth = depth

    def set_link(self, link):
        '''@TODO@'''
        self.__link = link
        if self.__link_proc is not None:
            self.del_processor(Event.ON_CLICKUP, self.__link_proc)
        if link is not None:
            def event(_):
                if self.is_clicked():
                    return self.activate()
                return False
            self.add_processor(Event.ON_CLICKUP, event)
            self.__link_proc = event

    def reset_size(self):
        '''@TODO@'''
        if self.parent is not None:
            self.parent.reset_size()
        self.__size = None

    def get_rect(self):
        '''@TODO@'''
        return Coord.rect(self.pos, self.size)

    def get_window_rect(self):
        '''@TODO@'''
        return Coord.rect(self.window_pos, self.size)

    def get_absolute_rect(self):
        '''@TODO@'''
        return Coord.rect(self.absolute_pos, self.size)

    def set_flag(self, val, flag):
        '''@TODO@'''
        if val:
            self.__flags |= flag
        else:
            self.__flags = self.__flags & ~flag

    def __set_flag_tree(self, val, flag):
        for child in self.iter_tree():
            child.set_flag(val, flag)

    def set_hidden(self, hidden):
        '''@TODO@'''
        self.__set_flag_tree(hidden, Node.HIDDEN)

    def set_selected(self, selected):
        '''@TODO@'''
        self.__set_flag_tree(selected, Node.SELECTED)

    def set_focus(self, focus):
        '''@TODO@'''
        self.__set_flag_tree(focus, Node.FOCUS)

    def set_disabled(self, disabled):
        '''@TODO@'''
        self.__set_flag_tree(disabled, Node.DISABLED)

    def is_hidden(self):
        '''@TODO@'''
        return self.__flags & Node.HIDDEN == Node.HIDDEN

    def is_selected(self):
        '''@TODO@'''
        return self.__flags & Node.SELECTED == Node.SELECTED

    def has_focus(self):
        '''@TODO@'''
        return self.__flags & Node.FOCUS == Node.FOCUS

    def is_disabled(self):
        '''@TODO@'''
        return self.__flags & Node.DISABLED == Node.DISABLED

    def is_clicked(self):
        '''@TODO@'''
        return self.__flags & Node.CLICKED == Node.CLICKED

    def set_clicked(self, clicked):
        '''@TODO@'''
        result = self.is_clicked() != clicked
        if result:
            self.set_flag(clicked, Node.CLICKED)
        return result

    def set_overed(self, overed):
        '''@TODO@'''
        self.set_flag(overed, Node.OVERED)

    def is_overed(self):
        '''@TODO@'''
        return self.__flags & Node.OVERED == Node.OVERED

    def add_child(self, node):
        '''@TODO@'''
        node.parent = self
        if self.manager is not None:
            self.manager.updated = True
        for child in node.iter_tree():
            child.set_manager(self.manager)

    def set_bubble(self, bubble, candidate_pos=None):
        '''@TODO@'''
        def pop(_):
            self.window.pop_node(
                bubble, node=self, candidate_pos=candidate_pos)
            return True

        def clear(_):
            if self.window.popped == bubble:
                self.window.clear_popped()
                return True
            return False
        self.add_processor(Event.ON_OVER, pop)
        self.add_processor(Event.ON_FOCUS, pop)
        self.add_processor(Event.ON_UNOVER, clear)
        self.add_processor(Event.ON_UNFOCUS, clear)

    def set_ctx_menu(
            self, menu, button=Util.MOUSEBUTTON_RIGHT, candidate_pos=None):
        '''@TODO@'''
        def pop(pgevt):
            win_pos = self.window.absolute_pos
            self.window.pop_node(
                menu, rect=Coord.rect(Coord.diff(pgevt.pos, win_pos), (0, 0)),
                candidate_pos=candidate_pos)
            return True
        if button == Util.MOUSEBUTTON_LEFT:
            self.add_processor(Event.ON_CLICKUP, pop)
        elif button == Util.MOUSEBUTTON_RIGHT:
            self.add_processor(Event.ON_CLICKUPRIGHT, pop)

    def clear_ctx_menu(self):
        '''@TODO@'''
        self.window.clear_popped()

    def reset_manager(self):
        '''@TODO@'''
        if self.__manager is not None:
            self.__manager.unref_proc(self)
        self.__manager = None

    def unref(self):
        '''@TODO@'''
        for node in self.iter_tree():
            node.reset_manager()

    def update_manager(self):
        '''@TODO@'''
        for manager in [self.root_manager, self.manager]:
            if manager is not None:
                manager.updated = True

    def compute_size(self):
        '''@TODO@'''
        def norm_dim(val, dim):
            if val is None or isinstance(val, int):
                return val

            #  check available size.  return None if unknown
            avail_size = self.container_size
            if avail_size is None and self.parent is None:
                if self.manager is not None:
                    avail_size = self.manager.available_size()
            if avail_size is None or avail_size[dim] is None:
                return None

            #  size is expressed as a percentage of avail_size
            m = Node.__PERCENT_EXPR.match(val)
            if not m:
                raise ValueError('could not parse size {}'.format(val))
            percent = int(val[:len(val) - 1])
            result = int(avail_size[dim] * percent / 100)
            return result

        def norm_style_size():
            img = self.bg_img
            if img is not None:
                size = img.get_size()
            else:
                size = self.get_style('size')
            if size is None:
                return None
            return norm_dim(size[0], 0), norm_dim(size[1], 1)

        #  size does not need to be recomputed
        if self.__size is not None:
            return self.__size

        size = norm_style_size()
        self.__size = size
        inner_size = self._compute_inner_size()
        result = Coord.combine(size, Coord.sum(inner_size, self._inner_diff()))
        self.__size = result
        return result

    @property
    def container_pos(self):
        '''@TODO@'''
        return Util.pos_align(
            self.pos, self.container_size, self.size,
            self.get_style('halign'), self.get_style('valign'))

    def position(self, pos):
        '''@TODO@'''

        #  change the node position according to its alignment
        self.__pos = Util.pos_align(
            pos, self.size, self.container_size,
            self.get_style('halign'), self.get_style('valign'))

        self._position(self.inner_pos)

    def __fill_background(self, surface):
        bg = self.get_style('background')
        if bg is None:
            return

        if self.container_size is not None:
            size = self.container_size
        else:
            size = self.size
        size = self.size
        pos = self.pos
        if bg == 'color':
            Draw.rectangle(
                surface,
                self.get_style('color-background'),
                Coord.rect(pos, size))
        elif bg == 'image':
            surface.blit(self.bg_img, pos)
        else:
            raise ValueError('undefined background type: {}'.format(bg))

    def __draw_border_images(self, surface):
        tl, tr, bl, br, hb, vb = map(
            Media.get_image, self.get_style('image-border'))

        #  blit horizontal bars
        w = self.size[0] - (tl.get_width() + tr.get_width())
        x = tl.get_width()
        while w > 0:
            if hb.get_width() > w:
                rect = Coord.rect((0, 0), (w, hb.get_height()))
            else:
                rect = None
            pos = Coord.sum(self.pos, (x, 0))
            surface.blit(hb, pos, rect)
            pos = Coord.sum(self.pos, (x, self.size[1] - hb.get_height()))
            surface.blit(hb, pos, rect)
            w -= hb.get_width()
            x += hb.get_width()

        #  blit vertical bars
        h = self.size[1] - (tl.get_height() + tr.get_height())
        y = tl.get_height()
        while h > 0:
            if vb.get_height() > h:
                rect = Coord.rect((0, 0), (vb.get_width(), h))
            else:
                rect = None
            pos = Coord.sum(self.pos, (0, y))
            surface.blit(vb, pos, rect)
            pos = Coord.sum(self.pos, (self.size[0] - vb.get_width(), y))
            surface.blit(vb, pos, rect)
            h -= hb.get_height()
            y += hb.get_height()

        #  blit corner images
        w, h = self.size
        for img, pos in [
                (tl, (0, 0)),
                (tr, (w, 0)),
                (bl, (w, h)),
                (br, (0, h))]:
            x, y = pos
            if x > 0:
                x -= img.get_width()
            if y > 0:
                y -= img.get_width()
            pos = Coord.sum((x, y), self.pos)
            surface.blit(img, pos)

    def __draw_border(self, surface):
        border = self.get_style('border')
        if border == 'image':
            self.__draw_border_images(surface)
        elif border == 'color':
            color = self.get_style('color-border')
            width = self.get_style('border-width')
            if width > 0:
                Draw.rectangle(
                    surface, color, Coord.rect(self.pos, self.size), width)
        elif border is not None:
            raise ValueError('invalid border type: {}'.format(border))

    def draw(self, surface):
        '''@TODO@'''
        if self.is_hidden():
            return
        self.__fill_background(surface)
        self.__draw_border(surface)
        self._draw(surface)

    def iter_tree(self):
        '''@TODO@'''
        yield self
        yield from self._iter_tree()

    def is_over(self, pos):
        '''@TODO@'''
        return self.__pos is not None and \
            self.__size is not None and \
            self.__manager is not None and \
            Coord.in_rect(self.get_absolute_rect(), pos)

    def disable(self):
        '''@TODO@'''
        self.set_disabled(True)
        for node in self.iter_tree():
            if node.manager is not None:
                node.manager.trigger(Event.ON_DISABLE, None, node)

    def enable(self):
        '''@TODO@'''
        self.set_disabled(False)
        for node in self.iter_tree():
            if node.manager is not None:
                node.manager.trigger(Event.ON_ENABLE, None, node)

    def focus_lookup(self, _, searched, previous):  # pylint: disable=R0201
        '''@TODO@'''
        return searched, previous

    def can_grab_focus(self):
        '''@TODO@'''
        return self.__link is not None

    def get_focus(self):
        '''@TODO@'''
        if self.has_focus():
            return
        self.set_focus(True)
        if self.manager is not None:
            self.manager.trigger(Event.ON_FOCUS, None, self)
            self.root_manager.give_focus(self)

    def lose_focus(self):
        '''@TODO@'''
        if not self.has_focus():
            return
        self.set_focus(False)
        if self.manager is not None:
            self.manager.trigger(Event.ON_UNFOCUS, None, self)
            self.root_manager.remove_focus()

    def set_manager(self, manager):
        '''@TODO@'''
        if self.__manager is not None:
            self.__manager.unref_proc(self)
        self.__manager = manager
        if manager is not None:
            for evt in self.__events:
                for fun in self.__events[evt]:
                    self.__manager.register(evt, self, fun)

    def is_unref(self):
        '''@TODO@'''
        return self.__manager is None

    def activate(self):
        '''@TODO@'''
        if self.manager is None:
            return False
        if not self.is_disabled():
            result = self.manager.trigger(Event.ON_ACTIVATE, None, self)
            result = self._activate() or result
            return result
        return False

    def _activate(self):
        '''@TODO@'''
        if self.__link is not None:
            self.get_focus()
            self.__link()
            return True
        return False

    def add_processor(self, evt, proc):
        '''@TODO@'''
        if evt not in self.__events:
            self.__events[evt] = list()
        self.__events[evt].append(proc)
        if self.__manager is not None:
            self.__manager.register(evt, self, proc)

    def del_processor(self, evt, proc):
        '''@TODO@'''
        self.__events[evt] = [p for p in self.__events[evt] if p != proc]
        if self.__manager is not None:
            self.__manager.unregister(evt, self, proc)

    def process(self, evt, data):
        '''@TODO@'''
        result = False
        if evt in self.__events:
            for fun in self.__events[evt]:
                result = result or fun(data)
        return result

    def get_style(self, attr, ctx=None):
        '''@TODO@'''
        def get_style(ctx):
            def get_own_style(node):
                if ctx in node.style and attr in node.style[ctx]:
                    return True, node.style[ctx][attr]
                return False, None
            found, result = get_own_style(self)
            if found:
                return True, result
            if attr in Style.INHERITED:
                parent = self.parent
                while parent is not None:
                    found, result = get_own_style(parent)
                    if found:
                        return True, result
                    parent = parent.parent
            return False, None
        if ctx is None:
            for c in Context.PRIORITY:
                if Context.check(self, c):
                    found, result = get_style(c)
                    if found:
                        return result
        else:
            found, result = get_style(ctx)
            if found:
                return result
        return self.__style[Context.BASE][attr]

    def set_style(self, attr, value, ctx=Context.BASE, update=True):
        '''@TODO@'''
        def change_style(evt):
            def do(pgevt):
                for ctx in Context.PRIORITY:
                    sound = self.get_style('sound', ctx=ctx)
                    if sound is None:
                        continue
                    has_ctx = Context.check(self, ctx)
                    if evt in Context.EVTS_ON[ctx] and has_ctx:
                        if evt == Event.ON_KEY and \
                           (not self.has_focus() or \
                            not self.does_process_key(pgevt.unicode)):
                            return False
                        Media.play_sound(sound)
                for ctx in Context.PRIORITY:
                    cursor = self.get_style('cursor', ctx=ctx)
                    if cursor is None:
                        continue
                    has_ctx = Context.check(self, ctx)
                    if evt in Context.EVTS_ON[ctx] and has_ctx:
                        Cursor.set_context(ctx)
                        Cursor.set(cursor, ctx=ctx)
                    elif evt in Context.EVTS_OFF[ctx] and not has_ctx:
                        Cursor.unset_context(ctx)
                        Cursor.unset(ctx)
                return True
            return do

        #  change the attribute in the style dictionary.  exit if the
        #  attribute is not updated
        if not self.style.set_attr(ctx, attr, value, update=update):
            return

        self.update_manager()
        self.reset_size()

        pred = lambda evt: evt not in self.__procs
        for evt in filter(pred, Context.EVTS_ON[ctx] + Context.EVTS_OFF[ctx]):
            proc = change_style(evt)
            self.add_processor(evt, proc)
            self.__procs[evt] = proc

    def does_process_key(self, _):  # pylint: disable=R0201
        '''@TODO@'''
        return False

    def _compute_inner_size(self):  # pylint: disable=R0201
        return 0, 0

    def _position(self, pos):
        pass

    def _iter_tree(self):  # pylint: disable=R0201
        yield from []

    def _draw(self, surface):
        pass

    def _inner_diff(self):
        padding = self.get_style('padding')
        border = self.get_style('border')
        if border == 'image':
            border = Media.get_image(
                self.get_style('image-border')[4]).get_height()
        elif border == 'color':
            border = self.get_style('border-width')
        elif border is not None:
            raise ValueError('invalid border type: {}'.format(border))
        else:
            border = 0
        if isinstance(padding, int):
            diff = 2 * (border + padding)
            result = diff, diff
        else:
            left, top = padding
            result = 2 * (border + left), 2 * (border + top)
        return result

    def has_relative_size(self):
        '''@TODO@'''
        s = self.get_style('size')
        if s is not None and (isinstance(s[0], str) or isinstance(s[1], str)):
            return True
        w = self.get_style('width')
        if w is not None and isinstance(w, str):
            return True
        return False

    def get_font(self):
        '''@TODO@'''
        return Media.get_font(
            self.get_style('font'), size=self.get_style('font-size'))
