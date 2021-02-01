"""
Created by SungMin Yoon on 2020-03-04..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import errno
import os
import time
import zipfile as compression
from datetime import datetime


# 폴더의 png 파일 리스트를 가지고 옵니다.
def find_png_list(source_folder):
    file_list = os.listdir(source_folder)
    file_list_png = [file for file in file_list if file.endswith(".png")]
    return file_list_png


# 저장할 파일 경로 만들기
def get_roi_path(save_path):
    last_name = save_path[save_path.rfind('/') + 1:]
    mask_name = f'roi/mask_{last_name}'
    source_folder = save_path.replace(last_name, '', 1)
    cv_mask_path = f'{source_folder}{mask_name}'
    return cv_mask_path


# 폴더에 있는 다이콤만 읽어 리스트로 만듭니다.
def get_dicom_path(source_folder):
    f_list = os.listdir(source_folder)
    file_list_all = [file for file in f_list if file.endswith(".dcm")]
    return file_list_all


# 원본 이미지 압축하기
def image_compression(ori, mask, zipfile):
    with compression.ZipFile(zipfile, mode='w') as f:
        f.write(ori, compress_type=compression.ZIP_DEFLATED)

    # append 압축파일에 또 다른 파일 추가 마스크 이미지 압축하기
    with compression.ZipFile(zipfile, mode='a') as f:
        f.write(mask, compress_type=compression.ZIP_DEFLATED)
    print('file_manager: 이미지 압축 완료')


# 압축된 이미지 불러오기
def load_zip(zip_path, save_path):
    print('file_manager: load_zip')
    full_name = zip_path[zip_path.rfind('/') + 1:]
    folder_name = full_name.replace(".zip", "")

    # zip 파일인지 확인
    filename, fileExtension = os.path.splitext(full_name)
    if fileExtension != '.zip':
        print('zip 파일이 아닙니다.')
        return 0

    path = f'{save_path}{folder_name}'

    zip_image = compression.ZipFile(zip_path)
    zip_image.extractall(path)

    # 하드에 이미지 저장할 시간을 좀 주고
    time.sleep(0.1)
    print('압축 풀기 완료')

    # 압축을 풀어 넣은 경로와 파일이름을 리턴 합니다.
    simplify_path = f'{path}/'
    ori_name = f'ori_{filename}.png'
    mask_name = f'mask_{filename}.png'
    return simplify_path, ori_name, mask_name


# PNG 저장할 폴더 이름 만들기
def create_folder_img(path):
    folder_name = datetime.today().strftime("%Y%m%d%H%M%S")
    img_folder = f'{path}{folder_name}/'
    return create_folder(img_folder)


# ROI 저장할 폴더 이름 만들기
def create_folder_roi(path):
    roi_folder = f'{path}roi/'
    return create_folder(roi_folder)


def create_folder(path):
    try:
        if not (os.path.isdir(path)):
            os.makedirs(os.path.join(path))
            return path
        return path

    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Error to create roi_folder directory!")
            raise


# 상대 경로
def relative_path(full_path, start_name):

    folder_list = full_path.split('/')
    string_path = []

    try:
        index = folder_list.index(start_name)

        i = 0
        for name in folder_list:
            if i > index:
                string_path.append('/')
                string_path.append(name)
            i = i + 1

        # 리스트의 문자를 -> 문자 열로 변환 합니다.
        string_path = ''.join(string_path)
        result_path = f'{start_name}{string_path}'
        print('file_manager: relative_path = ', result_path)
        return result_path

    except OSError as e:
        if e.errno != errno.EEXIST:
            print('ERROR: relative_path')
            raise
