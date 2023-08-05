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
import pandas as pd


class LineRecorder:
    _STATE_IDLE = 0
    _STATE_MOVE = 1

    def __init__(self):
        self._usage()

    def _usage(self):
        print('Press space key to move/stop')
        print('Press s key to save')
        print('Press ESC key to quit')
        print()

    def start(self, file_path):
        KeyEvent.start()
        dispose_all()


class HamsterGroupRecorder(LineRecorder):
    def _create_robot(self):
        return None

    def start(self, file_path):
        super(HamsterGroupRecorder, self).start(file_path)
        
        left_floors = []
        left_wheels = []
        right_wheels = []
        state = LineRecorder._STATE_IDLE
        hamster = self._create_robot()
        if hamster is None:
            KeyEvent.stop()
            return

        while True:
            key = KeyEvent.get_released_key()
            if state == LineRecorder._STATE_IDLE:
                if key == KeyEvent.SPACE:
                    state = LineRecorder._STATE_MOVE
            elif state == LineRecorder._STATE_MOVE:
                diff = (left_floor - 50) * 0.5
                left_wheel = 30 + diff
                right_wheel = 30 - diff
                hamster.wheels(left_wheel, right_wheel)
                left_floors.append(hamster.left_floor())
                left_wheels.append(left_wheel)
                right_wheels.append(right_wheel)
                
                if key == KeyEvent.SPACE:
                    hamster.stop()
                    state = LineRecorder._STATE_IDLE
            
            left_floor = hamster.left_floor()
            if key == 's':
                df = pd.DataFrame({'left_floor': left_floors,
                                   'left_wheel': left_wheels,
                                   'right_wheel': right_wheels})
                df.to_csv(file_path, index=False)
                print('Saved to', file_path)
            elif key == KeyEvent.ESC:
                break

            wait(20)
        
        KeyEvent.stop()
        hamster.dispose()


class HamsterRecorder(HamsterGroupRecorder):
    def _create_robot(self):
        return Hamster()


class HamsterSRecorder(HamsterGroupRecorder):
    def _create_robot(self):
        return HamsterS()
