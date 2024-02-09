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
import time
import logging
import pyperclip

from time import sleep
from threading import Thread

import google.generativeai as genai

from rich.panel import Panel
from rich.console import Console
from rich.markdown import Markdown

from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding import KeyBindings

__author__: str = 'nhattdm'
__version__: str = '0.0.1'
__license__: str = 'MIT'

console = Console()

MODEL_NAME: str = 'gemini-pro'
GOOGLE_API_KEY: str = ''


def print_error(message):
    console.print(
        Panel(f'[bold red]ERROR:[/] [red]{message}', border_style='bold red'))
    console.print()


try:
    GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
except Exception as e:
    print_error(
        f'Please set the GOOGLE_API_KEY environment variable before running this program.')
    sys.exit()

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)
chat = model.start_chat(history=[])

kb = KeyBindings()


@kb.add('escape', 'enter')
def _(event):
    event.current_buffer.insert_text('\n')


@kb.add('enter')
def _(event):
    event.current_buffer.validate_and_handle()


def getExc(e): return e.args[1] if len(e.args) > 1 else str(e)


class LoadingIcon:
    sleep_time = 0.1
    is_querying = None

    __spinner = ('⣾ ', '⣽ ', '⣻ ', '⢿ ', '⡿ ', '⣟ ', '⣯ ', '⣷ ')

    @classmethod
    def __action(cls, message: str):
        while cls.is_querying:
            for spin in cls.__spinner:
                Console().print(f' {message} {spin}', end='\r')
                if not cls.is_querying:
                    break
                sleep(cls.sleep_time)

    @classmethod
    def start_spinning(cls, message: str):
        try:
            cls.is_querying = True
            thread = Thread(target=cls.__action, args=(message,))
            thread.start()
            return thread
        except Exception as e:
            cls.is_querying = False
            logging.debug(getExc(e))

    @classmethod
    def stop_spinning(cls):
        if cls.is_querying:
            cls.is_querying = False
            sleep(cls.sleep_time)


cmds = {
    'help': ['h', 'shows the list of acceptable commands.'],
    'new':  ['n', 'removes the conversation history and starts a new one.'],
    'save': ['s', 'saves the current conversation.'],
    'load': ['l', 'loads a saved conversation.'],
    'delete': ['d', 'deletes a saved conversation.'],
    'copy': ['c', 'copies the last message to your clipboard.'],
    'copy_code': ['cc', 'copies a code from the last message to your clipboard.'],
    'quit': ['q', 'quits the program.']
}
cmd_start: str = '/'
prompt_count: int = 0
save_directory: str = os.path.join(
    os.environ['HOME'], 'geminal', 'conversations')


def to_plain_text(rich_text: str) -> str:
    words: list[str] = re.findall(r'[a-zA-Z0-9]+', rich_text)
    plain_text: str = ' '.join([word.capitalize() for word in words])
    return plain_text


def to_underscore_text(plain_text: str) -> str:
    words: list[str] = re.findall(r'[a-zA-Z0-9]+', plain_text)
    underscore_text: str = '_'.join([word for word in words])
    return underscore_text


def banner() -> str:
    banner: str = f"""
%s  ________ %s        %s         %s.__ %s        %s        %s.__    
%s /  _____/ %s  ____  %s  _____  %s|__|%s  ____  %s_____   %s|  |   
%s/   \  ___ %s_/ __ \ %s /     \ %s|  |%s /    \ %s\__  \  %s|  |   
%s\    \_\  \\\%s\  ___/ %s|  Y Y  \\\%s|  |%s|   |  \\\%s / __ \_%s|  |__ 
%s \______  /%s \___  >%s|__|_|  /%s|__|%s|___|  /%s(____  /%s|____/ 
%s        \/ %s     \/ %s      \/ %s    %s     \/ %s     \/ %s
%sA Chatbot on Terminal powered by Google %s.

%sVersion   : %s{__version__}
%sAuthor    : %s{__author__}

""" % ('[bold bright_blue]', '[bold bright_red]', '[bold bright_yellow]', '[bold bright_blue]', '[bold bright_green]', '[bold bright_red]', '[bold bright_yellow]',
        '[bold bright_blue]', '[bold bright_red]', '[bold bright_yellow]', '[bold bright_blue]', '[bold bright_green]', '[bold bright_red]', '[bold bright_yellow]',
        '[bold bright_blue]', '[bold bright_red]', '[bold bright_yellow]', '[bold bright_blue]', '[bold bright_green]', '[bold bright_red]', '[bold bright_yellow]',
        '[bold bright_blue]', '[bold bright_red]', '[bold bright_yellow]', '[bold bright_blue]', '[bold bright_green]', '[bold bright_red]', '[bold bright_yellow]',
        '[bold bright_blue]', '[bold bright_red]', '[bold bright_yellow]', '[bold bright_blue]', '[bold bright_green]', '[bold bright_red]', '[bold bright_yellow]',
        '[bold bright_blue]', '[bold bright_red]', '[bold bright_yellow]', '[bold bright_blue]', '[bold bright_green]', '[bold bright_red]', '[bold bright_yellow]',
        '[bold bright_magenta]', to_plain_text(MODEL_NAME),
        '[bold bright_yellow]', '[bold bright_green]',
        '[bold bright_yellow]', '[bold bright_green]')
    return banner


