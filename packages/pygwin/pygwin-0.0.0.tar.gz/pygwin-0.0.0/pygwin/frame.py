#!/usr/bin/env python3

'''@TODO@'''

import math
import pygame as pg

from . import Coord, Draw, Event, Node, EventManager, Util, Media


class Frame(Node, EventManager):
    '''@TODO@'''

    def __init__(self, node, **kwargs):
        '''@TODO@'''
        def propagate(pgevt):
            result = EventManager.process_pg_event(self, pgevt)
            if result:
                self.updated = True
            return result

        def click_down(pgevt):
            if self.__scroll_vertical(pgevt.pos, True):
                self.__vscrolling = True
                return True
            return propagate(pgevt)

        def click(pgevt):
            if self.__vscrolling:
                self.__vscrolling = False
                return True
            return propagate(pgevt)

        def slide(pgevt):
            if self.__vscrolling:
                return self.__scroll_vertical(pgevt.pos, False)
            return propagate(pgevt)

        def key(pgevt):
            if propagate(pgevt):
                return True
            result = False
            pts = None
            unit = self.get_style('frame-bar-wheel-pt-units')
            if pgevt.key == pg.K_DOWN:
                pts = unit
            elif pgevt.key == pg.K_UP:
                pts = - 1 * unit
            elif pgevt.key == pg.K_PAGEDOWN:
                pts = 10 * unit
            elif pgevt.key == pg.K_PAGEUP:
                pts = - 10 * unit
            if pts is not None:
                result = self.__vertical_scroll(pts)
            return result

        def mouse_wheel(pgevt):
            if propagate(pgevt):
                return True
            if not self.__has_vertical_scroll_bar():
                return False
            move = None
            pts = self.get_style('frame-bar-wheel-pt-units')
            if pgevt.button is Util.MOUSEBUTTON_WHEEL_DOWN:
                move = pts * - 1
            elif pgevt.button is Util.MOUSEBUTTON_WHEEL_UP:
                move = pts
            result = move is not None and self.__vertical_scroll(move)
            return result

        def unover(_):
            return self.clear()

        Util.check_type(node, Node, 'node')

        Node.__init__(self, **kwargs)
        EventManager.__init__(self)
        self.__scroll = [0, 0]
        self.__vscrolling = False
        self.__node = node
        self.__align_shift = 0, 0
        processed = {Event.ON_CLICKUP: click,
                     Event.ON_CLICKDOWN: click_down,
                     Event.ON_OVER: slide,
                     Event.ON_OVERAGAIN: slide,
                     Event.ON_MOUSEWHEEL: mouse_wheel,
                     Event.ON_KEY: key,
                     Event.ON_UNOVER: unover}
        for evt in Event:
            if evt not in processed:
                self.add_processor(evt, propagate)
        for proc in processed:
            self.add_processor(proc, processed[proc])
        for child in node.iter_tree():
            child.set_manager(self)

    def __str__(self):
        return 'frame(size={}, pos={}, {})'.format(
            self.size, self.pos, self.content)

    @property
    def content(self):
        return self.__node

    @property
    def hscroll(self):
        '''horizontal scrolling in pixels'''
        return self.__scroll[0]

    @property
    def vscroll(self):
        '''vertical scrolling in pixels'''
        return self.__scroll[1]

    def set_vscroll(self, vscroll):
        '''@TODO@'''
        self.__scroll[1] = vscroll
        self.update_manager()

    def scroll_bottom(self):
        '''@TODO@'''
        self.set_vscroll(self.__vscroll_bounds()[1])

    def scroll_top(self):
        '''@TODO@'''
        self.set_vscroll(self.__vscroll_bounds()[0])

    def get_scroll(self):
        '''@TODO@'''
        wd, hd = self._inner_diff()
        result = self.manager.get_scroll()
        result = Coord.sum(result, self.__scroll)
        result = Coord.diff(result, (int(wd / 2), int(hd / 2)))
        result = Coord.sum(result, self.__align_shift)
        return result

    def available_size(self):
        '''@TODO@'''
        return self.inner_size

    def compute_size(self):
        if self.size is None:
            Node.compute_size(self)
            if self.content.has_relative_size():
                self.content.reset_size()
                self.content.compute_size()
        return self.size

    def _compute_inner_size(self):
        return self.content.compute_size()

    def _draw(self, surface):
        self.draw_content()
        self.set_vscroll(
            Util.in_range(self.vscroll, self.__vscroll_bounds()))
        pos = Util.pos_align(
            self.inner_pos, self.content.size, self.inner_size,
            self.content.get_style('halign'), self.content.get_style('valign'))
        self.__align_shift = Coord.diff(self.inner_pos, pos)
        surface.blit(
            self.surface, pos, area=Coord.rect(self.__scroll, self.inner_size))
        self.__draw_scroll_bars(surface, self.inner_pos)

    def focus_lookup(self, forward, searched, previous):
        try:
            return EventManager.move_focus_loop(
                self, forward, searched, previous)
        except EventManager.NodeFound as ex:

            #  scroll if the node that now has the focus is invisible
            found = ex.node
            _, y = found.pos
            _, h = found.size
            _, ph = self.inner_size
            if y + h > self.vscroll + ph:
                self.set_vscroll(y + h - ph)
            if y < self.vscroll:
                self.set_vscroll(y)
            self.updated = True
            raise ex

    def __scroll_vertical(self, pos, check_in_bar):
        if not self.__has_vertical_scroll_bar():
            return False
        pos = Coord.diff(pos, self.absolute_pos)
        rect_container, _ = self.__get_vscroll_bar_rects()
        if not check_in_bar or Coord.in_rect(rect_container, pos):
            _, y, _, h = rect_container
            y = pos[1] - y
            _, h = self.inner_size
            _, rh = self.content.size
            newvscroll = math.ceil(rh / h * y)
            newvscroll = Util.in_range(newvscroll, self.__vscroll_bounds())
            self.set_vscroll(newvscroll)
            return True
        return False

    def __vscroll_bounds(self):
        max_height = None if self.inner_size is None else self.inner_size[1]
        if max_height is None:
            result = 0, 0
        else:
            _, ymax = self.content.size
            result = 0, max(0, ymax - max_height)
        return result

    def __has_vertical_scroll_bar(self):
        size = self.inner_size
        max_height = None if size is None else size[1]
        return max_height is not None and self.content.size[1] > max_height

    def __get_scroll_bar_sizes(self):
        w, h = self.inner_size
        rw, rh = self.content.size
        resultw, resulth = None, None
        if rh >= h and rh > 0:
            resulth = int(h * h / rh)
        if rw >= w and rw > 0:
            resultw = int(w * w / rw)
        return resultw, resulth

    def __get_vscroll_bar_rects(self):
        imgs = self.get_style('image-frame-vscroll-bar')
        if imgs is None:
            bar_width = self.get_style('frame-bar-width')
        else:
            bar_width = Media.get_image(imgs[0]).get_width()
        w, h = self.inner_size
        _, rh = self.content.size
        _, scrollh = self.__get_scroll_bar_sizes()
        x = w - bar_width
        ystart = math.ceil(self.vscroll * h / rh)
        return ((x, 0, bar_width, h),
                (x, ystart, bar_width, scrollh))

    def __draw_vscroll_bar_color(self, surface, rect_cont, rect_bar):
        col = self.get_style('color-frame-bar-container')

        #  draw the scrollbar container
        _, _, w, h = rect_cont
        Draw.rectangle(surface, col, (0, 0, w, h))

        #  draw the scrollbar
        _, y, w, h = rect_bar
        col = self.get_style('color-frame-bar')
        Draw.rectangle(surface, col, (0, y, w, h))

    def __draw_vscroll_bar_image(self, surface, rect_cont, rect_bar):
        def draw(ystart, yend, imgs):
            top, unit, bottom = imgs
            y = ystart
            surface.blit(top, (0, ystart))
            y += top.get_height()
            while y < yend:
                rect = None
                if unit.get_height() + y > yend:
                    rect = (0, 0, unit.get_width(), yend - y)
                surface.blit(unit, (0, y), rect)
                y += unit.get_height()
            surface.blit(bottom, (0, yend - bottom.get_height()))

        #  draw the container
        imgs = self.get_style('image-frame-vscroll-container')
        draw(0, rect_cont[3], list(map(Media.get_image, imgs)))

        #  draw the scrollbar
        _, y, _, h = rect_bar
        imgs = self.get_style('image-frame-vscroll-bar')
        draw(y, y + h, list(map(Media.get_image, imgs)))

    def __draw_scroll_bars(self, surface, pos):
        if self.__has_vertical_scroll_bar():
            rect_cont, rect_bar = self.__get_vscroll_bar_rects()
            x0, y0, w, h = rect_cont
            s = pg.Surface((w, h)).convert_alpha()
            s.fill((0, 0, 0, 0))
            if self.get_style('image-frame-vscroll-bar') is None:
                self.__draw_vscroll_bar_color(s, rect_cont, rect_bar)
            else:
                self.__draw_vscroll_bar_image(s, rect_cont, rect_bar)
            surface.blit(s, (pos[0] + x0, pos[1] + y0))

    def __vertical_scroll(self, pts):
        newvscroll = self.vscroll + pts
        newvscroll = Util.in_range(newvscroll, self.__vscroll_bounds())
        result = self.vscroll != newvscroll
        if result:
            self.set_vscroll(newvscroll)
        return result
