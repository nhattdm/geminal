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
import json
import os
import re
from typing import Any, Dict, Generator, List

from prompt_toolkit import HTML, prompt
from prompt_toolkit.clipboard.pyperclip import PyperclipClipboard
from pygments import lexers, formatters, highlight
from pygments.lexer import Lexer
from rich.markdown import Markdown
from rich.panel import Panel
from simple_term_menu import TerminalMenu

from .config import conf
from .console import log, log_error, log_info, new_line
from .gemini import get_last_response, get_chat_history, display_name
from .selection import Selection, confirmation_action
from .utils import quit_program, restart_program, to_separated_text_w_char

is_loaded: bool = False
save_dir: str = conf['settings']['save_dir']
clipboard: PyperclipClipboard = PyperclipClipboard()


class Action:

    def __init__(self, prompt_count: int) -> None:
        self.prompt_count: int = prompt_count
        self.selection: Selection = Selection(
            prompt_count=self.prompt_count
        )

    def interact_w_partial_action_menu(self) -> None:
        user_selection: int = 0

        try:
            user_selection = self.selection.partial_interactive_actions()
        except (KeyboardInterrupt, Exception,):
            quit_program()

        match user_selection:
            case 1:
                return
            case 2:
                self.__copy_last_message()
                self.interact_w_partial_action_menu()
            case 3:
                self.interact_w_full_action_menu()
            case 4:
                quit_program()
            case _:
                return

    def interact_w_full_action_menu(self) -> None:
        user_selection: int = 0

        try:
            user_selection: int = self.selection.full_interactive_actions()
        except (KeyboardInterrupt, Exception,):
            quit_program()

        match user_selection:
            case 1:
                return
            case 2:
                self.__copy_last_message()
                self.interact_w_partial_action_menu()
            case 3:
                self.__copy_code_block_from_last_message()
                self.interact_w_partial_action_menu()
            case 4:
                restart_program()
            case 5:
                self.__save_conversation(get_chat_history())
                self.interact_w_partial_action_menu()
            case 6:
                self.__load_conversation()
                self.interact_w_partial_action_menu()
            case 7:
                delete_conversation()
                self.interact_w_partial_action_menu()
            case 8:
                quit_program()
            case _:
                return

    def __copy_last_message(self) -> None:
        log(anything='[*] You selected the action to copy the last message to your clipboard.')

        if self.prompt_count == 0:
            log_error(message='There are no messages to copy.')
            return

        clipboard.set_text(text=get_last_response())
        log_info(message='Copied the last message to your clipboard.')
        return

    def __copy_code_block_from_last_message(self) -> None:
        log(anything='[*] You selected the action to copy a code block from the last message to your clipboard.')

        if self.prompt_count == 0:
            log_error(message='There are no messages to copy.')
            return

        markdown_code_blocks: List[str] = re.findall(
            pattern=r'```(\w*)\n(.*?)```',
            string=get_last_response(),
            flags=re.DOTALL
        )

        match len(markdown_code_blocks):
            case 0:
                log_error(message='There are no code blocks from the last message to copy.')
                return

            case 1:
                clipboard.set_text(text=markdown_code_blocks[0][1])
                log_info(message='Copied the selected code block to your clipboard.')
                return

            case _:
                languages: List[str] = []
                code_block_dict: Dict = {}

                def get_code_blocks_from_last_message() -> Generator[str, Any, None]:
                    nonlocal languages
                    nonlocal code_block_dict
                    nonlocal markdown_code_blocks

                    languages = []
                    code_block_dict = {}

                    for i, (language, code) in enumerate(iterable=markdown_code_blocks, start=1):
                        language_w_index: str = f"[{i}] {language if len(language) != 0 else '_'}"
                        code_block_dict[
                            language if len(language) != 0 else '_'
                        ] = code
                        languages.append(language_w_index)

                    return (lang for lang in languages)

                def highlight_code_block(language_w_index: str) -> str:
                    lexer_name: str = language_w_index.split()[-1].strip()
                    code_block: str = code_block_dict[lexer_name]

                    try:
                        lexer: Lexer = lexers.get_lexer_by_name(
                            _alias=lexer_name,
                            stripnl=False,
                            stripall=False
                        )
                    except (Exception,):
                        lexer = lexers.get_lexer_by_name(
                            _alias='text',
                            stripnl=False,
                            stripall=False
                        )

                    formatter = formatters.TerminalFormatter(
                        bg='dark'
                    )  # dark or light

                    highlighted_code_block: str = highlight(
                        code=code_block,
                        lexer=lexer,
                        formatter=formatter
                    )

                    return highlighted_code_block

                code_block_menu: TerminalMenu = TerminalMenu(
                    menu_entries=get_code_blocks_from_last_message(),
                    title='[*] Available code blocks:',
                    preview_command=highlight_code_block,
                    preview_size=0.5,
                    shortcut_key_highlight_style=('fg_cyan', 'bold',)
                )
                code_block_index: int = code_block_menu.show()

                selected_code_block: str = ''

                try:
                    selected_code_block = code_block_dict[
                        languages[code_block_index].split()[-1]
                    ]
                except (KeyboardInterrupt, Exception,):
                    quit_program()

                clipboard.set_text(text=selected_code_block)
                log_info(message='Copied the selected code block to your clipboard.')
                return

    def __save_conversation(self, chat_history: str) -> None:
        log(anything='[*] You selected the action to save the current conversation.')

        if self.prompt_count == 0:
            log_error(message='The conversation is empty. There is nothing to save.')
            return
        else:
            placeholder: HTML = HTML('<i><ansigray>Enter a name for this conversation</ansigray></i>')
            prefix_prompt: HTML = HTML('<b><ansibrightblue>[*] Name this conversation:</ansibrightblue></b> ')

            file_name_to_save: str = ''

            try:
                file_name_to_save = f"""{prompt(message=prefix_prompt, placeholder=placeholder).strip()}"""
            except KeyboardInterrupt:
                quit_program()
            except Exception as e:
                log_error(message=f"An error occurred while naming the conversation: {repr(e)}")
                return

            def chat_log_to_json(chat_log: str) -> str:
                chat_log = chat_log.replace('text:', '"text":')
                chat_log = chat_log.replace('\n, parts ', '\n},\n')
                chat_log = chat_log.replace('\n}\nrole', ',\n  "role"')
                chat_log = chat_log.replace(
                    '"role": "model"\n]',
                    '"role": "model"\n}]'
                )
                chat_log = chat_log.replace('[parts {', '[{')
                chat_log = chat_log.replace('\\n', '\\\\n')
                chat_log = chat_log.replace("\\'", "'")
                return chat_log

            def get_unique_file_path(filename: str) -> str:
                suffix: str = '.json'
                count: int = 0

                unique_file_path: str = os.path.join(save_dir, f"{filename}{suffix}")
                while os.path.exists(unique_file_path):
                    count += 1
                    unique_file_path = os.path.join(save_dir, f"{filename}_{str(count)}{suffix}")

                return unique_file_path

            file_name: str = to_separated_text_w_char(s=file_name_to_save)
            file_path: str = get_unique_file_path(file_name)
            file_content = json.loads(
                s=chat_log_to_json(
                    chat_log=chat_history
                )
            )

            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(obj=file_content, fp=file, indent=2)

            new_line()
            log_info(message=f"Saved file as \[{file_path}].")  # noqa: disable=W605
            return

    def __load_conversation(self) -> None:
        global is_loaded

        log('[*] You selected the action to load a saved conversation.')

        if self.prompt_count != 0 or is_loaded:
            log_error(message=f"This action only works when the conversation is empty.")
            return

        is_loaded = True

        file_names: list[str] = sorted(os.listdir(path=save_dir))
        if len(file_names) == 0:
            log_error(message='No saved conversations found.')
            return

        file_name_menu: TerminalMenu = TerminalMenu(
            menu_entries=file_names,
            title='[*] Available saved conversation files:'
        )
        file_name_index: int = file_name_menu.show()
        selected_file_name: str = ''

        try:
            selected_file_name = f'{file_names[file_name_index]}'
        except (KeyboardInterrupt, Exception,):
            quit_program()

        selected_file_path: str = os.path.join(
            save_dir, selected_file_name
        )

        try:
            with open(file=selected_file_path, mode='r', encoding='utf-8') as file:
                file_content: str = json.load(fp=file)
        except (Exception,):
            log_error(
                message=f'Unable to open the selected conversation file: \[{selected_file_name}].'
            )  # noqa: disable=W605
            return

        for message in file_content:
            role: str = message['role']
            if role == 'user':
                log(anything=f"[bold][bright_blue]$[/] {message['text']}")
            elif role == 'model':
                text = (
                    message['text']
                    .replace("'", "\\'")
                    .replace('\\n', '\n')
                )
                panel: Panel = Panel(
                    Markdown(
                        markup=text,
                        code_theme='monokai'
                    ),
                    border_style='bright_blue',
                    title=f'[bold bright_blue]{display_name}',
                    title_align='left',
                    subtitle=None,
                    subtitle_align='right'
                )
                log(anything=panel)
            else:
                pass


def delete_conversation() -> None:
    log(anything='[*] You selected the action to delete a saved conversation.')

    file_names: List[str] = os.listdir(path=save_dir)
    file_name_menu: TerminalMenu = TerminalMenu(
        menu_entries=file_names,
        title='[*] Available saved conversations files:'
    )
    file_name_index: int = file_name_menu.show()
    selected_file_name: str = ''

    try:
        selected_file_name = f'{file_names[file_name_index]}'
    except (KeyboardInterrupt, Exception,):
        quit_program()

    selected_file_path: str = os.path.join(save_dir, selected_file_name)

    user_confirmation: bool = confirmation_action(
        menu_title=f"Are you sure to delete this file \[{selected_file_name}]?"
    )  # noqa: disable=W605

    if user_confirmation:
        try:
            os.unlink(path=selected_file_path)
            log_info(message=f'Deleted file as \[{selected_file_path}].')  # noqa: disable=W605
            return
        except Exception as e:
            log_error(
                message=f'Unable to delete file as \[{selected_file_path}]: {repr(e)}'
            )  # noqa: disable=W605
            return
    else:
        log_info(message='Do nothing.')
        return