### Start of command handler functions. ###

def save_conversation() -> None:
    console.print()
    if prompt_count == 0:
        print_error('Unable to save an empty conversation.')
    else:
        placeholder = HTML(
            '<ansigray><italic>Enter a name for this conversation</italic></ansigray>')
        prefix_prompt = HTML(
            f'<bold><ansicyan>[i] </ansicyan><ansimagenta>Name this conversation</ansimagenta><ansiyellow> > </ansiyellow></bold>')
        user_input = f"""{prompt(prefix_prompt, placeholder=placeholder).strip()}"""
        file_name = to_underscore_text(user_input)
        if user_input.startswith(cmd_start):
            cmd = user_input.split(cmd_start)[1].lower().split()[0]
            if cmd in cmds or cmd in [short[0] for short in cmds.values()]:
                if cmd == 'quit' or cmd == 'q':
                    return
        conversation_file_path = os.path.join(
            save_directory, f'{file_name}.json')
        json_str = str(chat.history).replace('text:', '"text":')
        json_str = json_str.replace('\n, parts ', '\n},\n')
        json_str = json_str.replace('\n}\nrole', ',\n  "role"')
        json_str = json_str.replace(
            '"role": "model"\n]', '"role": "model"\n}]')
        json_str = json_str.replace('[parts {', '[{')
        json_str = json_str.replace('\\n', '\\\\n')
        json_str = json_str.replace("\\'", "'")
        conversation_as_json = json.loads(json_str)
        with open(conversation_file_path, 'w', encoding='utf-8') as file:
            json.dump(conversation_as_json, file, indent=2)
        console.print(
            f'[white]Saved file as {conversation_file_path}[/]')
        console.print()


def load_conversation() -> None:
    global prompt_count
    console.print(
        '[cyan][[bold]i] [magenta]Available Saved Conversations:[/]')
    files = {}
    for index, file_name in enumerate(os.listdir(save_directory)):
        file_str = file_name.split('.')[0]
        files[index + 1] = file_str
        console.print(f'[bold yellow]{index + 1}. {file_str}[/]')
    console.print()

    if len(files) == 0:
        print_error('No saved conversations found.')
        return

    while True:
        placeholder = HTML(
            '<ansigray><italic>Enter your number.</italic></ansigray>')
        prefix_prompt = HTML(
            f'<bold><ansicyan>[i] </ansicyan><ansimagenta>Select a file to load</ansimagenta><ansiyellow> > </ansiyellow></bold>')

        try:
            user_input = f"""{prompt(prefix_prompt, placeholder=placeholder).strip()}"""
        except KeyboardInterrupt:
            sys.exit()
        except Exception as e:
            print_error(
                f'An error occurred while getting the file to load: {e}')
            return

        if user_input.isdigit() == True and int(user_input) in files:
            break
        if user_input.startswith(cmd_start):
            cmd = user_input.split(cmd_start)[1].lower().split()[0]
            if cmd in cmds or cmd in [short[0] for short in cmds.values()]:
                if cmd == 'quit' or cmd == 'q':
                    return
                else:
                    print_error(f'{user_input} is not a valid selection.')
        else:
            print_error(f'{user_input} is not a valid selection.')

    selected_file_path = os.path.join(
        save_directory, f'{files[int(user_input)]}.json')
    with open(selected_file_path, 'r', encoding='utf-8') as file:
        conversation = json.load(file)
    prompt_count = 0
    for message in conversation:
        role = message['role']
        if role == 'user':
            console.print(
                f'[bold][red][{prompt_count}][/] [green]Prompt\n[/][yellow]> [/][/]{message["text"]}')
            prompt_count += 1
        elif role == 'model':
            text = message["text"].replace("'", "\\'").replace("\\n", "\n")
            text = text
            chat_panel = Panel(
                Markdown(text, 'monokai'),
                border_style='cyan',
                title=f'[bold cyan]✨ {to_plain_text(MODEL_NAME)} ✨',
                title_align='left',
                subtitle=None,
                subtitle_align='right'
            )
            console.print(chat_panel)
            console.print('\n')
        else:
            pass


