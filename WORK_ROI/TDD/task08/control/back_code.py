"""
Created by SungMin Yoon on 2020-10-08..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""

"""
Created by SungMin Yoon on 2020-05-11..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""

import math
import cv2 as cv
from TDD.common.util import algorithm
from TDD.common.util import magic_wand
from TDD.common.util import point2D

THRESHOLD_VALUE = 4


class Auto:
    best_list = None  # 결과 이미지

    standard_image = None  # 기준 이미지
    standard_trim = None
    trim_dicom = None  # 잘라낸 이미지
    cv_image = None  # 오픈 cv 이미지
    level_mask = None

    save_x = None
    save_y = None

    _flood_mask = None  # 쓰레숄드 마스크
    _flood_fill_flags = None  # 쓰레숄드 체우기 flag

    def __init__(self):
        self.best_list = []
        self.standard_image = None
        self.standard_trim = None
        self.cv_image = None
        self.save_x = None
        self.save_y = None

    # dicom 에서 roi 를 지정 합니다.
    def roi_designation(self, cv_list, index, mask):
        print('Auto: roi_designation')

        self.__init__()

        count: int = 0  # 리스트 처리 된 양
        down: int = 0  # 리스트 아래로 탐색합니다.
        up: int = 0  # 리스트 위로 탐색합니다.
        minus: int = index  # 리스트 인덱스 아래로 이동

        # 가공할 다이콤 이미지 준비
        self.cv_image = cv_list[index].copy()

        # 마스크 의 ROI 영역
        mask_copy = mask.copy()

        cv.imshow('mask_copy', mask_copy)
        cv.waitKey(0)
        cv.destroyAllWindows()

        # 템플릿용 사각형 크기 교정
        x, y, w, h = self.cut_square(mask_copy)
        correction: int = 2
        _x = x - correction
        _y = y - correction
        _w = w + (correction * 2)
        _h = h + (correction * 2)

        # 중심좌표 저장
        center_x = _x + (_w / 2)
        center_y = _y + (_h / 2)

        # standard_image 저장
        self.best_list.append(self.standard_image)

        # CV image list 아래로 탐색
        while True:
            print('아래로 탐색')
            # CV image list 위치 첫번째 보다 minus 면 멈춤
            if minus <= 0:
                break

            # index down 아래로 이동
            down = down + 1
            minus = index - down
            _image = cv_list[minus - 1]

            # title = f'{minus}'
            # cv.imshow(title, _image)
            # cv.waitKey(0)
            # cv.destroyAllWindows()
            print('minus = ', minus)

            # 반복 알고리즘
            best_image, switch = self.loop_logic(_image, THRESHOLD_VALUE)
            if switch is True:
                break

            self.best_list.append(best_image)
            count = count + 1

        # CV image list 위로 탐색
        _max = len(cv_list)
        plus = index
        self.trim_dicom = self.standard_trim

        while True:
            print('위로 탐색')
            # CV image list 끝까지 탐색하면 멈춤
            if plus >= _max:
                break

            # index up 위로 이동
            up = up + 1
            plus = index + up
            _image = cv_list[plus]
            print('plus = ', plus)

            # 반복 알고리즘
            best_image, switch = self.loop_logic(_image, THRESHOLD_VALUE)
            if switch is True:
                break

            self.best_list.append(best_image)
            count = count + 1

        print(count)
        print('Auto: END')
        return self.best_list

    @classmethod
    def cut_square(cls, image):
        ret, thresh = cv.threshold(image, 127, 255, 0)
        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        cnt = contours[0]
        x, y, w, h = cv.boundingRect(cnt)
        return x, y, w, h

    def loop_logic(self, dicom_image, threshold_value):

        # 연부조직 레벨링
        for i in range(0, 1600):
            level = i + (-400)
            level_mask = magic_wand.soft_tissue(dicom_image, level)
            title = f'{level}'
            cv.imshow(title, level_mask)
            cv.waitKey(0)
            cv.destroyAllWindows()

        # 템플릿 알고리즘을 결과 좌표를 가지고 쓰레숄드 알고리즘을 적용합니다.
        rectangle_list = algorithm.template(dicom_image, self.trim_dicom)

        # 지역 변수 초기화
        local_count: int = 0
        comparative_list = []
        threshold_list = []

        # 템플릿 알고리즘 결과 좌표
        for obj in rectangle_list:
            template_x = obj[0]
            template_y = obj[1]

            # 템플릿 결과 좌표의 중심 좌표
            trim_h, trim_w = self.trim_dicom.shape
            center_x = math.floor(template_x + (trim_w / 2))
            center_y = math.floor(template_y + (trim_h / 2))
            threshold_image = magic_wand.get_threshold(threshold_value, level_mask, center_x, center_y)

            # title = f'{local_count}'
            # cv.imshow(title, threshold_image)
            # cv.waitKey(0)
            # cv.destroyAllWindows()

            # 두점사이 거리 저장
            distance = point2D.dot_distance(self.save_x, self.save_y, center_x, center_y)
            comparative_list.append([distance, local_count, center_x, center_y])
            threshold_list.append(threshold_image)
            local_count = local_count + 1

        # 정렬
        comparative_list.sort()
        best_tuple = comparative_list[0]

        # tuple Parsing
        self.save_x = best_tuple[2]
        self.save_y = best_tuple[3]

        best_index = best_tuple[1]
        choice_image = threshold_list[best_index]

        # 리스트 비우기
        comparative_list.clear()
        threshold_list.clear()
        rectangle_list.clear()

        # threshold_image 의 ROI 영역을 정사각형 크기로 자른다.
        threshold_copy = choice_image.copy()
        x, y, w, h = self.cut_square(threshold_copy)

        self.trim_dicom = dicom_image[y:y + h, x:x + w]

        # 빈곳 체우기 로직
        result_image = algorithm.fill_blank(choice_image)

        # ORB 알고리즘 적용
        orb = algorithm.features_orb(choice_image, self.standard_image)
        print('점수 = ', orb)

        cv.imshow('result_image', result_image)
        cv.waitKey(0)
        cv.destroyAllWindows()

        # TODO: 할일
        switch = False
        # if orb[0] > 2000 or orb[0] < 100:
        #     switch = True

        return result_image, switch

    @classmethod
    def level_loop(cls, mask):

        # 연부조직 레벨링
        for i in range(0, 1):
            level = i + (-300)
            level_mask = magic_wand.soft_tissue(mask, level)
            title = f'{level}'
            cv.imshow(title, level_mask)
            cv.waitKey(0)
            cv.destroyAllWindows()



