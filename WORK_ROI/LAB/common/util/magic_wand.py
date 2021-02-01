"""
Created by SungMin Yoon on 2020-06-03..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import cv2 as cv
import numpy as np

CONNECTIVITY = 4        # 연결성


# 이미지 윈도우 레벨 (minimum_unit = 0.1 ~ 0.9 최소 단위 레벨링)
def get_level(img_data, window, level, minimum_unit):
    result = np.piecewise(img_data,
                          [img_data <= (level - minimum_unit - (window - 1) / 2),
                           img_data > (level - minimum_unit + (window - 1) / 2)],
                          [0, 255, lambda data: ((data - (level - minimum_unit)) / (window - 1) + minimum_unit) * (255 - 0)])
    return result


# 마스크 이미지 쓰레숄드
def get_threshold(threshold, img, x, y):

    height, width = img.shape
    flood_mask = np.zeros((height + 2, width + 2), np.uint8)
    flood_fill_flags = (CONNECTIVITY | cv.FLOODFILL_FIXED_RANGE | cv.FLOODFILL_MASK_ONLY | 255 << 8)

    cv.floodFill(img, flood_mask, (x, y), 0,
                 threshold,
                 threshold,
                 flood_fill_flags)
    flood_mask = flood_mask[1:-1, 1:-1].copy()
    return flood_mask


# 연부조직
def soft_tissue(cv_image, soft_tissue_level, window, bone, unit):

    _soft_tissue = get_level(cv_image, window, soft_tissue_level, unit)
    _bone = get_level(cv_image, window, bone, unit)

    # I want to put logo on top-left corner, So I create a ROI
    rows, cols = _bone.shape
    roi = _soft_tissue[0:rows, 0:cols]

    # Now create a mask of logo and create its inverse mask also
    ret, mask = cv.threshold(_bone, 10, 0, cv.THRESH_BINARY)
    mask_inv = cv.bitwise_not(mask)

    # Now black-out the area of logo in ROI
    img1_bg = cv.bitwise_not(roi, roi, mask=mask_inv)

    # Take only region of logo from logo image.
    img2_fg = cv.bitwise_and(_bone, _bone, mask=mask)

    # Put logo in ROI and modify the main image
    dst = cv.add(img1_bg, img2_fg)
    _soft_tissue[0:rows, 0:cols] = dst

    return _soft_tissue


