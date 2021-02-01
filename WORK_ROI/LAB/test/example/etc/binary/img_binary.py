"""
Created by SungMin Yoon on 2020-05-06..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import time
import numpy as np
from PIL import Image

# IMAGE -> BINARY
img = Image.open('test.png')

# png 파일을 numpy 로 변환 합니다.
img = np.array(img)

# 이미지의 128 값 보다 색이 높은 곳을 1이라는 값으로 numpy -> binary 변환 합니다.
binary = np.where(img > 128, 1, 0)

# binary 를 reshape( , )2차원 (1, )1줄 ( , -1) 나머지 자동 맞춤 후 TEXT 저장합니다.
np.savetxt("n01", binary.reshape(1, -1), fmt="%s", header='')

# 파일 저장할 시간을 주고
time.sleep(0.5)

# TEXT -> IMAGE
with open("n01", mode='r') as file:
    fileContent = file.read().split(' ')
    value = []

    # STRING binary 를 INT binary 변환 합니다.
    i = 1
    count = len(fileContent)
    for obj in fileContent:
        if i == count:
            break

        try:
            num = int(obj)
            value.append(num)

        # 마지막 줄 바꿈 STRING 은 예외 처리 합니다.
        except ValueError:
            value.append(0)
            break
        i = i + 1

    print(value)

    # INT binary 를 이미지로 변경 합니다.
    img = Image.new('1', (512, 512), "black")
    img.putdata(value)
    img.show()
