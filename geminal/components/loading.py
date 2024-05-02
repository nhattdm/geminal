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
import logging

from time import sleep
from threading import Thread
from typing import Tuple

from rich.console import Console


class Loading:
    sleep_time: float = 0.1
    is_querying: bool | None = None

    __spinner: Tuple = ('⣾ ', '⣽ ', '⣻ ', '⢿ ', '⡿ ', '⣟ ', '⣯ ', '⣷ ')

    @classmethod
    def __action(cls, message: str):
        while cls.is_querying:
            for spin in cls.__spinner:
                Console().print(f' {message} {spin}', end='\r')
                if not cls.is_querying:
                    break
                sleep(cls.sleep_time)

    @classmethod
    def start(cls, message: str):
        try:
            cls.is_querying = True
            thread: Thread = Thread(target=cls.__action, args=(message,))
            thread.start()
            return thread
        except Exception as ex:
            cls.is_querying = False

            def getExc(e):
                return e.args[1] if len(e.args) > 1 else str(e)

            logging.debug(getExc(ex))

    @classmethod
    def stop(cls):
        if cls.is_querying:
            cls.is_querying = False
            sleep(cls.sleep_time)
