"""
Created by SungMin Yoon on 2019-12-24..
Copyright (c) 2019 year SungMin Yoon. All rights reserved.
"""

import os
import numpy as np
import png  # pip install pypng
import pydicom
from PyQt5.QtGui import *


def q_imageToMat(incoming_Image):
    incomingImage = incoming_Image.convertToFormat(QImage.Format.Format_RGB32)

    width = incomingImage.width()
    height = incomingImage.height()

    ptr = incomingImage.bits()
    ptr.setsize(height * width * 4)
    arr = np.frombuffer(ptr, np.uint8).reshape((height, width, 4))
    return arr


def dicom_imageToImg(source_folder, output_folder, extension):

    list_of_files = os.listdir(source_folder)
    for file in list_of_files:

        # 폴더에서 가져온 파일의 확장자 명을 제거 합니다.
        file_name = file.replace('.dcm', '', 1)

        try:
            dicom_image = pydicom.read_file(os.path.join(source_folder, file))

            # Convert pixel_array (img) to -> gray image (img_2d_scaled)
            shape = dicom_image.pixel_array.shape

            # Step 1. Convert to float to avoid overflow or underflow losses.
            img_2d = dicom_image.pixel_array.astype(float)

            # Step 2. Rescaling grey scale between 0-255
            img_2d_scaled = (np.maximum(img_2d, 0) / img_2d.max()) * 255.0

            # Step 3. Convert to uint8
            img_2d_scaled = np.uint8(img_2d_scaled)

            # Write the PNG file
            ex = f'.{extension}'
            with open(os.path.join(output_folder, file_name)+ex, 'wb') as img_file:
                w = png.Writer(shape[1], shape[0], greyscale=True)
                w.write(img_file, img_2d_scaled)

        except:
            print('complete')

    return True
