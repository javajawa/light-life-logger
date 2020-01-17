#!/usr/bin/env python3
# vim: ts=4 expandtab

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Type, List, Optional


class Chart(ABC):
    @classmethod
    @abstractmethod
    def filename(cls: Type[Chart]) -> str:
        pass


    @classmethod
    @abstractmethod
    def title(cls: Type[Chart]) -> str:
        pass


    @classmethod
    @abstractmethod
    def min(cls: Type[Chart]) -> int:
        pass


    @classmethod
    @abstractmethod
    def max(cls: Type[Chart]) -> int:
        pass


    @classmethod
    @abstractmethod
    def note(cls: Type[Chart], data: Optional['catz.CatZ']) -> str:
        pass


    @classmethod
    @abstractmethod
    def value(cls: Type[Chart], data: Optional['catz.CatZ']) -> int:
        pass


    @classmethod
    @abstractmethod
    def colour(cls: Type[Chart], value: int) -> str:
        pass


_CHARTS: List[Type[Chart]] = []


def registerchart(to_register: Type[Chart]) -> Type[Chart]:
    if not issubclass(to_register, Chart):
        raise ValueError("Type is not a Chart")

    _CHARTS.append(to_register)

    return to_register


def chart_list() -> List[Type[Chart]]:
    return _CHARTS
