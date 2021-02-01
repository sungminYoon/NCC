"""
Created by SungMin Yoon on 2020-05-11..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import copy
import cv2 as cv
import numpy as np
from TDD.common.model.roi import Roi
from TDD.common.util import magic_wand
from TDD.common.util import point2D
from TDD.common.util import img_empty

MINIMUM_DISTANCE = 20   # 쓰레숄드 간 최소 거리


class Auto:

    auto_count = None       # 알고리즘 처리 된 COUNT
    call_progress = None    # 상태 표시 프로그래시브 바 입니다.

    best_list = None         # 결과 이미지
    mask_list = None         # 결과 마스크 이미지
    roi_list = None          # roi 객체 리스트
    detection_list = None    # 검출된 레벨 저장 리스트

    standard_obj = None     # 사용자 선택 기준 객체
    standard_save = None    # 기준 객체 저장
    standard_image = None   # 기준 이미지

    max_size: int           # 쓰레숄드 찾기 최대 크기
    min_size: int           # 쓰레숄드 찾기 멈춤 최소 크기
    level_range: int        # 레벨링 범위를 정합니다. 디폴트 0~ 100 사이 입니다.
    level_start: int        # 레벨링 시작 위치를 정합니다. 디폴트 -250 입니다.
    level_window: int       # 레벨링 윈도우 기본값은 800 입니다.
    level_bone: int         # 윈도우 레벨이미지 에서 제거할 뼈 또는 레벨 값입니다. 디폴트 600 입니다.
    level_unit: float       # 레벨링 최소 단위 입니다. 디폴트 0.1 입니다.
    level_overwrite: int    # 윈도우 레벨이미지 에서 찾은 마스크 덮어쓰기 카운트 입니다. 디폴트는 10 입니다.

    def __init__(self):
        self.best_list = []
        self.mask_list = []
        self.roi_list = []
        self.detection_list = []

    def default_setting(self, _max, _min, _range, _scope, _window, _bone, _unit, _over):
        self.max_size = _max
        self.min_size = _min
        self.level_range = _range
        self.level_start = _scope
        self.level_window = _window
        self.level_bone = _bone
        self.level_unit = _unit
        self.level_overwrite = _over

    def clear_list(self):

        # 리스트 처리 된 양
        self.auto_count = 0

        self.best_list.clear()
        self.mask_list.clear()
        self.roi_list.clear()

        self.standard_obj = Roi()       # 사용자 선택 쓰레숄드 roi
        self.standard_save = None       # 위로 탐색 기준 임시 저장 객체
        self.standard_image = None      # 사용자 선택 이미지

    # image 에서 roi 를 지정 합니다.
    def roi_designation(self, cv_image_list, index, mask, total_length):
        print('Auto: roi_designation')

        # 초기화
        self.clear_list()

        # list 원본 복사
        cv_list = copy.deepcopy(cv_image_list)

        # 이미지 크기
        size_h, size_w = mask.shape[:2]

        # 기준 마스크 이미지 데이터 저장
        x, y, w, h = self.cut_square(mask)
        self.standard_obj.image_mask = mask
        self.standard_obj.image_size_x = size_w
        self.standard_obj.image_size_y = size_h
        self.standard_obj.rect_start_x = x
        self.standard_obj.rect_start_y = y
        self.standard_obj.rect_width = w
        self.standard_obj.rect_height = h
        self.standard_obj.dimensions()
        self.standard_obj.center()

        # CV image list 아래로 탐색
        down: int = 0
        while True:
            # index down 아래로 이동

            minus = index - down
            _image = cv_list[minus]
            down = down + 1

            '''반복 로직'''
            # cv 찾아낸 쓰레숄드 리스트
            level_list = self.level_loop(_image)

            # 기준 데이터 와 쓰레숄드 비교
            result_data = self.proximate(self.standard_obj, level_list)

            # 결과를 화면에 표시
            self.check_result(result_data, _image, minus)

            # 찾기 종료 시점
            break_check = self.verdict_rectangle(result_data[0], self.min_size)
            if break_check is True:
                break

            # 이미지 처리 카운트
            self.auto_count = self.auto_count + 1
            self.call_progress(total_length, self.auto_count)

        # CV image list 위로 탐색
        _max = len(cv_list)-1
        up: int = 0
        plus: int = 0

        self.standard_obj = copy.deepcopy(self.standard_save)

        while True:
            # CV image list 끝까지 탐색하면 멈춤
            if plus >= _max:
                break

            # index up 위로 이동
            up = up + 1
            plus = index + up
            _image = cv_list[plus]

            '''반복 로직'''
            # 찾아낸 쓰레숄드 리스트
            level_list = self.level_loop(_image)

            # 기준 데이터 와 쓰레숄드 비교
            result_data = self.proximate(self.standard_obj, level_list)

            # 결과를 화면에 표시
            self.check_result(result_data, _image, plus)

            # 찾기 종료 시점
            break_check = self.verdict_rectangle(result_data[-1], self.min_size)
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
        for i in range(0, self.level_range):

            # 연부조직 level
            level = i + self.level_start

            # 이미지 레벨링
            level_image = magic_wand.soft_tissue(cv_image,
                                                 level,
                                                 self.level_window,
                                                 self.level_bone,
                                                 self.level_unit)

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

    def check_result(self, roi_data, cv_image, index):

        # roi 찾기 한계 설정
        get_roi = roi_data[0]
        roi: Roi = get_roi
        if roi.rect_dimensions > self.standard_obj.rect_dimensions * self.max_size:
            return

        if roi.rect_dimensions < self.min_size:
            return

        # 마스크 roi 표시 (채우기 옵션 cv.FILLED)
        h, w = cv_image.shape[:2]
        mask = img_empty.cv_image(w, h)
        hull = None
        for obj in roi_data:
            hull = obj.position_list
            mask_2 = cv.drawContours(mask, [hull], 0, (255, 0, 0), cv.FILLED)
            mask = cv.add(mask, mask_2)

        # 이미지 roi 표시
        view_image = cv.drawContours(cv_image, [hull], 0, (255, 0, 0), 1)

        # 기준 변경
        x, y, w, h = self.cut_square(mask)
        self.standard_obj.image_mask = mask
        self.standard_obj.rect_start_x = x
        self.standard_obj.rect_start_y = y
        self.standard_obj.rect_width = w
        self.standard_obj.rect_height = h
        self.standard_obj.dimensions()
        self.standard_obj.center()
        self.standard_obj.position_list = hull

        # 기준 ROI 저장
        if self.standard_save is None:
            self.standard_save = copy.deepcopy(self.standard_obj)

        # 리스트에 저장
        mask_group = (mask, index)
        view_group = (view_image, index)

        self.mask_list.append(mask_group)
        self.best_list.append(view_group)

    def proximate(self, standard: Roi, obj_list: object):

        level_list: list = []
        level_roi_list: list = []
        dimensions_list: list = []
        for obj in obj_list:
            roi: Roi = obj

            # 2점 사이 거리
            dist = point2D.dot_distance(standard.rect_center_x,
                                        standard.rect_center_y,
                                        roi.rect_center_x,
                                        roi.rect_center_y)

            if dist < MINIMUM_DISTANCE:
                # 넓이
                dimensions = roi.rect_dimensions
                dimensions_list.append(dimensions)
            else:
                # 넓이
                dimensions_list.append(0)

            # 결과 저장
            level_list.append(roi)

        # 기준 넓이와 가장 유사한 값의 인덱스 의 ROI 덮어쓰기
        # level_overwrite 몇번 덮어 쓸것인가.
        # 덮어 쓰면서 rect 크기 감산 또는 증감 (i * 10))
        for i in range(0, self.level_overwrite):
            dimensions_index = self.min_diff_pos(dimensions_list, standard.rect_dimensions - (i * self.level_overwrite))
            level_roi_list.append(level_list[dimensions_index])

        for i in range(0, self.level_overwrite):
            dimensions_index = self.min_diff_pos(dimensions_list, standard.rect_dimensions + (i * self.level_overwrite))
            level_roi_list.append(level_list[dimensions_index])

        return level_roi_list

    @classmethod
    def cut_square(cls, image):
        ret, thresh = cv.threshold(image, 127, 255, 0)
        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        cnt = contours[0]
        x, y, w, h = cv.boundingRect(cnt)
        return x, y, w, h

    @classmethod
    def min_diff_pos(cls, array_like, target):
        return np.abs(np.array(array_like) - target).argmin()

    @classmethod
    def verdict_rectangle(cls, roi_data, minimum_size):
        roi: Roi = roi_data
        if minimum_size > roi.rect_width or minimum_size > roi.rect_height:
            return True
        else:
            return False



