"""
Created by SungMin Yoon on 2021-01-06..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import cv2 as cv


class Merge:
    mutable: list

    def __init__(self):
        self.mutable = list()

    def clear(self):
        self.mutable.clear()

    '''     Method explanation: set_list
        서로 다른 길이의 list 병합하기 위해
        1. 먼저 기준이 되는 list 의 총 크기를 정하고
        2. 가장 큰 길이의 self.mutable 리스트가 기준이 되어
        3. 다른 작은 리스트(input_list)를 계속 받아 들입니다..
    '''
    def mask_overwrite(self, size, input_list):

        count = len(input_list)

        if len(self.mutable) == 0:
            self.mutable = [0]*size

        for i in range(0, count):

            mask, index = input_list[i]

            if self.mutable[index] == 0:
                self.mutable[index] = (mask, index)
            else:
                mutable_mask, mutable_index = self.mutable[index]
                plus_mask = cv.add(mutable_mask, mask)
                self.mutable[mutable_index] = (plus_mask, mutable_index)

        return self.mutable

    def roi_overwrite(self, size, input_list):

        count = len(input_list)

        if len(self.mutable) == 0:
            self.mutable = [0]*size

        for i in range(0, count):

            roi, index = input_list[i]

            if self.mutable[index] == 0:
                self.mutable[index] = (roi, index)
            else:
                mutable_roi, mutable_index = self.mutable[index]

                # 필터를 만들어 바탕 이미지를 해치지 않고 결과 덮어 씌운다.
                gray_filtered = cv.inRange(roi, 255, 255)

                plus_roi = cv.add(gray_filtered, mutable_roi)
                self.mutable[mutable_index] = (plus_roi, mutable_index)

        return self.mutable




