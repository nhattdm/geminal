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
import os
import sys
import time

from google.generativeai.types import GenerateContentResponse

from components.action import Action
from components.version import print_version
from components.config import conf
from components.console import log, log_error, new_line
from components.gemini import chat, display_name, print_welcome
from components.loading import Loading
from components.usage import print_usage
from components.utils import quit_program

from rich.panel import Panel
from rich.markdown import Markdown

from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding import KeyBindings


kb: KeyBindings = KeyBindings()


@kb.add('c-i')
@kb.add('escape', 'enter')
def _(event):
    event.current_buffer.insert_text('\n')


@kb.add('enter')
def _(event):
    event.current_buffer.validate_and_handle()


prompt_count: int = 0


def get_prompt() -> str | None:
    placeholder: HTML = HTML('<i><ansigray>Enter a prompt here</ansigray></i>')
    prefix_prompt: HTML = HTML(f'<b><ansibrightblue>$</ansibrightblue></b> ')

    user_prompt: str = ''
    try:
        user_prompt = f"""{
        prompt(
            message=prefix_prompt,
            placeholder=placeholder,
            key_bindings=kb,
            multiline=True
        ).strip()
        }"""
    except KeyboardInterrupt:
        quit_program()
    except Exception as e:
        log_error(message=f"An error occurred while getting the prompt: {repr(e)}")
        return

    return user_prompt


def send_prompt(user_prompt: str) -> None:
    global prompt_count

    new_line()
    if user_prompt.strip() == '':
        log_error(message='The user prompt is empty!')

    title: str = f'[bold bright_blue]{display_name}'
    Loading.start(message=f"{title} is thinking...")

    response: GenerateContentResponse | None = None
    start_time: float = time.time()
    try:
        response = chat.send_message(user_prompt)
        prompt_count += 1
    except KeyboardInterrupt:
        quit_program()
    except Exception as e:
        Loading.stop()
        log_error(message=f"Google API request failed to connect: {repr(e)}")
        return

    end_time: float = time.time()
    subtitle: str = (
        f"[bold bright_yellow]Time Elapsed: {(end_time - start_time):.1f}s[/]"
        f"[bright_blue] | [/][bold bright_red]Prompt Count: {prompt_count}[/]"
    )
    panel: Panel = Panel(
        Markdown(
            markup=response.text,
            code_theme='monokai'
        ),
        border_style='bright_blue',
        title=title,
        title_align='left',
        subtitle=subtitle,
        subtitle_align='right'
    )

    Loading.stop()
    log(anything=panel)


def run() -> None:
    global prompt_count
    user_prompt: str | None = ' '.join(sys.argv[1:]) if sys.argv[1:] else None

    save_dir: str = conf['settings']['save_dir']
    if not os.path.exists(path=save_dir):
        os.makedirs(name=save_dir)

    if user_prompt is not None:
        if user_prompt.strip() == '--version' or user_prompt.strip() == '-v':
            print_version()
            return
        elif user_prompt.strip() == '--help' or user_prompt.strip() == '-h':
            print_usage()
            return
        else:
            send_prompt(user_prompt=user_prompt)
    else:
        print_welcome()

    action: Action = Action(prompt_count=prompt_count)

    while True:
        # check if this program is running in the docker container.
        if not os.path.exists('/.dockerenv'):
            action.interact_w_partial_action_menu()

        user_prompt: str = get_prompt()
        if user_prompt is not None:
            send_prompt(user_prompt=user_prompt)
            if user_prompt == 'exit':
                quit_program()
            action: Action = Action(prompt_count=prompt_count)


if __name__ == '__main__':
    run()
