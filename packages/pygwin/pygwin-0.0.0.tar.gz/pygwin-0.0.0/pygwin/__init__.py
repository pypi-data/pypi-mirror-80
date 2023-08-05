#!/usr/bin/env python3

# disable cyclic-import checking
# pylint: disable=R0401

'''
.. module:: pygwin

import all pygwin classes here'''

import inspect
import pygame as pg

from .colors import Colors
from .coord import Coord
from .enum_type import EnumType
from .draw import Draw
from .event import Event
from .util import Util
from .animation import Animation
from .static_dict import StaticDict
from .style import Style
from .media import Media
from .keys import Keys
from .context import Context
from .context_style import ContextStyle
from .cursor import Cursor
from .style_class import StyleClass
from .node_type import NodeType
from .node import Node
from .empty import Empty
from .valued_node import ValuedNode
from .event_manager import EventManager
from .label import Label
from .box import Box
from .button import Button
from .table import Table
from .rule import Rule
from .image import Image
from .checkbox import Checkbox
from .radiobox import Radiobox
from .radiobox_group import RadioboxGroup
from .frame import Frame
from .input_text import InputText
from .menu import Menu
from .gauge import Gauge
from .select import Select
from .item_select import ItemSelect
from .int_select import IntSelect
from .text_board import TextBoard
from .window import Window
from .panel import Panel
from .window_system import WindowSystem
from .default_style import DefaultStyle

VERSION = '0.0.0'

#  default key bindings:
#    * escape => close window
#    * tab => move focus forward
#    * lshift + tab => move focus backward
#    * enter => activate element with focus
Keys.bind(pg.K_ESCAPE, Keys.ACT_CLOSE_WINDOW)
Keys.bind(pg.K_TAB, Keys.ACT_MOVE_FOCUS_FORWARD)
Keys.bind(pg.K_TAB, Keys.ACT_MOVE_FOCUS_BACKWARD, pressed=[pg.K_LSHIFT])
Keys.bind(pg.K_RETURN, Keys.ACT_ACTIVATE_FOCUS)
