#!/usr/bin/env python3

'''definition of class event'''

from . import EnumType


class Event(metaclass=EnumType):  # pylint: disable=R0903
    '''enumerate all possible event types'''

    #  the node has been activated
    ON_ACTIVATE = 'on-activate'

    #  the value of the node has changed
    ON_CHANGE = 'on-change'

    #  the mouse left button is being pressed while the cursor is on
    #  the node
    ON_CLICK = 'on-click'

    #  left-click down on the node
    ON_CLICKDOWN = 'on-click-down'

    #  right-click down on the node
    ON_CLICKDOWNRIGHT = 'on-click-down-right'

    #  left-click up on the node
    ON_CLICKUP = 'on-click-up'

    #  right-click up on the node
    ON_CLICKUPRIGHT = 'on-click-up-right'

    #  the node has been disabled
    ON_DISABLE = 'on-disable'

    #  the node has been enabled
    ON_ENABLE = 'on-enable'

    #  the node received the focus
    ON_FOCUS = 'on-focus'

    #  a key has been pressed while the node has the focus
    ON_KEY = 'on-key'

    #  the mouse wheel has been used over the node
    ON_MOUSEWHEEL = 'on-mouse-wheel'

    #  the cursor just moved over the node
    ON_OVER = 'on-over'

    #  the cursor was previously on the node and is still over it
    ON_OVERAGAIN = 'on-over-again'

    #  the node is a menu item that has been selected
    ON_SELECT = 'on-select'

    #  the mouse left button is being released while the cursor is on
    #  the node or the left mouse button is still pressed but the
    #  cursor is not over the node anymore
    ON_UNCLICK = 'on-unclick'

    #  the node has lost the focus
    ON_UNFOCUS = 'on-unfocus'

    #  the cursor is not over the node anymore
    ON_UNOVER = 'on-unover'

    #  the node is a menu item that has been unselected
    ON_UNSELECT = 'on-unselect'