def delete_conversation() -> None:
    global prompt_count
    console.print()
    console.print(
        '[cyan][[bold]i] [magenta]Available Saved Conversations:[/]')
    files = {}
    for index, file_name in enumerate(os.listdir(save_directory)):
        file_str = file_name.split('.')[0]
        files[index + 1] = file_str
        console.print(f'[bold yellow]{index + 1}. {file_str}[/]')
    console.print()

    if len(files) == 0:
        print_error('No saved conversations found.')
        return

    while True:
        placeholder = HTML(
            '<ansigray><italic>Enter your number.</italic></ansigray>')
        prefix_prompt = HTML(
            f'<bold><ansicyan>[i] </ansicyan><ansimagenta>Select a file to delete</ansimagenta><ansiyellow> > </ansiyellow></bold>')

        try:
            user_input = f"""{prompt(prefix_prompt, placeholder=placeholder).strip()}"""
        except KeyboardInterrupt:
            sys.exit()
        except Exception as e:
            print_error(
                f'An error occurred while getting the file to delete: {e}')
            return

        if user_input.isdigit() == True and int(user_input) in files:
            break
        if user_input.startswith(cmd_start):
            cmd = user_input.split(cmd_start)[1].lower().split()[0]
            if cmd in cmds or cmd in [short[0] for short in cmds.values()]:
                if cmd == 'quit' or cmd == 'q':
                    return
                else:
                    print_error(f'{user_input} is not a valid selection.')
        else:
            print_error(f'{user_input} is not a valid selection.')

    selected_file_path = os.path.join(
        save_directory, f'{files[int(user_input)]}.json')
    try:
        os.unlink(selected_file_path)
        console.print(
            f'[white]Deleted file {selected_file_path}[/]')
        console.print()
    except Exception as e:
        print_error(
            f'Unable remove file in {selected_file_path} because it is being used by another program: {e}')
        return


def copy_message(user_cmd: str) -> None:
    if prompt_count == 0:
        print_error(
            f'Unable to run {user_cmd} because there are no messages from [bold]{to_plain_text(MODEL_NAME)}[/] to copy.')
        return
    last_response: str = chat.history[-1].parts[0].text
    pyperclip.copy(last_response)
    console.print(f'Copied the last message to your clipboard.')
    console.print()


def copy_code_from_last_message(user_cmd: str) -> None:
    if prompt_count == 0:
        print_error(
            f'Unable to run {user_cmd} because there are no messages from [bold]{to_plain_text(MODEL_NAME)}[/] to copy.')
        return
    last_response: str = chat.history[-1].parts[0].text
    code_blocks = re.findall(r'```(\w+)\n(.*?)```', last_response, re.DOTALL)
    if len(code_blocks) == 0:
        print_error(
            f'Unable to run {user_cmd} because there are no code blocks in the last message from [bold]{to_plain_text(MODEL_NAME)}[/].')
        return
    else:
        console.print(
            '[cyan][[bold]i] [magenta]Available code blocks:[/]')
        blocks = {}
        for i, (language, code) in enumerate(code_blocks, 1):
            title_str: str = f'[bold green][{i}]{" " + language}[/]'
            blocks[i] = code
            code_block: str = f'```{language}\n{code}```'
            code_block_panel = Panel(
                Markdown(code_block, 'monokai'),
                border_style='green',
                title=title_str,
                title_align='left',
                subtitle=None
            )
            console.print(code_block_panel)
            console.print()

    while True:
        placeholder = HTML(
            '<ansigray><italic>Enter your number.</italic></ansigray>')
        prefix_prompt = HTML(
            f'<bold><ansicyan>[i] </ansicyan><ansimagenta>Select the code black that you want</ansimagenta><ansiyellow> > </ansiyellow></bold>')

        try:
            user_input = f"""{prompt(prefix_prompt, placeholder=placeholder).strip()}"""
        except KeyboardInterrupt:
            sys.exit()
        except Exception as e:
            print_error(f'An error occurred while getting the code block: {e}')
            return

        if user_input.isdigit() == True and int(user_input) in blocks:
            break
        if user_input.startswith(cmd_start):
            cmd = user_input.split(cmd_start)[1].lower().split()[0]
            if cmd in cmds or cmd in [short[0] for short in cmds.values()]:
                if cmd == 'quit' or cmd == 'q':
                    return
                else:
                    print_error(f'{user_input} is not a valid selection.')
        else:
            print_error(f'{user_input} is not a valid selection.')

    selected_code_block: str = blocks[int(user_input)]
    pyperclip.copy(selected_code_block)
    console.print(f'Copied the code block to your clipboard.')
    console.print()

