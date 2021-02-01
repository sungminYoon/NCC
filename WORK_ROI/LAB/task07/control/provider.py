"""
Created by SungMin Yoon on 2020-04-13..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import os
import time
from LAB.common.model.info import Info
from LAB.common.util import container


class Provider:

    info_list = None        # 이미지 정보 데이터 리스트를 만듭니다.
    image_container = None  # Open cv 이미지 모음 세트 입니다.
    dicom_set = None
    png_set = None

    def __init__(self):
        self.info_list = []

    # level 에 사용 됩니다.
    def data_create_dicom(self, dicom_folder):
        self.dicom_set = container.set_DicomToCv(dicom_folder)

    # 뷰 테이블에 사용 됩니다.
    def data_create(self, start_path, data_folder, roi_list):

        file_list = os.listdir(data_folder)
        file_list.sort()
        file_list_png = [file for file in file_list if file.endswith(".png")]

        # container 에서 image_set 을 생성합니다.
        self.image_container = container.set_cv_image(data_folder, start_path, file_list_png)

        # container 에서 image_set 파일쓰기 시간을 줍니다.
        time.sleep(1)

        print('Provider: Open cv image data set 생성을 완료 했습니다.')

        i = 0
        for name in file_list_png:
            info = Info()
            info.image_name = name
            info.image_path = f'{data_folder}{name}'
            info.image_thumbnail = f'{data_folder}thumbnail/thumbnail_{name}'
            info.image_annotation = None
            info.image_data = self.image_container[i]

            # roi 있다면 roi 경로 데이터 생성
            for roi in roi_list:
                cut_string = roi.replace("mask_", "", 1)
                if cut_string == info.image_name:
                    info.image_roi = f'{data_folder}roi/{roi}'

            self.info_list.append(info)
            i = i + 1

    def data_read(self):
        for info in self.info_list:
            print('image_name', info.image_name)
            print('image_path', info.image_path)
            print('image_thumbnail', info.image_thumbnail)
            print('image_annotation', info.image_annotation)
            print('image_roi', info.image_roi)
            print('image_data', True if info.image_data is not None else False)
            print('----------------------------------------------')

    def get_data_path(self, index):
        info = self.info_list[index]
        return info.image_path

    # 데이터 속성에 roi 경로 1개를 추가합니다.
    def data_update_roi(self, name, path):
        for info in self.info_list:
            if info.image_name == name:
                info.image_roi = path
        return None

    def data_del(self):
        pass

