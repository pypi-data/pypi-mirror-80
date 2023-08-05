#!/usr/bin/env python3

'''@TODO@'''

import re
import inspect
import xml.etree.ElementTree as ET
import pygame as pg


class Util:
    '''@TODO@'''

    #  constants taken from pygame
    MOUSEBUTTON_LEFT = 1
    MOUSEBUTTON_RIGHT = 3
    MOUSEBUTTON_WHEEL_DOWN = 4
    MOUSEBUTTON_WHEEL_UP = 5

    RE_RGB = re.compile(r'\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*')

    @classmethod
    def in_range(cls, value, bounds):
        '''@TODO@'''
        min_val, max_val = bounds
        result = value
        if min_val is not None:
            result = max(result, min_val)
        if max_val is not None:
            result = min(result, max_val)
        return result

    @classmethod
    def split_lines(cls, text, font, color, width=0):
        '''@TODO@'''
        def traverse(elem, style):
            yield from split(elem.text, style)
            for child in elem:
                child_style = dict(style)
                if child.tag == 'color':
                    try:
                        match = Util.RE_RGB.search(child.attrib['rgb'])
                    except KeyError:
                        raise ValueError(
                            'rgb attribute is expected for color tag')
                    if match:
                        child_style['color'] = tuple(map(int, match.groups()))
                    else:
                        raise ValueError(
                            'cannot parse rgb color {}'.format(
                                child.attrib['rgb']))
                else:
                    raise ValueError('undefined tag: {}'.format(child.tag))
                yield from traverse(child, child_style)
                yield from split(child.tail, style)
        def split(text, style):
            if text is not None:
                yield text, style
        def style_color(style):
            return style.get('color', color)
        def yield_surface():
            size = (sum(map(lambda s: s.get_width(), surfaces)),
                    max(map(lambda s: s.get_height(), surfaces), default=0))
            if size[0] > 0:
                surface = pg.Surface(size).convert_alpha()
                surface.fill((0, 0, 0, 0))
                w = 0
                for surf in surfaces:
                    surface.blit(surf, (w, 0))
                    w += surf.get_width()
                yield surface
        text = str(text).replace('\n', ' ')
        line = ''
        surfaces = list()
        for block, style in traverse(
                ET.fromstring('<root>' + text + '</root>'), {}):
            first = True
            for word in block.split(' '):
                if not first:
                    word = ' ' + word
                if font.size(line)[0] + font.size(word)[0] > width > 0:
                    yield from yield_surface()
                    line = ''
                    if not first:
                        word = word[1:]
                    surfaces = list()
                surfaces.append(font.render(word, 1, style_color(style)))
                line += word
                first = False
        yield from yield_surface()

    @classmethod
    def check_type(cls, value, typ, name=None, none_accepted=False):
        '''@TODO@'''
        if none_accepted and value is None:
            return
        if not isinstance(value, typ):
            msg = 'in {}:{}: {} is of type {}. type {} is expected'.format(
                inspect.stack()[1].filename,
                inspect.stack()[1].lineno,
                name if name is not None else 'value',
                type(value).__name__, typ.__name__)
            raise ValueError(msg)

    @classmethod
    def pos_align(cls, pos, size,  # pylint: disable=R0913
                  cont_size, halign, valign):
        '''@TODO@'''
        if cont_size is None:
            return pos
        x, y = pos
        w, h = size
        cw, ch = cont_size
        if halign == 'center':
            x += int((cw - w) / 2)
        elif halign == 'right':
            x += cw - w
        if valign == 'center':
            y += int((ch - h) / 2)
        elif valign == 'bottom':
            y += ch - h
        return x, y
