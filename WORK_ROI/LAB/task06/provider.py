"""
Created by SungMin Yoon on 2020-04-13..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import os
from LAB.common.model.info import Info


class Provider:

    data_list = None

    def __init__(self):
        self.data_list = []

    def data_create(self, data_folder, roi_list):
        file_list = os.listdir(data_folder)
        file_list_png = [file for file in file_list if file.endswith(".png")]

        i = 0
        for name in file_list_png:
            data = Info()
            data.image_name = name
            data.image_path = f'{data_folder}{name}'
            data.image_thumbnail = f'{data_folder}thumbnail/thumbnail_{name}'
            data.image_annotation = None

            # roi 있다면 roi 경로 데이터 생성
            for roi in roi_list:
                cut_string = roi.replace("mask_", "", 1)
                if cut_string == data.image_name:
                    data.image_roi = f'{data_folder}roi/{roi}'

            self.data_list.append(data)
            i = i + 1

    def data_read(self):
        for data in self.data_list:
            print('image_name', data.image_name)
            print('image_path', data.image_path)
            print('image_thumbnail', data.image_thumbnail)
            print('image_annotation', data.image_annotation)
            print('image_roi', data.image_roi)
            print('----------------------------------------------')

    # 데이터 리스트에 roi 경로 1개를 추가합니다.
    def data_update_roi(self, name, path):
        for data in self.data_list:
            if data.image_name == name:
                data.image_roi = path
        return None

    def data_del(self):
        pass

