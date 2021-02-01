"""
Created by SungMin Yoon on 2020-05-18..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import cv2 as cv


def pixels_mask_size(src):
    # 마스크 threshold 영역 넓이 계산
    mask_pixels = cv.countNonZero(src)
    return mask_pixels


def contour(src):
    # threshold 영역의 중심값 찾는 cv 에있는 알고리즘
    _, binary = cv.threshold(src, 127, 255, 0)
    contours, _ = cv.findContours(binary, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

    try:
        for value in contours:
            M = cv.moments(value)
            cX = int(M['m10'] / M['m00'])
            cY = int(M['m01'] / M['m00'])

    except OverflowError:
        print('contour: error')

    # cv2.circle(dst, (cX, cY), 3, (255, 0, 0), -1)
    # cv2.drawContours(dst, [i], 0, (0, 0, 255), 2)
    return cX, cY

