#!/usr/bin/env python3

'''definition of class Checkbox'''

from . import Draw, Event, ValuedNode, Coord, Media


class Checkbox(ValuedNode):
    '''Checkbox are square boxes used to select options'''

    def __init__(self, **kwargs):
        '''kwarg value is True if the checkbox is initially checked'''
        def click_event(_):
            return self.activate()
        kwargs['value'] = kwargs.get('value', False)
        ValuedNode.__init__(self, **kwargs)
        self.add_processor(Event.ON_CLICKUP, click_event)

    def __str__(self):
        return 'checkbox({})'.format(self.value)

    def can_grab_focus(self):
        '''overload Node.can_grab_focus'''
        return True

    def _activate(self):
        '''activate checkbox which is equivalent to having the user clicking
        on it'''
        self.get_focus()
        self.set_value(not self.value)
        return True

    def _compute_inner_size(self):
        imgs = self.get_style('image-checkbox')
        if imgs is not None:
            return Media.get_image(imgs[int(self.value)]).get_size()
        return 20, 20

    def _draw(self, surface):
        imgs = self.get_style('image-checkbox')
        if imgs is not None:
            img = Media.get_image(imgs[int(self.value)])
            surface.blit(img, self.inner_pos)
        elif self.value:
            color = self.get_style('color')
            Draw.rectangle(
                surface, color, Coord.rect(self.inner_pos, self.inner_size))
