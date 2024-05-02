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

from .console import log_error
from .utils import quit_program


def __get(key: str, default: str | None) -> str | None:
    value: str | None = os.environ.get(key, default)
    return value


def get_or_default(key: str, default: str) -> str:
    """
    Get a value from environment variable or default if it does not exist.
    """
    value: str = __get(key, default)
    return value


def get_or_none(key: str) -> str | None:
    """
    Get a value from environment variable or None if it does not exist.
    """
    value: str = __get(key, default=None)
    return value


def get_or_error(key: str) -> str:
    """
    Get a value from environment variable or raise an exception and quit the program if it does not exist.
    """
    try:
        value: str = os.environ[key]
        return value
    except Exception as e:
        log_error(
            message=f"Unable to get the \[{key}] environment variable.\n\nError Details: {repr(e)}"
        )  # noqa: disable=W605
        quit_program()


conf = {
    'app': {
        'name': 'Geminal',
        'version': '0.1.0',
        'author': 'nhattdm'
    },
    'settings': {
        'api_key': get_or_error('GOOGLE_API_KEY'),
        'model_name': get_or_default(key='MODEL_NAME', default='gemini-pro'),
        'save_dir': os.path.join(os.environ['HOME'], '.geminal', 'conversations')
    }
}
