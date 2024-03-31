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
import sys

from components.Console import print_error

__author__: str = 'nhattdm'
__version__: str = '1.0.0'

MODEL_NAME: str = 'gemini-pro'
GOOGLE_API_KEY: str = ''
SAVE_DIRECTORY: str = os.path.join(
    os.environ['HOME'], '.geminal', 'conversations')


def get_google_api_key() -> str:
    global GOOGLE_API_KEY

    try:
        GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
        return GOOGLE_API_KEY
    except Exception as e:
        print_error(
            message='Please set the GOOGLE_API_KEY environment variable before running this program.'
        )
        sys.exit()
