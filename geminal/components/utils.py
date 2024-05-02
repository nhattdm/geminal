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
import re
import sys


def restart_program() -> None:
    os.system(command='clear')
    os.execl(sys.executable, sys.executable, *sys.argv)


def quit_program() -> None:
    sys.exit()


def to_capitalized_plain_text(s: str) -> str:
    """ 
    Convert a string formatted as 'hello-world', 'hello_world', 'hello.world' to 'Hello World'.
    """
    words: list[str] = re.findall(pattern=r'[a-zA-Z0-9]+', string=s)
    plain_text: str = ' '.join([word.capitalize() for word in words])
    return plain_text


def to_lowercase_plain_text(s: str) -> str:
    """
    Convert a string formatted as 'hello-world', 'hello_world', 'hello.world' to 'hello world'.
    """
    words: list[str] = re.findall(pattern=r'[a-zA-Z0-9]+', string=s)
    plain_text: str = ' '.join([word.lower() for word in words])
    return plain_text


def to_separated_text_w_char(s: str, char: str = '_') -> str:
    """
    Convert a string to separated text using a specific character.

    The default character to separate is '_'.
    """
    words: list[str] = re.findall(pattern=r'[a-zA-Z0-9]+', string=s)
    separated_text: str = char.join([word.lower() for word in words])
    return separated_text
