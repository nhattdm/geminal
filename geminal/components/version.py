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
from .config import conf
from .console import log


def print_version() -> None:
    log(anything=f"""
%s  ________ %s        %s         %s.__ %s        %s        %s.__    
%s /  _____/ %s  ____  %s  _____  %s|__|%s  ____  %s_____   %s|  |   
%s/   \  ___ %s_/ __ \ %s /     \ %s|  |%s /    \ %s\__  \  %s|  |   
%s\    \_\  \\\%s\  ___/ %s|  Y Y  \\\%s|  |%s|   |  \\\%s / __ \_%s|  |__ 
%s \______  /%s \___  >%s|__|_|  /%s|__|%s|___|  /%s(____  /%s|____/ 
%s        \/ %s     \/ %s      \/ %s    %s     \/ %s     \/ %s
%sA Chatbot on Terminal powered by Google Generative AI.

%sAuthor  : %s{conf['app']['author']}
%sVersion : %s{conf['app']['version']}""" % (
        '[bold bright_blue]', '[bold bright_red]', '[bold bright_yellow]', '[bold bright_blue]', '[bold bright_green]',
        '[bold bright_red]', '[bold bright_yellow]',
        '[bold bright_blue]', '[bold bright_red]', '[bold bright_yellow]', '[bold bright_blue]', '[bold bright_green]',
        '[bold bright_red]', '[bold bright_yellow]',
        '[bold bright_blue]', '[bold bright_red]', '[bold bright_yellow]', '[bold bright_blue]', '[bold bright_green]',
        '[bold bright_red]', '[bold bright_yellow]',
        '[bold bright_blue]', '[bold bright_red]', '[bold bright_yellow]', '[bold bright_blue]', '[bold bright_green]',
        '[bold bright_red]', '[bold bright_yellow]',
        '[bold bright_blue]', '[bold bright_red]', '[bold bright_yellow]', '[bold bright_blue]', '[bold bright_green]',
        '[bold bright_red]', '[bold bright_yellow]',
        '[bold bright_blue]', '[bold bright_red]', '[bold bright_yellow]', '[bold bright_blue]', '[bold bright_green]',
        '[bold bright_red]', '[bold bright_yellow]',
        '[bold bright_magenta]',
        '[bold bright_yellow]', '[bold bright_green]',
        '[bold bright_yellow]', '[bold bright_green]'
    )
        )  # noqa: disable=W605)
