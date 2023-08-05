#!/usr/bin/env python3

'''@TODO@'''

import pygame as pg


class Animation:
    '''@TODO@'''

    __ALL = list()

    def __init__(self, prog, period, handler):
        '''@TODO@'''
        self.__prog = prog
        self.__period = period
        self.__handler = handler
        self.__last = pg.time.get_ticks()
        self.__paused = False

    @property
    def prog(self):
        '''@TODO@'''
        return self.__prog

    def pause(self):
        '''@TODO@'''
        self.__paused = True

    def start(self):
        '''@TODO@'''
        self.__paused = False
        self.__prog = self.__handler(self.__prog)
        if self.__prog is not None:
            Animation.__ALL.append(self)

    def done(self):
        '''@TODO'''
        return self.__prog is None

    def stop(self):
        '''@TODO'''
        self.__prog = None

    def check_run(self):
        '''@TODO'''
        return not self.__paused and \
            self.__prog is not None and \
            pg.time.get_ticks() - self.__last >= self.__period

    def run(self):
        '''@TODO'''
        self.__prog = self.__handler(self.__prog)
        self.__last = pg.time.get_ticks()

    @classmethod
    def run_all(cls):
        '''@TODO'''
        result = False
        done = []
        for anim in Animation.__ALL:
            if anim.check_run():
                anim.run()
                result = True
            if anim.done():
                done.append(anim)
        if done != []:
            Animation.__ALL = list(filter(
                lambda a: a not in done, Animation.__ALL))
        return result
