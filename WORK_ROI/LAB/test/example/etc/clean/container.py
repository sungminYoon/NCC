"""
Created by SungMin Yoon on 2020-05-20..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""


# 어떠한 맵에서 기준값 밖으로 벗어나는 값인지 확인 하는 코드
class Boundaries:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __contains__(self, _item):
        x, y = _item
        return 0 <= x < self.width and 0 <= y < self.height


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.limits = Boundaries(width, height)

    def __contains__(self, _item):
        return _item in self.limits


if __name__ == '__main__':
    item = [9, 2]       # 임의 값
    g = Grid(10, 10)    # 기준 값

    print(g.__contains__(item))     # 기준 값을 벗어 나는지 확인
    print(g.width, ':', g.height)   # 기준 값 확인





