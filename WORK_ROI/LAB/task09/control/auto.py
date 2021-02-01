"""
Created by SungMin Yoon on 2020-05-11..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import time
import numpy as np
import cv2 as cv
import copy
from LAB.common.model.roi import Roi
from LAB.common.util import magic_wand
from LAB.common.util import point2D
from LAB.common.util import img_empty


MINIMUM_DISTANCE = 20   # 쓰레숄드 간 최소 거리


class Auto:

    auto_count = None       # 알고리즘 처리 된 COUNT
    call_progress = None    # 상태 표시 프로그래시브 바 입니다.

    best_list = None         # 결과 이미지
    mask_list = None         # 결과 마스크 이미지
    roi_list = None          # roi 객체 리스트

    standard_obj = None
    standard_image = None

    max_size: int           # 쓰레숄드 찾기 최대 크기
    min_size: int           # 쓰레숄드 찾기 멈춤 최소 크기

    def __init__(self):
        self.best_list = []
        self.mask_list = []
        self.roi_list = []

    def clear_list(self):

        # 리스트 처리 된 양
        self.auto_count = 0

        self.best_list.clear()
        self.mask_list.clear()
        self.roi_list.clear()

        self.standard_obj = Roi()       # 사용자 선택 쓰레숄드 roi
        self.standard_image = None      # 사용자 선택 이미지

    # image 에서 roi 를 지정 합니다.
    def roi_designation(self, cv_image_list, index, mask, total_length):
        print('Auto: roi_designation')

        # 초기화
        self.clear_list()

        # list 원본 복사
        cv_list = copy.deepcopy(cv_image_list)

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
            break_check = self.verdict_rectangle(result_array, self.min_size)
            if break_check is True:
                break

            # 이미지 처리 카운트
            self.auto_count = self.auto_count + 1
            self.call_progress(total_length, self.auto_count)

        # CV image list 위로 탐색
        _max = len(cv_list)
        up: int = 0
        while True:

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
            break_check = self.verdict_rectangle(result_array, self.min_size)
            if break_check is True:
                break

            # 이미지 처리 카운트
            self.auto_count = self.auto_count + 1
            self.call_progress(total_length, self.auto_count)

        sort_best = sorted(self.best_list, key=lambda index_n: index_n[1])
        sort_mask = sorted(self.mask_list, key=lambda index_m: index_m[1])
        return sort_best, sort_mask

    def level_loop(self, cv_image):

        # roi 리스트 초기화
        self.roi_list.clear()

        # 레벨링
        for i in range(0, 100):

            # 연부조직 level
            level = i + (-250)

            # 이미지 레벨링
            level_image = magic_wand.soft_tissue(cv_image, level)

            # 이미지 광역 쓰레숄드
            _, thresh = cv.threshold(level_image, 0, 255, 0)
            contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                x, y, w, h = cv.boundingRect(cnt)

                # 관심 영역 데이터를 객체에 넣고
                roi = Roi()
                roi.rect_level = level
                roi.rect_start_x = x
                roi.rect_start_y = y
                roi.rect_width = w
                roi.rect_height = h
                roi.center()
                roi.dimensions()
                roi.position_list = cnt

                # 관심 영역 사각형 표시
                # level_image = cv.rectangle(level_image, (x, y), (x + w, y + h), (255, 255, 255), 1)

                # 리스트로 보관
                self.roi_list.append(roi)

        return self.roi_list

    def check_result(self, array, cv_image, index):

        roi: Roi = array[2]

        if roi.rect_dimensions > self.standard_obj.rect_dimensions * self.max_size:
            return

        if roi.rect_dimensions < self.min_size:
            return

        # 이미지 roi 표시
        hull = cv.convexHull(roi.position_list)
        view_image = cv.drawContours(cv_image, [hull], 0, (255, 0, 0), 2)

        # 마스크 roi 표시 (채우기 옵션 cv.FILLED)
        empty_mask = img_empty.cv_image(512, 512)
        mask = cv.drawContours(empty_mask, [hull], 0, (255, 0, 0), cv.FILLED)

        # 그려줄 시간을 준다.
        time.sleep(0.1)

        # 리스트에 저장
        mask_group = (mask, index)
        view_group = (view_image, index)
        self.mask_list.append(mask_group)
        self.best_list.append(view_group)

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
        return array

    @classmethod
    def min_diff_pos(cls, array_like, target):
        return np.abs(np.array(array_like) - target).argmin()

    @classmethod
    def verdict_rectangle(cls, array, minimum_size):
        roi: Roi = array[2]
        if minimum_size > roi.rect_width or minimum_size > roi.rect_height:
            return True
        else:
            return False



