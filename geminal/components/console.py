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
from typing import Any

from rich.panel import Panel
from rich.console import Console

console: Console = Console()


def log(anything: Any) -> None:
    console.print(anything)
    new_line()


def log_error(message: str) -> None:
    console.print(
        Panel(
            renderable=f'[bright_red]ERROR: {message}[/]',
            border_style='bright_red'
        )
    )
    new_line()


def log_info(message: str) -> None:
    console.print(
        Panel(
            renderable=f'[bold bright_blue]INFO:[/] [bright_blue]{message}',
            border_style='bright_blue'
        )
    )
    new_line()


def new_line() -> None:
    console.print()
