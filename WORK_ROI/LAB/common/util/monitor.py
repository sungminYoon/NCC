"""
Created by SungMin Yoon on 2019-12-13..
Copyright (c) 2019 year SungMin Yoon. All rights reserved.
"""
import ctypes


def get_size():
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    f'{screen_width}, {screen_height}'
    return screen_width, screen_height
