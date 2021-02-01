"""
Created by SungMin Yoon on 2020-10-13..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import math


class Roi:
    image_cv = None
    image_mask = None
    image_size_x = None
    image_size_y = None
    position_list = None

    rect_level = 0          # 레벨 저장
    rect_dimensions = 0     # 넓이
    rect_center_x = 0       # 중심 좌표
    rect_center_y = 0
    rect_start_x = 0        # 시작 좌표
    rect_start_y = 0
    rect_width = 0
    rect_height = 0

    def chk(self):
        if self.rect_height == 0:
            return False
        return True

    def center(self):
        if self.chk() is True:
            self.rect_center_x = math.floor(self.rect_start_x + (self.rect_width / 2))
            self.rect_center_y = math.floor(self.rect_start_y + (self.rect_height / 2))
        else:
            print('roi: center error')

    def dimensions(self):
        if self.chk() is True:
            self.rect_dimensions = self.rect_width * self.rect_height
        else:
            print('roi: center error')
