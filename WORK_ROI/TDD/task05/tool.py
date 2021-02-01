"""
Created by SungMin Yoon on 2020-03-04..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import os
import time
import zipfile as compression
from datetime import datetime


class Tool:

    @classmethod
    def get_image_path(cls, save_path):
        # 저장할 파일 이름 만들기
        file_name = datetime.today().strftime("%Y%m%d%H%M%S")
        original_name = f'ori_{file_name}.png'
        mask_name = f'mask_{file_name}.png'
        zip_name = f'{file_name}.zip'

        cv_ori_path = f'{original_name}'
        cv_mask_path = f'{mask_name}'
        cv_zip_path = f'{save_path}{zip_name}'

        return cv_ori_path, cv_mask_path, cv_zip_path

    @classmethod
    def image_compression(cls, ori, mask, zipfile):

        # 원본 이미지 압축하기
        with compression.ZipFile(zipfile, mode='w') as f:
            f.write(ori, compress_type=compression.ZIP_DEFLATED)

        # append 압축파일에 또 다른 파일 추가 마스크 이미지 압축하기
        with compression.ZipFile(zipfile, mode='a') as f:
            f.write(mask, compress_type=compression.ZIP_DEFLATED)
        print('DrawView: 이미지 압축 완료')

    # 압축된 이미지 불러오기
    @classmethod
    def load_zip(cls, zip_path, save_path):
        print('DrawView: load_zip')
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
