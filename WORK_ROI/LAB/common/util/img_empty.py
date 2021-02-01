"""
Created by SungMin Yoon on 2020-09-10..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import numpy as np
import cv2 as cv


def cv_image(cv_width, cv_height):
    # 빈 이미지 생성
    size = (cv_width, cv_height, 1)
    return np.zeros(size, np.uint8)


# 아무것도 없는 이미지를 만들고 add_image 와 합칩니다.
def cv_add(origin_x, origin_y, x_offset, y_offset, add_image):
    result_image = np.zeros((origin_y, origin_x), np.uint8)
    result_image[y_offset:y_offset + add_image.shape[0],
    x_offset:x_offset + add_image.shape[1]] = add_image
    return result_image


# 빈곳 체우기
def fill_blank(src):
    contour, hier = cv.findContours(src, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
    for cnt in contour:
        cv.drawContours(src, [cnt], 0, 255, -1)

    return cv.bitwise_not(src)
