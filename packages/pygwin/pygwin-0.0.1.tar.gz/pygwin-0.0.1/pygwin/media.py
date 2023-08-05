#!/usr/bin/env python3

'''@TODO@'''

import logging
import functools
import pygame as pg


class Media:
    '''@TODO@'''

    IMAGE = 'img'
    FONT = 'font'
    SOUND = 'sound'

    CACHE_SIZE = 10000

    @classmethod
    @functools.lru_cache(maxsize=CACHE_SIZE)
    def get(cls, mtype, path, **kwargs):
        '''@TODO@'''
        if path is None:
            return None

        try:
            if mtype == Media.IMAGE:
                result = pg.image.load(path).convert_alpha()
                rotate = kwargs.get('rotate')
                if rotate is not None:
                    result = pg.transform.rotate(result, rotate)
                scale = kwargs.get('scale')
                if scale is not None:
                    result = pg.transform.scale(result, scale)
            elif mtype == Media.FONT:
                result = pg.font.Font(path, kwargs.get('size', 24))
            elif mtype == Media.SOUND:
                result = pg.mixer.Sound(path)
        except (pg.error, FileNotFoundError):
            logging.error('could not load media file "%s"', path)
            result = None
        return result

    @classmethod
    def get_image(cls, img, **kwargs):
        '''@TODO@'''
        return img if isinstance(img, pg.Surface) \
            else Media.get(Media.IMAGE, img, **kwargs)

    @classmethod
    def get_font(cls, path, **kwargs):
        '''@TODO@'''
        return Media.get(Media.FONT, path, **kwargs)

    @classmethod
    def get_sound(cls, path, **kwargs):
        '''@TODO@'''
        return Media.get(Media.SOUND, path, **kwargs)

    @classmethod
    def play_sound(cls, path, wait=False):
        '''@TODO@'''
        sound = Media.get(Media.SOUND, path)
        result = None
        if sound is not None:
            logging.info('playing sound %s', path)
            result = sound.play()
            if wait:
                Media.wait_sound(result)
                result = None
        return result

    @classmethod
    def wait_sound(cls, channel):
        '''@TODO@'''
        if channel is not None:
            while channel.get_busy():
                pg.time.wait(10)
