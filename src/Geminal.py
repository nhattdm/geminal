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
import time

from components.Action import Action
from components.Banner import print_banner
from components.Config import MODEL_NAME, SAVE_DIRECTORY
from components.Console import print, print_error
from components.Gemini import chat
from components.Loading import Loading

from rich.panel import Panel
from rich.console import Console
from rich.markdown import Markdown

from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding import KeyBindings

kb = KeyBindings()


@kb.add('c-i')
def _(event):
    event.current_buffer.insert_text('\n')


@kb.add('enter')
def _(event):
    event.current_buffer.validate_and_handle()


prompt_count: int = 0
console: Console = Console()


def get_prompt() -> str:
    placeholder: HTML = HTML('<i><ansigray>Enter a prompt here</ansigray></i>')
    prefix_prompt: HTML = HTML(f'<b><ansibrightblue>$</ansibrightblue></b> ')

    try:
        user_prompt: str = f"""{
            prompt(
                message=prefix_prompt, 
                placeholder=placeholder, 
                key_bindings=kb, 
                multiline=True
            ).strip()
        }"""
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        print_error(message=f'An error occurred while getting the prompt: {e}')
        return

    return user_prompt


def __to_plain_text(rich_text: str) -> str:
    words: list[str] = re.findall(pattern=r'[a-zA-Z0-9]+', string=rich_text)
    plain_text: str = ' '.join([word.capitalize() for word in words])
    return plain_text


def send_prompt(user_prompt: str) -> None:
    global prompt_count

    console.print()
    if user_prompt.strip() == '':
        print_error(message='The user prompt is empty!')

    title: str = f'[bold bright_blue]✨ {__to_plain_text(rich_text=MODEL_NAME)} ✨'
    Loading.start(message=f'{title} is thinking...')

    start_time: float = time.time()
    try:
        response = chat.send_message(user_prompt)
        prompt_count += 1
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        Loading.stop()
        print_error(message=f'Google API request failed to connect: {e}')
        return

    end_time: float = time.time()
    subtitle: str = f'[bold bright_yellow]Time Elapsed: {(end_time - start_time):.1f}s[/][bright_blue] | [/][bold bright_red]Prompt Count: {prompt_count}[/]'
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
    print(any=panel)


def main():
    global prompt_count
    action: Action = Action(prompt_count=prompt_count)

    user_prompt: str | None = ' '.join(sys.argv[1:]) if sys.argv[1:] else None

    if not os.path.exists(path=SAVE_DIRECTORY):
        os.makedirs(name=SAVE_DIRECTORY)

    print_banner()

    if user_prompt is not None:
        send_prompt(user_prompt=user_prompt)

    while True:
        # interactive actions are not available if the application runs in a docker container.
        if not os.path.exists('/.dockerenv'):
            action.interact_w_partial_action_menu()
            
        prompt: str = get_prompt()
        if prompt is not None:
            send_prompt(user_prompt=prompt)
            action: Action = Action(prompt_count=prompt_count)


if __name__ == '__main__':
    main()
