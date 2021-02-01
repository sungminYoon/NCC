"""
Created by SungMin Yoon on 2020-05-11..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import numpy as np
import cv2 as cv
from TDD.common.model.roi import Roi
from TDD.common.util import magic_wand
from TDD.common.util import point2D


MINIMUM_SIZE = 20       # 쓰레숄드 최소 크기
MINIMUM_DISTANCE = 20   # 쓰레숄드 간 최소 거리


class Auto:
    best_list = None    # 결과 이미지
    mask_list = None    # 결과 마스크 이미지
    roi_list = None     # roi 객체 리스트

    standard_image = None               # 기준 이미지
    standard_obj: Roi = None            # roi 기준 객체

    def __init__(self):
        self.best_list = []
        self.mask_list = []
        self.roi_list = []

        self.standard_obj = Roi()       # 사용자 선택 쓰레숄드 roi
        self.standard_image = None      # 사용자 선택 이미지

    # dicom 에서 roi 를 지정 합니다.
    def roi_designation(self, cv_list, index, mask):
        print('Auto: roi_designation')

        self.__init__()

        # 리스트 처리 된 양
        count: int = 0

        # roi 가 있는 마스크
        mask_copy = mask.copy()

        # 기준 마스크 이미지 데이터 저장
        x, y, w, h = self.cut_square(mask_copy)
        self.standard_obj.rect_start_x = x
        self.standard_obj.rect_start_y = y
        self.standard_obj.rect_width = w
        self.standard_obj.rect_height = h
        self.standard_obj.dimensions()
        self.standard_obj.center()

        # 기준 이미지와 마스크 저장
        save_image = cv_list[index]
        view_group = (save_image, index)
        mask_group = (mask_copy, index)
        self.best_list.append(view_group)
        self.mask_list.append(mask_group)

        # CV image list 아래로 탐색
        down: int = 0
        while True:
            print('아래로 탐색')

            # index down 아래로 이동
            down = down + 1
            minus = index - down
            _image = cv_list[minus]

            '''반복 로직'''
            # cv 찾아낸 쓰레숄드 리스트
            level_list = self.level_loop(_image)

            # 이미지 데이터 와 쓰레숄드 비교
            result_array = self.proximate(self.standard_obj, level_list)

            # 결과를 cv_image 에 표시
            self.check_result(result_array, _image, minus)

            # 찾기 종료 시점
            break_check = self.verdict_rectangle(result_array, MINIMUM_SIZE)
            if break_check is True:
                break

            # 이미지 처리 카운트
            count = count + 1

        # CV image list 위로 탐색
        _max = len(cv_list)
        up: int = 0
        while True:
            print('위로 탐색')
            # CV image list 끝까지 탐색하면 멈춤
            if up >= _max:
                break

            # index up 위로 이동
            up = up + 1
            plus = index + up
            _image = cv_list[plus]

            '''반복 로직'''
            # cv 찾아낸 쓰레숄드 리스트
            level_list = self.level_loop(_image)

            # 이미지 데이터 와 쓰레숄드 비교
            result_array = self.proximate(self.standard_obj, level_list)

            # 결과를 cv_image 에 표시
            self.check_result(result_array, _image, plus)

            # 찾기 종료 시점
            break_check = self.verdict_rectangle(result_array, MINIMUM_SIZE)
            if break_check is True:
                break

            # 이미지 처리 카운트
            count = count + 1

        print(count)
        print('Auto: END')
        return self.best_list

    def level_loop(self, cv_image):

        # roi 리스트 초기화
        self.roi_list.clear()

        # 연부조직 레벨링
        for i in range(0, 100):
            level = i + (-250)

            # 이미지 레벨링
            level_image = magic_wand.soft_tissue(cv_image, level)

            # 이미지 쓰레숄드
            ret, thresh = cv.threshold(level_image, 0, 255, 0)
            contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            for obj in contours:
                cnt = obj
                x, y, w, h = cv.boundingRect(cnt)

                # 관심 영역 사각형 표시
                level_image = cv.rectangle(level_image, (x, y), (x + w, y + h), (255, 255, 255), 1)

                # 관심 영역 데이터를 객체에 넣고
                roi = Roi()
                roi.rect_level = level
                roi.rect_start_x = x
                roi.rect_start_y = y
                roi.rect_width = w
                roi.rect_height = h
                roi.center()
                roi.dimensions()

                # 리스트로 보관
                self.roi_list.append(roi)

        return self.roi_list

    def check_result(self, array, cv_image, index):

        level = array[1]
        roi: Roi = array[2]

        level_image = magic_wand.soft_tissue(cv_image, level)
        rect_image = cv.rectangle(level_image,
                                (roi.rect_start_x, roi.rect_start_y),
                                (roi.rect_start_x + roi.rect_width, roi.rect_start_y + roi.rect_height),
                                (255, 255, 255), 1)

        view_image = cv.rectangle(cv_image,
                                (roi.rect_start_x, roi.rect_start_y),
                                (roi.rect_start_x + roi.rect_width, roi.rect_start_y + roi.rect_height),
                                (255, 255, 255), 1)

        mask_group = (rect_image, index)
        view_group = (view_image, index)
        self.mask_list.append(mask_group)
        self.best_list.append(view_group)

        # set_index = f'{index}'
        # cv.imshow(set_index, rect_image)
        # cv.waitKey(0)
        # cv.destroyAllWindows()

    @classmethod
    def cut_square(cls, image):
        ret, thresh = cv.threshold(image, 127, 255, 0)
        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        cnt = contours[0]
        x, y, w, h = cv.boundingRect(cnt)
        return x, y, w, h

    @classmethod
    def proximate(cls, standard, obj_list):

        _standard: Roi = standard

        result_list: list = []
        dimensions_list: list = []
        for obj in obj_list:
            roi: Roi = obj

            # 2점 사이 거리
            dist = point2D.dot_distance(_standard.rect_center_x,
                                        _standard.rect_center_y,
                                        roi.rect_center_x,
                                        roi.rect_center_y)

            if dist < MINIMUM_DISTANCE:
                # 넓이
                dimensions = roi.rect_dimensions
                dimensions_list.append(dimensions)
            else:
                # 넓이
                dimensions_list.append(0)

            # 레벨
            level = roi.rect_level

            # 튜플
            group = (dist, level, roi)

            # 결과 저장
            result_list.append(group)

        # 기준 넓이와 가장 유사한 값의 인덱스
        dimensions_index = cls.min_diff_pos(dimensions_list, standard.rect_dimensions)
        array = result_list[dimensions_index]
        print('---------------------------------------------------------------------')
        print(array)

        return array

    @classmethod
    def min_diff_pos(cls, array_like, target):
        return np.abs(np.array(array_like) - target).argmin()

    @classmethod
    def verdict_rectangle(cls, array, minimum_size):

        roi: Roi = array[2]
        # print('minimum_size', minimum_size)
        # print('roi_width', roi.rect_width)
        # print('roi_height', roi.rect_height)

        if minimum_size > roi.rect_width or minimum_size > roi.rect_height:
            return True
        else:
            return False



