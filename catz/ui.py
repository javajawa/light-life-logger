#!/usr/bin/env python3
# vim: ts=4 expandtab

from __future__ import annotations

import curses
import enum

from typing import Any, Dict, List, Set, Type


_WIDTH: int = 76
_HEIGHT: int = 36

class Window:
    stdscr: Any = ...
    win: Any = ...

    def __init__(self: Window):
        pass

    def __enter__(self: Window) -> Window:
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.cbreak()

        self.win = curses.newwin(_HEIGHT + 1, _WIDTH + 1, 0, 0)
        self.win.keypad(True)

        return self


    def __exit__(self: Window, _type, value, traceback):
        curses.nocbreak()
        curses.echo()
        curses.endwin()


    def reset(self: Window, stage: str):
        self.win.erase()
        self.win.move(0, 0)
        self.win.addstr('CatZ - ')
        self.win.addstr(stage)
        self.win.move(2, 0)
        self.win.noutrefresh()
        self.win.leaveok(True)
        curses.noecho()


    def clear(self: Window):
        self.win.move(2, 0)
        self.win.clrtobot()


    def scale(self: Window, prompt: str, value: int) -> int:
        self.win.addstr(prompt)

        if value != -1:
            self.win.addstr(' (was %d)' % value)

        self.win.addstr(' [1-4] ')
        self.win.refresh()

        while True:
            char = self.win.getch()

            if value != -1:
                if char in [curses.KEY_ENTER, 10, 13]:
                    char = str(value)
                    break

            if char > 255:
                continue

            char = chr(char)

            if '1' <= char <= '4':
                break

        self.win.addstr(char)
        self.win.addstr('\n')

        return int(char)


    def text_list(self: Window, prompt: str, values: List[str]) -> List[str]:
        # TODO: Print out existing values and check if to keep.
        self.clear()
        self.win.addstr(prompt)
        self.win.addstr('\n> ')
        curses.echo()
        self.win.refresh()

        while True:
            keyword = self.win.getstr()

            if not keyword:
                break

            values.append(keyword.decode('utf-8'))
            self.win.addstr('> ')
            self.win.refresh()

        return values


    def single_select(self: Window, options: Type[enum.Enum], value: enum.Enum):
        length: int = 4 + max(*[len(opt.name) for opt in options])
        cols: int = int(_WIDTH / length)

        self.clear()

        while True:
            self.single_select_render(options, value, cols)

            choice = chr(self.win.getch())

            if choice in ['\n', '\r', 'q', value.value]:
                return value

            try:
                value = options(choice)
            except ValueError:
                pass


    def multi_select(self: Window, options: Type[enum.Enum], values: Set):
        length: int = 4 + max(*[len(opt.name) for opt in options])
        cols: int = int(_WIDTH / length)

        self.clear()

        while True:
            self.multi_select_render(options, values, cols)

            choice = chr(self.win.getch())

            if choice in ['\n', '\r', 'q']:
                return

            try:
                option = options(choice)

                if option in values:
                    values.remove(option)
                else:
                    values.add(option)
            except ValueError:
                pass


    def multi_count(self: Window, options: Type[enum.Enum], values: Dict[Any, int]):
        current_row: int = 0
        max_row: int = len(options)
        rows: List[str] = []
        items: List[enum.Enum] = []

        for option in options:
            if option not in values:
                values[option] = 0

            rows.append(option.value)
            items.append(option)

        self.clear()

        while True:
            item: enum.Enum = items[current_row]

            self.multi_count_render(options, values, item)

            choice = self.win.getch()

            if choice == curses.KEY_RIGHT:
                values[item] += 1

            elif choice == curses.KEY_LEFT:
                values[item] -= 1

            elif choice == curses.KEY_UP:
                if current_row > 0:
                    current_row -= 1

            elif choice == curses.KEY_DOWN:
                if current_row < max_row:
                    current_row += 1

            else:
                choice = chr(choice)

                if choice in ['\n', '\r', 'q']:
                    return

                if choice in rows:
                    current_row = rows.index(choice)


    def single_select_render(self: Window, options: Type[enum.Enum], value: enum.Enum, cols: int):
        width: int = int(_WIDTH / cols)
        position: int = 2 * cols

        for act in options:
            self.win.addstr(
                int(position / cols), width * (position % cols),
                "%s %s" % (act.value, act.name),
                curses.A_BOLD if act == value else curses.A_DIM
            )

            position += 1


    def multi_select_render(self: Window, options: Type[enum.Enum], values: Set, cols: int):
        width: int = int(_WIDTH / cols)
        position: int = 2 * cols

        for act in options:
            self.win.addstr(
                int(position / cols), width * (position % cols),
                "%s %s" % (act.value, act.name),
                curses.A_BOLD if act in values else curses.A_DIM
            )

            position += 1


    def multi_count_render(self: Window, options: Type[enum.Enum], values: Dict, selected):
        position: int = 2

        for act in options:
            self.win.addstr(
                position, 0, "%s %-20s %d" % (act.value, act.name, values[act]),
                curses.A_BOLD if act == selected else curses.A_DIM
            )

            position += 1
