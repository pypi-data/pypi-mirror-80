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

from roboid import *
from roboidlab import KeyEvent
import random


class GridWorld:
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
    _ACTIONS = (LEFT, RIGHT, UP, DOWN)

    def __init__(self, grid_robot):
        self._robot = grid_robot
        self._q = [ [ None, None, None, None, None ],
                   [ None, None, None, None, None ],
                   [ None, None, None, None, None ],
                   [ None, None, None, None, None ],
                   [ None, None, None, None, None ] ]
        for y in range(1, 5):
            for x in range(1, 5):
                self._q[y][x] = [0, 0, 0, 0]
        KeyEvent.start()

    def wait_space_key(self):
        while True:
            key = KeyEvent.get_released_key()
            if key == KeyEvent.SPACE or key == KeyEvent.ESC:
                return key
            elif key == 'r':
                self._robot.reset()
            wait(20)

    def wait_key(self):
        while True:
            key = KeyEvent.get_released_key()
            if key == KeyEvent.SPACE or key == KeyEvent.ESC or key == 'o' or key == 'x':
                return key
            elif key == 'r':
                self._robot.reset()
            wait(20)

    def _is_valid_action(self, x, y, action):
        if action == GridWorld.LEFT: return x > 1
        elif action == GridWorld.RIGHT: return x < 4
        elif action == GridWorld.UP: return y < 4
        else: return y > 1

    def _is_opposite_action(self, action):
        direction = self._robot.get_direction()
        if action == GridWorld.LEFT: return direction == GridWorld.RIGHT
        elif action == GridWorld.RIGHT: return direction == GridWorld.LEFT
        elif action == GridWorld.UP: return direction == GridWorld.DOWN
        else: return direction == GridWorld.UP

    def get_max_q_action(self, x, y):
        q_values = []
        valid_actions = []
        for a in GridWorld._ACTIONS:
            if self._is_valid_action(x, y, a) and self._is_opposite_action(a) == False:
                q_values.append(self._q[y][x][a])
                valid_actions.append(a)
        q_max = max(q_values)
        candidates = []
        for a in valid_actions:
            if self._q[y][x][a] == q_max:
                candidates.append(a)
        return random.choice(candidates)

    def get_max_q(self, x, y):
        q_values = []
        for a in GridWorld._ACTIONS:
            if self._is_valid_action(x, y, a):
                q_values.append(self._q[y][x][a])
        return max(q_values)

    def get_next_max_q(self, x, y, action):
        if self._is_valid_action(x, y, action):
            if action == GridWorld.LEFT:
                return self.get_max_q(x-1, y)
            elif action == GridWorld.RIGHT:
                return self.get_max_q(x+1, y)
            elif action == GridWorld.UP:
                return self.get_max_q(x, y+1)
            else:
                return self.get_max_q(x, y-1)
        return 0

    def set_q(self, x, y, action, value):
        self._q[y][x][action] = value


class GridHamster(Hamster):
    def __init__(self, index=0, port_name=None):
        super(GridHamster, self).__init__(index, port_name)
        self.reset()

    def reset(self):
        self._x = 1
        self._y = 1
        self._direction = GridWorld.RIGHT
        super(GridHamster, self).reset()

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_direction(self):
        return self._direction

    def move_left(self):
        if self._direction == GridWorld.RIGHT:
            self.board_left()
            self.board_left()
        elif self._direction == GridWorld.UP:
            self.board_left()
        elif self._direction == GridWorld.DOWN:
            self.board_right()
        self.board_forward()
        self._x -= 1
        self._direction = GridWorld.LEFT

    def move_right(self):
        if self._direction == GridWorld.LEFT:
            self.board_left()
            self.board_left()
        elif self._direction == GridWorld.UP:
            self.board_right()
        elif self._direction == GridWorld.DOWN:
            self.board_left()
        self.board_forward()
        self._x += 1
        self._direction = GridWorld.RIGHT

    def move_up(self):
        if self._direction == GridWorld.LEFT:
            self.board_right()
        elif self._direction == GridWorld.RIGHT:
            self.board_left()
        elif self._direction == GridWorld.DOWN:
            self.board_left()
            self.board_left()
        self.board_forward()
        self._y += 1
        self._direction = GridWorld.UP

    def move_down(self):
        if self._direction == GridWorld.LEFT:
            self.board_left()
        elif self._direction == GridWorld.RIGHT:
            self.board_right()
        elif self._direction == GridWorld.UP:
            self.board_left()
            self.board_left()
        self.board_forward()
        self._y -= 1
        self._direction = GridWorld.DOWN

    def move(self, action):
        if action == GridWorld.LEFT:
            self.move_left()
        elif action == GridWorld.RIGHT:
            self.move_right()
        elif action == GridWorld.UP:
            self.move_up()
        else:
            self.move_down()

    def express_good(self):
        self.leds('green')
        self.note('c4', 0.5)
        self.note('e4', 0.5)
        self.note('g4', 0.5)
        self.leds('off')

    def express_bad(self):
        self.leds('red')
        self.beep()
        self.beep()
        self.leds('off')


class GridHamsterS(HamsterS):
    def __init__(self, index=0, port_name=None):
        super(GridHamsterS, self).__init__(index, port_name)
        self.reset()

    def reset(self):
        self._x = 1
        self._y = 1
        self._direction = GridWorld.RIGHT
        super(GridHamsterS, self).reset()

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_direction(self):
        return self._direction

    def move_left(self):
        if self._direction == GridWorld.RIGHT:
            self.turn_left()
            self.turn_left()
        elif self._direction == GridWorld.UP:
            self.turn_left()
        elif self._direction == GridWorld.DOWN:
            self.turn_right()
        self.move_forward()
        self._x -= 1
        self._direction = GridWorld.LEFT

    def move_right(self):
        if self._direction == GridWorld.LEFT:
            self.turn_left()
            self.turn_left()
        elif self._direction == GridWorld.UP:
            self.turn_right()
        elif self._direction == GridWorld.DOWN:
            self.turn_left()
        self.move_forward()
        self._x += 1
        self._direction = GridWorld.RIGHT

    def move_up(self):
        if self._direction == GridWorld.LEFT:
            self.turn_right()
        elif self._direction == GridWorld.RIGHT:
            self.turn_left()
        elif self._direction == GridWorld.DOWN:
            self.turn_left()
            self.turn_left()
        self.move_forward()
        self._y += 1
        self._direction = GridWorld.UP

    def move_down(self):
        if self._direction == GridWorld.LEFT:
            self.turn_left()
        elif self._direction == GridWorld.RIGHT:
            self.turn_right()
        elif self._direction == GridWorld.UP:
            self.turn_left()
            self.turn_left()
        self.move_forward()
        self._y -= 1
        self._direction = GridWorld.DOWN

    def move(self, action):
        if action == GridWorld.LEFT:
            self.move_left()
        elif action == GridWorld.RIGHT:
            self.move_right()
        elif action == GridWorld.UP:
            self.move_up()
        else:
            self.move_down()

    def express_good(self):
        self.leds('green')
        self.note('c4', 0.5)
        self.note('e4', 0.5)
        self.note('g4', 0.5)
        self.leds('off')

    def express_bad(self):
        self.leds('red')
        self.sound_until_done('beep', 2)
        self.leds('off')
