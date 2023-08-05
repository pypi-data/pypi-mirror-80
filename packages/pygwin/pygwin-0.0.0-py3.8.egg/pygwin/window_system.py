#!/usr/bin/env python3

'''@TODO@'''

import pygame as pg

from . import Animation, Coord, Cursor, Util, Context


class WindowSystem:  # pylint: disable=R0902
    '''@TODO@'''

    def __init__(self, screen):
        '''@TODO@'''
        self.__screen = screen
        self.__surface = pg.Surface(screen.get_size())
        self.__windows = list()
        self.__panels = set()
        self.__updated = list()
        self.__frozen = False
        self.__closed = False

    @property
    def screen(self):
        '''@TODO'''
        return self.__screen

    @property
    def closed(self):
        '''@TODO'''
        return self.__closed

    @closed.setter
    def closed(self, closed):
        '''@TODO'''
        self.__closed = closed

    def freeze(self):
        '''@TODO@'''
        self.__frozen = True

    def unfreeze(self):
        '''@TODO@'''
        self.__frozen = False

    def top_window(self):
        '''@TODO@'''
        if self.__windows == []:
            result = None
        else:
            result = self.__windows[0]
        return result

    def center_window(self, win):
        '''@TODO@'''
        sw, sh = self.__surface.get_size()
        win.compute_size()
        w, h = win.size
        win.absolute_pos = (int((sw - w) / 2), int((sh - h) / 2))

    def open_window(self, win, pos=None):
        '''@TODO@'''
        self.__windows.insert(0, win)
        if pos is None:
            self.center_window(win)
        else:
            win.absolute_pos = pos

    def window_opened(self, win):
        '''@TODO@'''
        return win in self.__windows or win in self.__panels

    def close_window(self, win):
        '''@TODO@'''
        if win is None:
            if self.__windows == []:
                return
            win = self.__windows[0]
        if win in self.__windows:
            self.__windows = list(filter(lambda w: w != win, self.__windows))

    def close_all_windows(self):
        '''@TODO@'''
        self.__windows = list()

    def center_all_windows(self):
        '''@TODO@'''
        for win in self.__windows:
            self.center_window(win)

    def open_panel(self, panel, pos):
        '''@TODO@'''
        self.__panels.add(panel)
        panel.absolute_pos = pos

    def close_panel(self, panel):
        '''@TODO@'''
        if panel in self.__panels:
            self.__panels.remove(panel)

    def process_pg_event(self, pgevt):
        '''@TODO@'''
        def dispatch():
            result = False
            for win in self.__windows + list(self.__panels):
                result = win.process_pg_event(pgevt)
                if result or win.modal:
                    break
            return result

        #  update the cursor image
        if pgevt.type == pg.MOUSEBUTTONDOWN:
            if pgevt.button == Util.MOUSEBUTTON_LEFT:
                Cursor.set_context(Context.CLICKED)
        elif pgevt.type == pg.MOUSEBUTTONUP:
            if pgevt.button == Util.MOUSEBUTTON_LEFT:
                Cursor.unset_context(Context.CLICKED)

        result = not self.__frozen and dispatch()
        return result

    def draw(self, update=False):
        '''@TODO@'''
        self.__surface.fill((0, 0, 0))
        for win in list(self.__panels) + self.__windows[::-1]:
            win.blit(self.__surface)
        self.__screen.blit(self.__surface, (0, 0))
        self.__draw_cursor()
        if update:
            pg.display.update()

    def update_window(self, win, surface, rect, update):
        '''@TODO@'''
        x, y, w, h = rect
        pt = Coord.sum((x, y), win.absolute_pos)
        pt = x, y
        self.__surface.blit(surface, pt, area=(0, 0, w, h))
        self.__updated.append(rect)
        if update:
            self.update_display()

    def update_display(self):
        '''@TODO@'''
        self.__draw_cursor()
        self.__screen.blit(self.__surface, (0, 0))
        pg.display.update(self.__updated)
        self.__updated = list()

    def set_surface(self, screen):
        '''@TODO@'''
        self.__screen = screen
        self.__surface = pg.Surface(screen.get_size())

    def loop(self, fps):
        '''@TODO@'''
        clock = pg.time.Clock()
        self.draw(update=True)
        while not self.closed:
            redraw = False
            cursor_updated = False
            redraw = Animation.run_all()
            for pgevt in pg.event.get():
                if pgevt.type == pg.QUIT:
                    self.closed = True
                redraw = self.process_pg_event(pgevt) or redraw
                cursor_updated = cursor_updated or \
                    (Cursor.activated() and pgevt.type in [
                        pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP, pg.MOUSEMOTION])
            self.draw(update=True)
            if redraw:
                self.draw(update=True)
            elif cursor_updated:
                self.__screen.blit(self.__surface, (0, 0))
                self.__draw_cursor()
                pg.display.update()
            clock.tick(fps)

    def __draw_cursor(self):
        if Cursor.activated():
            Cursor.draw(self.__screen, pg.mouse.get_pos())
