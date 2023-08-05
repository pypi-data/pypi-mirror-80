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
from roboidlab.grid import GridWorld


class QGame:
    def __init__(self):
        dispose_all()

    def start(self, grid_robot):
        world = GridWorld(grid_robot)
        if world.wait_space_key() == KeyEvent.ESC:
            grid_robot.dispose()
            return
        
        total_counts = []
        move_count = 0
        
        while True:
            x = grid_robot.get_x()
            y = grid_robot.get_y()
            action = world.get_max_q_action(x, y)
            next_max_q = world.get_next_max_q(x, y, action)
            
            grid_robot.move(action)
            move_count += 1
            key = world.wait_key()
            if key == KeyEvent.ESC: break
            
            reward = 0
            if key == 'o': reward = 1
            elif key == 'x': reward = -1
            
            world.set_q(x, y, action, reward + 0.9 * next_max_q)
            if key == 'o' or key == 'x':
                if key == 'o':
                    total_counts.append(move_count)
                    move_count = 0
                    print(total_counts)
                    grid_robot.express_good()
                else:
                    grid_robot.express_bad()
                grid_robot.reset()
                if world.wait_space_key() == KeyEvent.ESC: break
            
            wait(20)
        
        grid_robot.dispose()
