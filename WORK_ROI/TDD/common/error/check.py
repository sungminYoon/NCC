"""
Created by SungMin Yoon on 2020-06-29..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import os
import fnmatch


# DICOM 확장자 확인
def extension_dicom(dicom_folder):
    print('error: extension_dicom')

    for file in os.listdir(dicom_folder):
        if fnmatch.fnmatch(file, '*.dcm'):
            return True
        else:
            return False


# PNG 확장자 확인
def extension_png(png_folder):
    print('error: extension_png')

    for file in os.listdir(png_folder):
        if fnmatch.fnmatch(file, '*.png'):
            return True
        else:
            return False


# jpg 확장자 확인
def extension_jpg(jpg_folder):
    print('error: extension_png')

    for file in os.listdir(jpg_folder):
        if fnmatch.fnmatch(file, '*.jpg'):
            return True
        else:
            return False
