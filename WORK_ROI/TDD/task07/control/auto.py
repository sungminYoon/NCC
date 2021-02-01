"""
Created by SungMin Yoon on 2020-05-11..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import cv2 as cv
import numpy as np
from TDD.common.util import magic_wand
from TDD.common.util import moments
from TDD.common.util import algorithm

CONNECTIVITY = 4  # 연결성


class Auto:

    down_position = None  # 정보리스트 에서 낮은 인덱스로 향하는 좌표 입니다.
    down_count = None  # 정보리스트 에서 낮은 쪽으로 이동한 갯수를 샙니다.
    up_position = None  # 정보리스트 에서 높은 인덱스로 향하는 좌표 입니다.
    up_count = None  # 정보리스트 에서 높은 쪽으로 이동한 갯수를 샙니다.
    mask_size = None  # 마스크의 하얀부분 픽셀 사이즈 입니다.

    result_list = None  # 알고리즘을 거친 이미지를 저장합니다.
    orb_list = None  # 알고리즘을 거친 값을 저장합니다.
    best_list = None  # 알고리즘을 거친 이미지들 중 베스트 이미지들의 모음 입니다.

    _flood_mask = None
    _flood_fill_flags = None

    def __init__(self):
        self.orb_list = []
        self.result_list = []
        self.best_list = []

    @classmethod  # 중심점 찾기
    def _find_exterior_contours(cls, img):
        ret = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        if len(ret) == 2:
            return ret[0]
        elif len(ret) == 3:
            return ret[1]

    # dicom 에서 roi 를 추출 합니다.
    def roi_designation(self, cv_list, location_position, index, mask):
        print('Auto: roi_designation')

        self.__init__()

        count: int = 0      # 정보 리스트  처리 된 양
        down: int = 0       # 정보 리스트  아래로 탐색합니다.
        up: int = 0         # 정보 리스트  위로 탐색합니다.
        minus: int = index  # 아래로

        # CV IMAGE 리스트에서 사용자 선택 기준 이미지
        h, w = mask.shape[:2]
        flood_mask = np.zeros((h + 2, w + 2), np.uint8)
        flood_fill_flags = (CONNECTIVITY | cv.FLOODFILL_FIXED_RANGE | cv.FLOODFILL_MASK_ONLY | 255 << 8)
        _, _, self.mask_size = moments.contour(mask)

        # CV IMAGE 리스트 아래로 탐색
        while True:
            # CV IMAGE 리스트 위치 첫번째 보다 minus 면 멈춤
            if minus <= 0:
                break

            # 인덱스를 다운시켜 아래로 이동
            minus = index - down
            dicom_image = cv_list[minus-1]

            for i in range(50):
                result_image = magic_wand.get_threshold(i,
                                                        dicom_image,
                                                        location_position[0],
                                                        location_position[1],
                                                        flood_mask,
                                                        flood_fill_flags)

                # ORB 알고리즘 적용
                orb = algorithm.features_orb(mask, result_image)
                obj = [orb, i]
                self.result_list.append(result_image)
                self.orb_list.append(obj)

                print('Auto down:', i)

            # 알고리즘 정렬
            self.orb_list.sort()
            best_tuple = self.orb_list[0]
            best_index = best_tuple[1]
            best_image = self.result_list[best_index]

            # 마스크 모양이 픽셀 기준으로 너무 작거나 크면 멈춤
            size = moments.pixels_size(best_image)
            if (self.mask_size * 2) < size or 50 > size:
                self.down_count = count
                break

            # 가장 높은 알고리즘 값의 이미지를 저장 합니다.
            self.best_list.append(best_image)

            # 결과를 초기화 합니다.
            self.result_list = []

            # 1개씩 증감
            down = down + 1
            count = count + 1

        # CV IMAGE 리스트 위로 탐색
        _max = len(cv_list)
        while True:
            # CV IMAGE 리스트 끝까지 탐색하면 멈춤
            if count - 1 >= _max:
                break

            # 인덱스를 업시켜 위로 이동
            plus = index + up
            dicom_image = cv_list[plus]

            for i in range(50):
                result_image = magic_wand.get_threshold(i,
                                                        dicom_image,
                                                        location_position[0],
                                                        location_position[1],
                                                        flood_mask,
                                                        flood_fill_flags)

                # ORB 알고리즘 적용
                orb = algorithm.features_orb(mask, result_image)
                obj = [orb, i]
                self.result_list.append(result_image)
                self.orb_list.append(obj)
                print('Auto up:', i)

            # ORB 알고리즘 값들 정렬
            self.orb_list.sort()
            best_tuple = self.orb_list[0]
            best_index = best_tuple[1]
            best_image = self.result_list[best_index]

            # 마스크 모양이 픽셀 기준으로 너무 작거나 크면 멈춤
            size = moments.pixels_size(best_image)
            if (self.mask_size * 2) < size or 50 > size:
                self.up_count = count
                break

            # ORB 값 정렬 후 가장 높은 값의 이미지를 저장합니다.
            self.best_list.append(best_image)

            # 결과 리스트를 초기화 합니다.
            self.result_list = []

            # 1개씩 증감
            up = up + 1
            count = count + 1

        print('Auto: END')
        return self.best_list
