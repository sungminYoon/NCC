"""
Created by SungMin Yoon on 2020-09-10..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""

import math
import collections


# 두점사이 거리 구하기
def dot_distance(p1_x, p1_y, p2_x, p2_y):
    Point2D = collections.namedtuple('Point2D', ['x', 'y'])

    p1 = Point2D(x=p1_x, y=p1_y)  # 점1
    p2 = Point2D(x=p2_x, y=p2_y)  # 점2

    a = p1.x - p2.x  # 선 a의 길이
    b = p1.y - p2.y  # 선 b의 길이

    c = math.sqrt((a * a) + (b * b))
    return c