### End of command handler functions. ###


def get_prompt() -> str:
    global chat, prompt_count
    placeholder = HTML(
        '<ansigray><italic>Enter a prompt here</italic></ansigray>')
    prefix_prompt = HTML(
        f'<bold><ansired>[{prompt_count}] </ansired><ansigreen>Prompt</ansigreen>\n<ansiyellow>> </ansiyellow></bold>')

    try:
        user_prompt = f"""{prompt(prefix_prompt, placeholder=placeholder, key_bindings=kb, multiline=True).strip()}"""
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        print_error(f'An error occurred while getting the prompt: {e}')
        return

    if user_prompt == '':
        print_error('The prompt is empty!')
    elif user_prompt[0] == cmd_start:
        cmd = user_prompt.split(cmd_start)[
            1].lower().split()[0]
        if cmd in cmds or cmd in [short[0] for short in cmds.values()]:
            if cmd == 'quit' or cmd == 'q':
                sys.exit()
            elif cmd == 'help' or cmd == 'h':
                console.print(
                    f'[bold underline]Command[/] [bold]: [underline]Description[/]')
                for cmd, desc in cmds.items():
                    short = '' if desc[0] is None else f'{cmd_start}{desc[0]}'
                    console.print(
                        f'{cmd_start}{cmd}, {short}: {desc[1]}')
                console.print()
            elif cmd == 'save' or cmd == 's':
                save_conversation()
            elif cmd == 'load' or cmd == 'l':
                load_conversation()
            elif cmd == 'delete' or cmd == 'd':
                delete_conversation()
            elif cmd == 'new' or cmd == 'n':
                console.clear()
                chat = model.start_chat(history=[])
                prompt_count = 0
                console.print(banner())
            elif cmd == 'copy' or cmd == 'c':
                copy_message(user_prompt)
            elif cmd == 'copy_code' or cmd == 'cc':
                copy_code_from_last_message(user_prompt)
        else:
            print_error(
                f'{user_prompt} is not in the list of acceptable commands, type [bold underline]{cmd_start}help[/] [red]for more details.[/]')
    else:
        return user_prompt


def send_prompt(user_prompt) -> None:
    console.print()
    title_str: str = f'[bold cyan]✨ {to_plain_text(MODEL_NAME)} ✨'
    LoadingIcon.start_spinning(f'{title_str} is thinking...')
    start_time = time.time()
    try:
        response = chat.send_message(user_prompt)
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        print_error(f"Google API request failed to connect: {e}")
        sys.exit()
    end_time = time.time()

    subtitle_str = f'[bold yellow]Time Elapsed: {(end_time - start_time):.1f}s[/]'
    chat_panel = Panel(
        Markdown(response.text, 'monokai'),
        border_style='cyan',
        title=title_str,
        title_align='left',
        subtitle=subtitle_str,
        subtitle_align='right'
    )

    LoadingIcon.stop_spinning()
    console.print(chat_panel)
    console.print('\n')


def run(init_prompt: str) -> None:
    global prompt_count
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    console.print(banner())

    if init_prompt is not None:
        prompt_count += 1
        send_prompt(init_prompt)

    while True:
        prompt = get_prompt()
        if prompt is not None:
            prompt_count += 1
            send_prompt(prompt)


def main():
    user_prompt = ' '.join(sys.argv[1:]) if sys.argv[1:] else None
    run(user_prompt)


if __name__ == '__main__':
    main()
