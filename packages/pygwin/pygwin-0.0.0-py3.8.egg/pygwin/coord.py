#!/usr/bin/env python3

'''definition of class Coord'''


class Coord:
    '''contains basic class methods to work with (x, y) coordinates'''

    ABSOLUTE = 'absolute'
    RELATIVE = 'relative'

    LEFT = 'left'
    MIDDLE = 'middle'
    RIGHT = 'right'
    TOP = 'top'
    BOTTOM = 'bottom'

    @classmethod
    def diff(cls, c1, c2):
        '''get the difference of two coordinates'''
        return c1[0] - c2[0], c1[1] - c2[1]

    @classmethod
    def sum(cls, c1, c2):
        '''get the sum of two coordinates'''
        return c1[0] + c2[0], c1[1] + c2[1]

    @classmethod
    def in_rect(cls, rect, pt):
        '''check if point pt is in rectangle rect'''
        x, y = pt
        xr, yr, w, h = rect
        return xr <= x < xr + w and yr <= y < yr + h

    @classmethod
    def gt(cls, pt1, pt2):
        '''@TODO@'''
        return pt1[0] > pt2[0] and pt1[1] > pt2[1]

    @classmethod
    def ge(cls, pt1, pt2):
        '''@TODO@'''
        return Coord.gt(pt1, pt2) or pt1 == pt2

    @classmethod
    def rect_of(cls, pt1, pt2):
        '''return the pygame rectangle (x, y, width, height) having pt1 and
        pt2 as opposite corners'''
        x1, y1 = pt1
        x2, y2 = pt2
        return min(x1, x2), min(x2, y2), abs(x1 - x2), abs(y1 - y2)

    @classmethod
    def absolute_to_coord(cls, pos, node_size, container_size):
        '''return an (x, y) coordinate corresponding to position pos given as
        an ((xcoord, x), (ycoord, y)) couple with xcoord in [LEFT,
        RIGHT, MIDDLE] and ycoord in [TOP, BOTTOM, MIDDLE].  node_size
        is the size of the node of which we compute the coordinates.
        container_size is the size of the container (e.g., a window)
        this node is put in'''
        (xcoord, x), (ycoord, y) = pos
        w, h = node_size
        cw, ch = container_size
        if xcoord == Coord.RIGHT:
            x = cw - w - x
        elif xcoord == Coord.MIDDLE:
            x = int((cw - w) / 2)
        if ycoord == Coord.BOTTOM:
            y = ch - h - y
        elif ycoord == Coord.MIDDLE:
            y = int((ch - h) / 2)
        return x, y

    @classmethod
    def relative_to_coord(cls, pos, node_size, rect):
        '''return an (x, y) coordinate corresponding to position pos given as
        an ((xcoord, x), (ycoord, y)) couple with xcoord in [LEFT,
        RIGHT, MIDDLE] and ycoord in [TOP, BOTTOM, MIDDLE].  node_size
        is the size of the node of which we compute the coordinates.
        rect is the rectangle of which position pos is relative to'''
        (xcoord, x), (ycoord, y) = pos
        rx, ry, rw, rh = rect
        nw, nh = node_size
        if xcoord == Coord.RIGHT:
            x = rx + rw
        elif xcoord == Coord.MIDDLE:
            x = rx + int((rw - nw) / 2)
        else:
            x = rx - nw
        if ycoord == Coord.BOTTOM:
            y = ry + rh
        elif ycoord == Coord.MIDDLE:
            y = ry + int((rh - nh) / 2)
        else:
            y = ry - nh
        return x, y

    @classmethod
    def rect(cls, pos, size):
        '''return a rectangle from (x, y) position pos and (width, height)
        size'''
        return pos[0], pos[1], size[0], size[1]

    @classmethod
    def combine(cls, c0, c1):
        '''@TODO@'''
        if c0 is None:
            return c1
        return (c0[0] if c0[0] is not None else c1[0],
                c0[1] if c0[1] is not None else c1[1])
