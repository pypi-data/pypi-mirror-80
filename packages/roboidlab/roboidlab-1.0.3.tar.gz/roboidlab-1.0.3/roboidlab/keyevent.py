# Part of the ROBOID project - http://hamster.school
# Copyright (C) 2016 Kwang-Hyun Park (akaii@kw.ac.kr)
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General
# Public License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330,
# Boston, MA  02111-1307  USA

from pynput.keyboard import Listener, Key


def _on_keyboard_pressed(key):
    if hasattr(key, 'char'): KeyEvent._pressed_key = key.char
    else: KeyEvent._pressed_key = key

def _on_keyboard_released(key):
    if hasattr(key, 'char'): KeyEvent._released_key = key.char
    else: KeyEvent._released_key = key


class KeyEvent:
    SPACE = Key.space
    ESC = Key.esc

    _listener = None
    _pressed_key = None
    _released_key = None

    @staticmethod
    def start():
        KeyEvent.stop()
        KeyEvent._listener = Listener(on_press=_on_keyboard_pressed, on_release=_on_keyboard_released)
        KeyEvent._listener.start()

    @staticmethod
    def stop():
        listener = KeyEvent._listener
        KeyEvent._listener = None
        if listener is not None:
            listener.stop()

    @staticmethod
    def get_pressed_key():
        key = KeyEvent._pressed_key
        KeyEvent._pressed_key = None
        return key

    @staticmethod
    def get_released_key():
        key = KeyEvent._released_key
        KeyEvent._released_key = None
        return key
