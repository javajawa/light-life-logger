#!/usr/bin/env python3
# vim: ts=4 expandtab

from __future__ import annotations

import enum
import typing

from catz import CatZ, Chart, Page, registerfield, registerchart, registerpage
from catz.ui import Window


@enum.unique
class DayType(enum.Enum):
    Work = 'w'
    Rest = 's'
    Holiday = 'h'
    Illness = 'i'
    Social = 'v'
    Other = 'o'


@registerpage(order=10)
@registerfield('overall', int, -1)
@registerfield('energy', int, -1)
@registerfield('productivity', int, -1)
@registerfield('type', DayType, DayType.Other)
@registerfield('moodlets', typing.List[str], list)
class Activities(Page):
    @classmethod
    def title(cls: typing.Type[Page]) -> str:
        return 'Mood'

    @classmethod
    def query(cls: typing.Type[Page], win: Window, data: CatZ):
        data.overall = win.scale('How Are?', data.overall)
        data.energy = win.scale('Energy?', data.energy)
        data.productivity = win.scale('Productivity?', data.productivity)

        data.type = win.single_select(DayType, data.type)

        data.moodlets = win.text_list('Moodlets', data.moodlets)


@registerchart
class MoodChart(Chart):
    @classmethod
    def filename(cls: typing.Type[Chart]) -> str:
        return 'mood.svg'

    @classmethod
    def title(cls: typing.Type[Chart]) -> str:
        return 'Mood'

    @classmethod
    def min(cls: typing.Type[Chart]) -> int:
        return 2

    @classmethod
    def max(cls: typing.Type[Chart]) -> int:
        return 20

    @classmethod
    def colour(cls: typing.Type[Chart], value: int) -> str:
        if value == -1:
            return 'grey'

        return 'hsl(%d, 50%%, 50%%)' % (value * 6)

    @classmethod
    def note(cls: typing.Type[Chart], data: typing.Optional[CatZ]) -> str:
        if not data:
            return ''

        score = cls.value(data)

        return '%d (o: %d, e: %d, p: %d)' % (score, data.overall, data.energy, data.productivity)

    @classmethod
    def value(cls: typing.Type[Chart], data: typing.Optional[CatZ]) -> int:
        if not data:
            return -1

        return 4 * data.overall + data.energy + data.productivity - 4
