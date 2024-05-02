#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

Author  : nhattdm
GitHub  : https://github.com/nhattdm/


MIT License

Copyright (c) 2024 Tran Doan Minh Nhat (nhattdm)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
from typing import Iterable, List

from simple_term_menu import TerminalMenu


class Selection:

    def __init__(self, prompt_count: int) -> None:
        self.prompt_count: int = prompt_count

    def full_interactive_actions(self) -> int:
        actions: List[str] = [
            '[1] Starts a conversation' if self.prompt_count == 0 else '[1] Continues the conversation',
            '[2] Copies the last message to your clipboard',
            '[3] Copies a code block from the last message to your clipboard',
            '[4] Starts a new conversation',
            '[5] Saves the current conversation',
            '[6] Loads a saved conversation',
            '[7] Deletes a saved conversation',
            '[8] Quits the program'
        ]

        action_menu: TerminalMenu = TerminalMenu(
            menu_entries=actions,
            title='Interactive actions:',
            shortcut_key_highlight_style=('fg_cyan', 'bold',)
        )

        action_index: int = action_menu.show()
        return action_index + 1

    def partial_interactive_actions(self) -> int:
        actions: List[str] = [
            '[1] Starts a conversation' if self.prompt_count == 0 else '[1] Continues the conversation',
            '[2] Copies the last message to your clipboard',
            '[3] Shows more actions',
            '[4] Quits the program'
        ]

        action_menu: TerminalMenu = terminal_menu(
            menu_title='Interactive actions:',
            entries=actions
        )

        action_index: int = action_menu.show()
        return action_index + 1


def terminal_menu(menu_title: str, entries: Iterable[str]) -> TerminalMenu:
    _terminal_menu: TerminalMenu = TerminalMenu(
        title=menu_title,
        menu_entries=entries,
        shortcut_key_highlight_style=('fg_cyan', 'bold',)
    )

    return _terminal_menu


def confirmation_action(menu_title: str) -> bool:
    options: List[str] = ['Yes', 'No']

    option_menu: TerminalMenu = terminal_menu(
        menu_title=menu_title,
        entries=options
    )
    option_index: int = option_menu.show()

    match options[option_index]:
        case 'Yes':
            return True
        case _:
            return False
