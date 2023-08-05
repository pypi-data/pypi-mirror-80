#!/usr/bin/env python3

'''@TODO@'''

from . import Event, EnumType


class Context(metaclass=EnumType):  # pylint: disable=R0903
    '''@TODO@'''

    #  the node is activated
    ACTIVATED = 'activated'

    #  base context
    BASE = 'base'

    #  the node is being left-clicked (i.e., the cursor is over it and
    #  the user has the left mouse button pressed)
    CLICKED = 'clicked'

    #  the node is disabled
    DISABLED = 'disabled'

    #  the node has the focus
    FOCUS = 'focus'

    #  a key is being pressed while the node has the focus
    KEYED = 'keyed'

    #  the cursor is over the node
    OVERED = 'overed'

    #  the node is being selected
    SELECTED = 'selected'

    #  order in which we check the different contexts of a node
    PRIORITY = [
        DISABLED,
        SELECTED,
        ACTIVATED,
        KEYED,
        CLICKED,
        FOCUS,
        OVERED,
        BASE
    ]

    #  for each context ctx, EVTS_ON[ctx] lists the events that may
    #  turn this context on and EVTS_OFF[ctx] are the events that may
    #  turn this context off
    EVTS_ON = {
        ACTIVATED: [Event.ON_ACTIVATE],
        BASE: [],
        CLICKED: [Event.ON_CLICKDOWN, Event.ON_OVER],
        DISABLED: [Event.ON_DISABLE],
        FOCUS: [Event.ON_FOCUS],
        KEYED: [Event.ON_KEY],
        OVERED: [Event.ON_OVER],
        SELECTED: [Event.ON_SELECT]
    }
    EVTS_OFF = {
        ACTIVATED: [],
        BASE: [],
        CLICKED: [Event.ON_CLICKUP, Event.ON_UNOVER],
        DISABLED: [Event.ON_ENABLE],
        FOCUS: [Event.ON_UNFOCUS],
        KEYED: [],
        OVERED: [Event.ON_UNOVER],
        SELECTED: [Event.ON_UNSELECT]
    }

    @classmethod
    def check(cls, node, ctx):
        '''check whether context ctx applies to node'''
        return {
            Context.ACTIVATED: lambda: True,  #  not yet implemented
            Context.BASE: lambda: True,
            Context.CLICKED: lambda: node.is_clicked() and node.is_overed(),
            Context.DISABLED: node.is_disabled,
            Context.FOCUS: node.has_focus,
            Context.KEYED: lambda: True,  #  not yet implemented,
            Context.OVERED: node.is_overed,
            Context.SELECTED: node.is_selected
        }[ctx]()
