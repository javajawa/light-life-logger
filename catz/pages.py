#!/usr/bin/env python3
# vim: ts=4 expandtab

from __future__ import annotations

from abc import ABC, abstractmethod
from operator import itemgetter
from typing import List, Tuple, Type


def page_list() -> List[Type[Page]]:
    _PAGES.sort(key=itemgetter(1))

    return [t for (t, o) in _PAGES]


class Page(ABC):
    @classmethod
    @abstractmethod
    def title(cls: Type[Page]) -> str:
        pass


    @classmethod
    @abstractmethod
    def query(cls: Type[Page], win: 'catz.ui.Window', data: 'catz.CatZ'):
        pass


_PAGES: List[Tuple[Type[Page], int]] = []


def registerpage(order: int):
    def wrap(to_register: Type[Page]) -> Type[Page]:
        if not issubclass(to_register, Page):
            raise ValueError("Type is not a Page")

        _PAGES.append((to_register, order))

        return to_register

    return wrap
