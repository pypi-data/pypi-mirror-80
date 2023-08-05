#!/usr/bin/env python3

'''definition of class Rule'''

from . import Draw, Node, Media


class Rule(Node):
    '''Rule nodes are simple lines that occupy all the width of their
    container (for horizontal rules) and all the height of their
    container (for vertical rules)'''

    def __init__(self, **kwargs):
        '''create a rule'''
        Node.__init__(self, **kwargs)

    def __str__(self):
        return 'rule'

    def _compute_inner_size(self):
        if self.container_size is None:
            w, h = 0, 0
        else:
            w, h = self.container_size
        if self.get_style('orientation') == 'horizontal':
            i = self.get_style('image-hrule')
            h = self.get_style('width') if i is None \
                else Media.get_image(i[0]).get_height()
        else:
            i = self.get_style('image-vrule')
            w = self.get_style('width') if i is None \
                else Media.get_image(i[0]).get_width()
        return w, h

    def _draw(self, surface):
        orientation = self.get_style('orientation')
        w, h = self.inner_size
        x, y = self.container_pos
        imgs = self.get_style('image-vrule') if orientation == 'vertical'\
            else self.get_style('image-hrule')
        if imgs is None:
            Draw.rectangle(surface, self.get_style('color'), (x, y, w, h))
        else:
            start, unit, end = (Media.get_image(img) for img in imgs)
            surface.blit(start, (x, y))
            if orientation == 'horizontal':
                shift = start.get_width()
                while shift < w:
                    rect = None
                    if unit.get_width() + shift > w:
                        rect = (0, 0, w - shift, unit.get_height())
                    surface.blit(unit, (x + shift, y), rect)
                    shift += unit.get_width()
                surface.blit(end, (x + w - end.get_width(), y))
            else:
                shift = start.get_height()
                while shift < h:
                    rect = None
                    if unit.get_height() + shift > h:
                        rect = (0, 0, unit.get_width(), h - shift)
                    surface.blit(unit, (x, y + shift), rect)
                    shift += unit.get_height()
                surface.blit(end, (x, y + h - end.get_height()))

    def has_relative_size(self):
        return True
