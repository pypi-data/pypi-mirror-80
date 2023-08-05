#!/usr/bin/env python3

'''definition of class Draw'''

import math
import pygame as pg


class Draw:
    '''defines several drawing functions'''

    BLACK = (0, 0, 0, 0)

    @classmethod
    def intersection(cls, line1, line2):
        '''return the intersection points of two lines given as point couples.
        return None, if the two lines do not intersect'''
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            result = None
        else:
            d = (det(*line1), det(*line2))
            result = (int(round(det(d, xdiff) / div, 0)),
                      int(round(det(d, ydiff) / div, 0)))
        return result

    @classmethod
    def on_line(cls, line, pt):
        '''return True if pt is on line (given as a point couple), False
        otherwise'''
        (x0, y0), (x1, y1) = line
        xp, yp = pt
        if x0 == x1:
            return xp == x0 and min(y0, y1) <= yp <= max(y0, y1)
        a = (y0 - y1) / (x0 - x1)
        b = ((x0 * y1) - (y0 * x1)) / (x0 - x1)
        return yp == a * xp + b

    @classmethod
    def rectangle(cls, surface, color, rect, width=0):
        '''draw rectangle rect on the surface with the given color and width'''
        x, y, w, h = rect
        if w == 0 or h == 0:
            return
        if width == 0 or width is None:
            pg.draw.rect(surface, color, rect)
        else:
            if width > 2 * w or width > 2 * h:
                msg = 'incorrect width for a ({}, {}) rectangle: {}'.format(
                    w, h, width)
                raise ValueError(msg)
            pg.draw.rect(surface, color, (x, y, w, width))
            pg.draw.rect(surface, color, (x, y, width, h))
            pg.draw.rect(surface, color, (x + w - width, y, width, h))
            pg.draw.rect(surface, color, (x, y + h - width, w, width))

    @classmethod
    def rounded_rectangle(cls, surface, color,  # pylint: disable=R0913
                          rect, radius, width=0):
        '''draw a rounded rectangle with corners having the given radius'''
        x, y, w, h = rect
        radius = min(radius, int(w / 2), int(h / 2))
        if radius == 0:
            Draw.rectangle(surface, color, rect, width)
            return

        if width == 0 or width is None:
            rects = [(x + radius, y, w - 2 * radius + 1, radius),
                     (x, y + radius, w, h - 2 * radius),
                     (x + radius, y + h - radius, w - 2 * radius + 1, radius)]
            arcs = [((x + radius, y + radius), math.pi / 2, math.pi),
                    ((x + w - radius, y + radius), 0, math.pi / 2),
                    ((x + radius, y + h - radius), math.pi, 3 * math.pi / 2),
                    ((x + w - radius, y + h - radius), 3 * math.pi / 2, 0)]
        else:
            rects = [(x + radius, y, w - 2 * radius + 1, width),
                     (x + radius, y + h - width, w - 2 * radius + 1, width),
                     (x, y + radius, width, h - 2 * radius),
                     (x + w - width, y + radius, width, h - 2 * radius)]
            arcs = [((x + radius, y + radius), math.pi / 2, math.pi),
                    ((x + w - radius, y + radius), 0, math.pi / 2),
                    ((x + radius, y + h - radius), math.pi, 3 * math.pi / 2),
                    ((x + w - radius, y + h - radius), 3 * math.pi / 2, 0)]
        for r in rects:
            Draw.rectangle(surface, color, r)
        for arc in arcs:
            Draw.arc(surface, color, arc[0], radius, arc[1], arc[2], width)

    @classmethod
    def circle(cls, surface, color,  # pylint: disable=R0913
               origin, radius, width=0):
        '''draw a circle'''
        if width == 0:
            pg.draw.circle(surface, color, origin, radius)
        else:
            circle = pg.Surface((radius * 2, radius * 2)).convert_alpha()
            circle.fill(Draw.BLACK)
            pg.draw.circle(
                circle, color, (radius, radius), radius)
            pg.draw.circle(
                circle, Draw.BLACK, (radius, radius), radius - width)
            surface.blit(circle, (origin[0] - radius, origin[1] - radius))

    @classmethod
    def arc(cls, surface, color, origin,  # pylint: disable=R0913
            radius, start, end, width=0):
        '''draw an arc'''
        def get_extremities(frame, start, end):
            start = (radius + int(round(radius * math.cos(start), 0)),
                     radius + int(round(radius * math.sin(start), 0)))
            end = (radius + int(round(radius * math.cos(end), 0)),
                   radius + int(round(radius * math.sin(end), 0)))
            for pt in [start, end]:
                prev = frame[0]
                for corner in frame[1:]:

                    #  compute the intersection point between the frame
                    #  line and (circle center, circle point)
                    frame_line = (corner, prev)
                    inter = Draw.intersection(frame_line, (center, pt))
                    prev = corner

                    # check there's an intersection point and this one is
                    # on the frame line
                    if inter is None or not Draw.on_line(frame_line, inter):
                        continue

                    #  check the circle point is on the line (circle
                    #  center, intersection)
                    if min(center[0], inter[0]) \
                       <= pt[0] \
                       <= max(center[0], inter[0]) \
                       and min(center[1], inter[1]) \
                       <= pt[1] \
                       <= max(center[1], inter[1]):
                        yield inter
                        break

        #  get a polygon covering the region that is outside the arc
        def get_poly(frame, extremities):
            ext_start, ext_end = extremities
            yield center
            yield ext_end
            last = ext_end
            frame = frame[1:]
            frame.reverse()
            pt = None
            while pt != ext_start:
                pt = None
                if last in frame:
                    pt = frame[frame.index(last) - 1]
                else:
                    prev = frame[-1]
                    for corner in frame:
                        if Draw.on_line((prev, corner), last):
                            pt = prev
                        prev = corner
                if Draw.on_line((last, pt), ext_start):
                    pt = ext_start
                yield pt
                last = pt
            yield center

        #  initialise the surface that will contain the arc and draw a
        #  circle on it with the given width
        center = radius, radius
        arc = pg.Surface((2 * radius, 2 * radius)).convert_alpha()
        arc.fill(Draw.BLACK)
        Draw.circle(arc, color, center, radius, width)

        frame = [(0, 0),
                 (2 * radius, 0),
                 (2 * radius, 2 * radius),
                 (0, 2 * radius), (0, 0)]

        #  draw the polygon that is outside the arc
        pg.draw.polygon(
            arc, Draw.BLACK,
            list(get_poly(frame, get_extremities(frame, start, end))))

        surface.blit(pg.transform.flip(arc, False, True),
                     (origin[0] - radius, origin[1] - radius))
