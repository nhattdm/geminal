"""
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

import os
import re
import sys
import json
import pyperclip

from components.Config import SAVE_DIRECTORY, MODEL_NAME
from components.Console import print, print_error, print_info
from components.Gemini import get_last_response, get_chat_history
from components.Selection import Selection

from pygments import lexers, formatters, highlight
from simple_term_menu import TerminalMenu

from rich.panel import Panel
from rich.console import Console
from rich.markdown import Markdown

from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML

is_loaded: bool = False

class Action:

    def __init__(self, prompt_count: int) -> None:
        self.prompt_count: int = prompt_count
        self.selection: Selection = Selection(prompt_count=self.prompt_count)

    def interact_w_partial_action_menu(self) -> None:
        try:
            user_selection: int = self.selection.partial_interactive_actions()
        except KeyboardInterrupt:
            sys.exit()
        except Exception:
            sys.exit()

        match user_selection:
            case 1:
                return
            case 2:
                self.__copy_last_message()
                self.interact_w_partial_action_menu()
            case 3:
                self.interact_w_full_action_menu()
            case 4:
                self.__quit_program()
            case _:
                return

    def interact_w_full_action_menu(self) -> None:
        try:
            user_selection: int = self.selection.full_interactive_actions()
        except KeyboardInterrupt:
            sys.exit()
        except Exception:
            sys.exit()

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
                self.__start_new_conversation()
            case 5:
                self.__save_conversation(get_chat_history())
                self.interact_w_partial_action_menu()
            case 6:
                self.__load_conversation()
                self.interact_w_partial_action_menu()
            case 7:
                self.__delete_conversation()
                self.interact_w_partial_action_menu()
            case 8:
                self.__quit_program()
            case _:
                return

    def __copy_last_message(self) -> None:
        print(
            any='[*] You selected the action to copy the last message to your clipboard.'
        )

        if self.prompt_count == 0:
            print_error(message='There are no messages to copy.')
            return

        last_response: str = get_last_response()
        pyperclip.copy(last_response)
        print_info(message='Copied the last message to your clipboard.')
        return

    def __copy_code_block_from_last_message(self) -> None:
        print(
            any='[*] You selected the action to copy a code block from the last message to your clipboard.'
        )

        if self.prompt_count == 0:
            print_error(message='There are no messages to copy.')
            return

        last_response: str = get_last_response()
        markdown_code_blocks: list[str] = re.findall(
            pattern=r'```(\w*)\n(.*?)```', string=last_response, flags=re.DOTALL
        )

        match len(markdown_code_blocks):
            case 0:
                print_error(
                    message='There are no code blocks from the last message to copy.'
                )
                return

            case 1:
                pyperclip.copy(markdown_code_blocks[0][1])
                print_info(
                    message='Copied the selected code block to your clipboard.')
                return

            case _:
                language_list = []
                code_block_dict = {}

                def get_code_blocks_from_last_message() -> list[str]:
                    nonlocal language_list
                    nonlocal code_block_dict
                    nonlocal markdown_code_blocks

                    language_list = []
                    code_block_dict = {}

                    for i, (language, code) in enumerate(iterable=markdown_code_blocks, start=1):
                        language_w_index: str = f"[{i}] {language if len(language) != 0 else '_'}"
                        code_block_dict[
                            language if len(language) != 0 else '_'
                        ] = code
                        language_list.append(language_w_index)

                    return (lang for lang in language_list)

                def highlight_code_block(language_w_index: str):
                    lexer_name: str = language_w_index.split()[-1].strip()
                    code_block: str = code_block_dict[lexer_name]

                    try:
                        lexer = lexers.get_lexer_by_name(
                            _alias=lexer_name,
                            stripnl=False,
                            stripall=False
                        )
                    except Exception:
                        lexer = lexers.get_lexer_by_name(
                            _alias='text',
                            stripnl=False,
                            stripall=False
                        )

                    formatter = formatters.TerminalFormatter(
                        bg='dark'
                    )  # dark or light

                    highlighted_code_block = highlight(
                        code=code_block,
                        lexer=lexer,
                        formatter=formatter
                    )

                    return highlighted_code_block

                code_block_menu: TerminalMenu = TerminalMenu(
                    menu_entries=get_code_blocks_from_last_message(),
                    title='Available code blocks:',
                    preview_command=highlight_code_block,
                    preview_size=0.5
                )

                code_block_index: int = code_block_menu.show()
                selected_code_block: str = code_block_dict[
                    language_list[code_block_index].split()[-1]
                ]
                pyperclip.copy(selected_code_block)
                print_info(
                    message='Copied the selected code block to your clipboard.')
                return

    def __start_new_conversation(self) -> None:
        os.system(command='clear')
        os.execl(sys.executable, sys.executable, *sys.argv)

    def __save_conversation(self, chat_history: str) -> None:
        print('[*] You selected the action to save the current conversation.')

        if self.prompt_count == 0:
            print_error('The conversation is empty. There is nothing to save.')
            return
        else:
            placeholder: HTML = HTML(
                '<i><ansigray>Enter a name for this conversation</ansigray></i>'
            )
            prefix_prompt: HTML = HTML(
                '<b><ansibrightblue>[*] Name this conversation:</ansibrightblue></b> '
            )
            
            try:
                file_name_input: str = f"""{prompt(message=prefix_prompt, placeholder=placeholder).strip()}"""
            except KeyboardInterrupt:
                sys.exit()
            except Exception as e:
                print_error(message=f'An error occurred while naming the conversation: {e}')
                return

            def to_underscored_text(plain_text: str) -> str:
                words: list[str] = re.findall(
                    pattern=r'[a-zA-Z0-9]+', string=plain_text)
                underscored_text: str = '_'.join([word for word in words])
                return underscored_text

            def chat_history_to_json(chat_history: str) -> str:
                chat_history = chat_history.replace('text:', '"text":')
                chat_history = chat_history.replace('\n, parts ', '\n},\n')
                chat_history = chat_history.replace('\n}\nrole', ',\n  "role"')
                chat_history = chat_history.replace(
                    '"role": "model"\n]',
                    '"role": "model"\n}]'
                )
                chat_history = chat_history.replace('[parts {', '[{')
                chat_history = chat_history.replace('\\n', '\\\\n')
                chat_history = chat_history.replace("\\'", "'")
                return chat_history

            file_name: str = to_underscored_text(plain_text=file_name_input)
            file_path: str = os.path.join(SAVE_DIRECTORY, f'{file_name}.json')
            file_content = json.loads(
                s=chat_history_to_json(chat_history=chat_history)
            )

            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(obj=file_content, fp=file, indent=2)
            
            Console().print()
            print_info(message=f'Saved file as \[{file_path}].')
            return

    def __load_conversation(self) -> None:
        global is_loaded

        print('[*] You selected the action to load a saved conversation.')

        if self.prompt_count != 0 or not is_loaded == False:
            print_error(
                message='This action only works when the conversation is empty.'
            )
            return

        is_loaded = True

        file_names: list[str] = sorted(os.listdir(path=SAVE_DIRECTORY))
        if len(file_names) == 0:
            print_error(message='No saved conversations found.')
            return

        file_name_menu: TerminalMenu = TerminalMenu(
            menu_entries=file_names,
            title='[*] Available saved conversation files:'
        )
        file_name_index: int = file_name_menu.show()
        selected_file_name: str = f'{file_names[file_name_index]}'
        selected_file_path: str = os.path.join(
            SAVE_DIRECTORY, selected_file_name
        )

        try:
            with open(file=selected_file_path, mode='r', encoding='utf-8') as file:
                file_content: str = json.load(fp=file)
        except Exception as e:
            print_error(
                message=f'Unable to open the selected conversation file: \[{selected_file_name}].'
            )
            return

        for message in file_content:
            role = message['role']
            if role == 'user':
                print(
                    any=f'[bold][bright_blue]$[/] {message["text"]}'
                )
            elif role == 'model':
                def to_plain_text(rich_text: str) -> str:
                    words: list[str] = re.findall(
                        pattern=r'[a-zA-Z0-9]+',
                        string=rich_text
                    )
                    plain_text: str = ' '.join(
                        [word.capitalize() for word in words]
                    )
                    return plain_text

                text = message["text"].replace("'", "\\'").replace('\\n', '\n')
                panel: Panel = Panel(
                    Markdown(
                        markup=text,
                        code_theme='monokai'
                    ),
                    border_style='bright_blue',
                    title=f'[bold bright_blue]✨ {to_plain_text(rich_text=MODEL_NAME)} ✨',
                    title_align='left',
                    subtitle=None,
                    subtitle_align='right'
                )
                print(any=panel)
            else:
                pass

    def __delete_conversation(self) -> None:
        print(any='[*] You selected the action to delete a saved conversation.')

        file_names: list[str] = os.listdir(path=SAVE_DIRECTORY)
        file_name_menu: TerminalMenu = TerminalMenu(
            menu_entries=file_names,
            title='[*] Available saved conversations files:'
        )
        file_name_index: str = file_name_menu.show()
        selected_file_name: str = f'{file_names[file_name_index]}'
        selected_file_path: str = os.path.join(
            SAVE_DIRECTORY,
            selected_file_name
        )

        user_confirmation: bool = self.selection.confirmation_action(
            menu_title=f"Are you sure to delete this file '{selected_file_name}'?"
        )

        if user_confirmation:
            try:
                os.unlink(path=selected_file_path)
                print_info(message=f'Deleted file as \[{selected_file_path}].')
                return
            except Exception as e:
                print_error(
                    message=f'Unable to delete file as \[{selected_file_path}] because it is being used by another program: {e}'
                )
                return
        else:
            print_info(message='Do nothing.')
            return

    def __quit_program(self) -> None:
        sys.exit()
