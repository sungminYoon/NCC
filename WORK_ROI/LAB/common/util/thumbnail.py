"""
Created by SungMin Yoon on 2020-04-10..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import os
import errno
from PIL import Image


def img_toThumbnail(data_folder, extension):
    find_name = f'{extension}'
    file_list = os.listdir(data_folder)
    file_list_img = [file for file in file_list if file.endswith(find_name)]

    output_folder = f'{data_folder}thumbnail'

    try:
        if not (os.path.isdir(output_folder)):
            os.makedirs(os.path.join(output_folder))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!")
            raise

    for name in file_list_img:
        image_path = f'{data_folder}{name}'

        with Image.open(image_path) as im:
            new_path = f'{output_folder}/thumbnail_{name}'
            im.thumbnail((50, 50))
            im.save(new_path)
