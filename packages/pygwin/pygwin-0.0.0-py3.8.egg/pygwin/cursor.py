#!/usr/bin/env python3

'''definition of class Cursor'''

import logging
import pygame as pg

from . import Context
from . import Media


class Cursor:
    '''class Cursor contains various functions for cursor management.
    cursor images can be associated with contexts.  contexts can be
    turned on/off and work as priorities (Context.BASE <
    Context.OVERED < Context.CLICKED).  for instance, if contexts
    Context.BASE and Context.OVERED are both on, then the cursor image
    is the one associated with the OVERED context.  if not present it
    is the one of the BASE context'''

    __ON = False
    __IMG = dict()
    __DEFAULT = dict()
    __CTX = set([Context.BASE])
    __PRIORITY = [Context.CLICKED, Context.OVERED, Context.BASE]

    @classmethod
    def set_context(cls, ctx):
        '''turn context ctx on'''
        Cursor.__CTX.add(ctx)

    @classmethod
    def unset_context(cls, ctx):
        '''turn context ctx off'''
        if ctx in Cursor.__CTX:
            Cursor.__CTX.remove(ctx)

    @classmethod
    def get(cls):
        '''get the pygame Surface of the current cursor according to the
        context'''
        for ctx in Cursor.__PRIORITY:
            if ctx in Cursor.__CTX:
                img = Cursor.__IMG.get(ctx)
                if img is not None:
                    return img
                img = Cursor.__DEFAULT.get(ctx)
                if img is not None:
                    return img
        return None

    @classmethod
    def set(cls, path, ctx=Context.BASE):
        '''set the cursor image of context ctx.  does nothing if the cursor
        system has not been activated'''
        if not Cursor.__ON:
            return
        media = Media.get_image(path)
        if media is not None:
            Cursor.__IMG[ctx] = media

    @classmethod
    def unset(cls, ctx):
        '''unset the cursor image of context ctx'''
        if ctx in Cursor.__IMG:
            del Cursor.__IMG[ctx]

    @classmethod
    def set_default(cls, path, ctx=Context.BASE):
        '''set the default image file of context ctx'''
        media = Media.get_image(path)
        if media is not None:
            Cursor.__DEFAULT[ctx] = media

    @classmethod
    def draw(cls, surface, pos):
        '''draw the current cursor on surface at position pos'''
        if Cursor.__ON and Cursor.__IMG is not None:
            img = Cursor.get()
            if img is not None:
                surface.blit(img, pos)
            else:
                logging.error('default cursor image is not set')

    @classmethod
    def activate(cls):
        '''activate the cursor system.  the cursor image of the base context
        must have been set before this to work.  if successful, the
        system cursor becomes invisible'''
        if Context.BASE not in Cursor.__DEFAULT:
            logging.error('default cursor image is not set')
        else:
            Cursor.__ON = True
            Cursor.__CTX = set([Context.BASE])
            pg.mouse.set_visible(False)

    @classmethod
    def deactivate(cls):
        '''deactivate the cursor system.  the system cursor becomes visible
        again'''
        Cursor.__ON = False
        pg.mouse.set_visible(True)

    @classmethod
    def activated(cls):
        '''check if the cursor system has been activated'''
        return Cursor.__ON
