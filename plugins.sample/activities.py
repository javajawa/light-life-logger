#!/usr/bin/env python3
# vim: ts=4 expandtab

from __future__ import annotations

import enum
import typing

from catz import CatZ, Page, registerfield, registerpage
from catz.ui import Window


@enum.unique
class Activity(enum.Enum):
    Cooked = 'c'
    Breakfast = 'b'
    Lunch = 'l'
    Dinner = 'd'
    Meat = 'm'
    Vegetables = 'h'
    FastFood = 'f'
    Soda = 's'
    Chocolate = 'C'
    Biscuits = 'B'
    Yoga = 'y'
    Exercise = 'e'
    Hike = 'W'
    WentOut = 'o'
    Visitors = 'v'


@registerpage(order=30)
@registerfield('activities', typing.Set[Activity], list)
class Activities(Page):
    @classmethod
    def title(cls: typing.Type[Page]) -> str:
        return 'Activities'

    @classmethod
    def query(cls: typing.Type[Page], win: Window, data: CatZ):
        win.multi_select(Activity, data.activities)
