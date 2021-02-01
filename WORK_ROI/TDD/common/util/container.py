"""
Created by SungMin Yoon on 2020-05-13..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import cv2 as cv
import numpy as np
import pydicom
from TDD.common.path import file_manager

CONNECTIVITY = 4        # 연결성


# 분석이 가능한 이미지 셋을 만듭니다.
def set_cv_image(data_folder, start_path, file_list_image):
    print('Container: data_set_image')
    image_set = []

    for file_name in file_list_image:
        # 상대 경로를 만들고
        image_folder = file_manager.relative_path(data_folder, start_path)
        path = f'{image_folder}/{file_name}'

        # cv 이미지를 생성합니다
        cv_img = cv.imread(path, 1)
        color_img = cv.cvtColor(cv_img, cv.COLOR_BGR2GRAY)
        image_set.append(color_img)

    return image_set


def set_mask(count, img):
    print('Container: data_set_mask')
    flood_mask_set = []
    flood_fill_flags_set = []

    # Open cv mask 들을 초기화 합니다.
    h, w = img.shape[:2]
    for j in range(count):
        flood_mask_set.append(np.zeros((h + 2, w + 2), np.uint8))
        flood_fill_flags_set.append(
            (CONNECTIVITY | cv.FLOODFILL_FIXED_RANGE | cv.FLOODFILL_MASK_ONLY | 255 << 8))

    return flood_mask_set, flood_fill_flags_set


def set_DicomToCv(dicom_folder):
    last_name = dicom_folder[dicom_folder.rfind('/') + 1:]
    source_folder = dicom_folder.replace(last_name, '', 1)
    dicom_list = file_manager.get_dicom_path(source_folder)

    img_list = []
    # Open cv Image 들을 만들어 보관합니다
    i: int = 0
    for file_name in dicom_list:
        dicom_path = f'{source_folder}{file_name}'
        ds = pydicom.read_file(dicom_path)
        img_list.append(ds.pixel_array)
        i = i + 1
        if i >= len(dicom_list):
            break
    return img_list


def set_label(self):
    print('Container: data_set_label')
    print(self._label_set)
