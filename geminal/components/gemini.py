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
from typing import Dict

from google.generativeai import GenerativeModel, ChatSession
from rich.panel import Panel

from .config import conf
from .console import log, new_line

import google.generativeai as client

supported_models: Dict[str, str] = {
    'gemini-pro': 'Gemini Pro',
    'models/gemini-pro': 'Gemini Pro',
    'gemini-1.0-pro-latest': 'Gemini Pro',
    'gemini-1.0-pro': 'Gemini Pro',
    'gemini-1.0-pro-001': 'Gemini Pro',
    'models/gemini-1.5-pro-latest': 'Gemini 1.5 Pro',
}


def validate_model_name(name: str) -> str:
    if name in supported_models:
        return name
    else:
        return 'gemini-pro'


api_key: str = conf['settings']['api_key']
model_name: str = conf['settings']['model_name']
model_name = validate_model_name(model_name)
display_name: str = supported_models[model_name]

client.configure(api_key=api_key)
model: GenerativeModel = client.GenerativeModel(model_name=model_name)
chat: ChatSession = model.start_chat(history=[])


def get_last_response() -> str:
    last_response: str = chat.history[-1].parts[0].text
    return last_response


def get_chat_history() -> str:
    chat_history: str = str(chat.history)
    return chat_history


def print_welcome() -> None:
    new_line()
    panel: Panel = Panel(
        renderable="Hello there! How can I assist you today?",
        border_style='bright_blue',
        title=f"[bold bright_blue]{display_name}",
        title_align='left',
        subtitle_align='right'
    )
    log(anything=panel)
