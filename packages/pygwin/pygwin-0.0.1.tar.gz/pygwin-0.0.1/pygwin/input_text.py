#!/usr/bin/env python3

'''definition of class InputText'''

import string
import pygame as pg

from . import Event, Util, ValuedNode, Coord


class InputText(ValuedNode):  # pylint: disable=R0902
    '''InputText nodes are one-line boxes in which the user can type text
    as <input type="text"> HTML elements.'''

    DEFAULT_ALLOWED = '.\'-\" ' + string.ascii_letters

    def __init__(self, **kwargs):
        '''kwarg allowed is a string or a list of allowed characters in the
        input text (i.e., if the user types a key that's not in that
        list, nothing happens).  default is InputText.DEFAULT_ALLOWED.

        kwarg max_size is the maximal number of characters that can be
        typed in the input text (None for no max).  default is None.

        kwarg place_holder is a string displayed in the input text if
        its value is empty.  default is ''.

        kwarg value is the initial value of the input text.  default
        is ''.

        kwarg prompt is a string displayed at the beginning of the
        input text.  default is ''.'''
        def click_event(_):
            if not self.is_disabled():
                self.get_focus()
                return True
            return False

        def key_event(evt):
            if not self.has_focus():
                result = False
            else:
                result = self.new_key(evt.key, evt.unicode)
            return result
        if 'value' not in kwargs:
            kwargs['value'] = ''
        ValuedNode.__init__(self, **kwargs)
        self.__place_holder = kwargs.get('place_holder')
        self.__max_size = kwargs.get('max_size')
        self.__prompt = kwargs.get('prompt')
        self.__allowed = kwargs.get('allowed', InputText.DEFAULT_ALLOWED)
        self.__cursor = 0
        self.__text_height = None
        self.__surface = None
        self.__xshift = 0
        self.__prev = None
        self.__prompt_surface = None
        self.__init_text_height()
        self.__redraw()
        self.add_processor(Event.ON_CLICKUP, click_event)
        self.add_processor(Event.ON_KEY, key_event)

    def __str__(self):
        return 'input_text({})'.format(self.value)

    def can_grab_focus(self):
        '''overload Node.can_grab_focus'''
        return True

    def is_char_allowed(self, char):
        '''check is char is allowed to be typed in the input text'''
        return char != '' and char in self.__allowed

    def does_process_key(self, uni):
        '''check if the unicode character is allowed to be typed in the input
        text'''
        return self.is_char_allowed(uni)

    def set_value(self, value, trigger=True):
        '''change the value of the input text. trigger the ON_CHANGE event of
        the input text if trigger is True'''
        ValuedNode.set_value(self, value, trigger=trigger)
        self.__cursor = Util.in_range(self.__cursor, (0, len(value)))
        self.__redraw()

    def append_value(self, value):
        '''concatenate value to the current value of the input text'''
        self.set_value(self.value + value)

    def set_cursor_at_end(self):
        '''place the cursor at the end of the input text, after the last
        character typed'''
        self.__cursor = len(self.value)

    def set_prompt(self, prompt):
        '''change the prompt of the input text'''
        self.__prompt = prompt
        self.__redraw()

    def _activate(self):
        '''activate the input text: if it has the focus, it loses it,
        otherwise it gets it'''
        if self.has_focus():
            self.lose_focus()
        else:
            self.get_focus()
        return True

    def new_key(self, key, uni):
        '''a key is pressed when the input text has the focus'''
        result = True
        val = self.value
        if key == pg.K_RETURN:
            self.lose_focus()
        elif key == pg.K_BACKSPACE:
            if self.__cursor > 0:
                self.__cursor -= 1
                self.set_value(val[:self.__cursor] + val[self.__cursor + 1:])
        elif key == pg.K_DELETE:
            if self.__cursor < len(val):
                self.set_value(val[:self.__cursor] + val[self.__cursor + 1:])
        elif key == pg.K_LEFT:
            self.__cursor = max(0, self.__cursor - 1)
        elif key == pg.K_RIGHT:
            self.__cursor = min(len(val), self.__cursor + 1)
        elif self.is_char_allowed(uni):
            if self.__max_size is None or len(val) < self.__max_size:
                char = uni
                self.set_value(val[:self.__cursor] +
                               char + val[self.__cursor:])
                self.__cursor += 1
        else:
            result = False
        if result:
            self.__redraw()
        return result

    def __init_text_height(self):
        test = self.get_font().render(self.__allowed, 1, (0, 0, 0))
        self.__text_height = test.get_height()

    def __drawn_text(self):
        if self.value == '' \
           and not self.has_focus() \
           and self.__place_holder is not None:
            result = self.__place_holder
        else:
            result = self.value
        return result

    def __max_text_width(self):
        result = self.inner_size[0]
        if self.__prompt_surface is not None:
            result = max(0, result - self.__prompt_surface.get_width())
        return result

    def __redraw(self):
        def draw_cursor(w, h):
            pg.draw.line(self.__surface, color, (w, 0), (w, h), 1)
            return w

        color = self.get_style('color')
        font = self.get_font()
        focus = self.has_focus()

        #  everything unchanged => exit
        if self.__prev == (
                focus, self.__prompt, self.value, self.__cursor, color, font):
            return

        #  draw the prompt
        if self.__prompt is not None:
            lbl = font.render(self.__prompt, 1, color)
            size = lbl.get_size()
            self.__prompt_surface = pg.Surface(size).convert_alpha()
            self.__prompt_surface.fill((0, 0, 0, 0))
            self.__prompt_surface.blit(lbl, (0, 0))

        self.__prev = \
            focus, self.__prompt, self.value, self.__cursor, color, font
        self.__init_text_height()
        cursor = self.__cursor

        #  create a surface for each letter in the text to draw and
        #  compute the width of the node surface (its width is the sum
        #  of all letter surface widths + 1 if the cursor is at the
        #  end of the text)
        w = 0
        h = self.__text_height
        letters = list()
        for letter in self.__drawn_text():
            s = font.render(letter, 1, color)
            letters.append(s)
            w += s.get_width()
        if cursor == len(letters):
            w += 1
        self.__surface = pg.Surface((w, h)).convert_alpha()
        self.__surface.fill((0, 0, 0, 0))

        #  copy all letter surfaces on the node surface and also draw
        #  the cursor on it
        w = 0
        cursor_pos = None
        for i, letter in enumerate(letters):
            if i == cursor and self.has_focus():
                cursor_pos = draw_cursor(w, h)
            self.__surface.blit(letter, (w, 0))
            w += letter.get_width()
        if cursor == len(letters) and self.has_focus():
            cursor_pos = draw_cursor(w, h)

        #  adjust the xshift so that cursor remains visible
        if cursor_pos is None:
            self.__xshift = 0
        elif cursor_pos < self.__xshift:
            self.__xshift = cursor_pos
        elif cursor_pos > self.__xshift + self.__max_text_width():
            self.__xshift = cursor_pos - self.__max_text_width() + 1

        self.update_manager()

    def _compute_inner_size(self):
        return 200, self.__text_height

    def _draw(self, surface):
        self.__redraw()
        sh = self.__surface.get_height()
        if self.__prompt_surface is None:
            x = 0
        else:
            surface.blit(self.__prompt_surface, self.inner_pos)
            x = self.__prompt_surface.get_width()
        y = int(
            (self.size[1] - self.__text_height - self._inner_diff()[1]) / 2)
        surface.blit(
            self.__surface, Coord.sum(self.inner_pos, (x, y)),
            area=(self.__xshift, 0, self.__max_text_width(), sh))
