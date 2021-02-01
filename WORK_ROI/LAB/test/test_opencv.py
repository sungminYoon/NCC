"""
Created by SungMin Yoon on 2020-01-13..
Copyright (c) 2019 year SungMin Yoon. All rights reserved.
"""
import unittest
import cv2
import numpy as np

IMAGE_PATH = '../image/test.png'


class OpenCv(unittest.TestCase):
    # 각기 다른 이미지 선언
    result = None

    # 매 테스트 메소드 실행 전 동작
    def setUp(self):
        # 맨 끝 숫자 0의 파라미터는 그레이 스케일의
        # CV_8U 타입으로 이미지를 가져 옵니다.
        self.gray_img = cv2.imread(IMAGE_PATH, 0)
        self.color_img = cv2.imread(IMAGE_PATH, cv2.COLOR_RGB2BGR)
        self.clone_img = cv2.copyMakeBorder(self.color_img, 0, 0, 0, 0, cv2.BORDER_REPLICATE)
        self.mask_img = np.zeros(self.clone_img.shape[0:2], np.uint8)
        self.blank_img = np.ones((1024, 768, 1), np.uint8) * 127

    def testShow(self):
        cv2.imshow('a', self.clone_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def testEqual(self):
        print('OpenCv : testEqual')
        # 복제한 이미지를 그레이 스케일로 변환
        self.result = cv2.cvtColor(self.clone_img, cv2.COLOR_RGB2GRAY)

        # 결과 uint8 타입을 유지하고 있는지 비교
        self.assertEqual(self.result.dtype, 'uint8')

    def testFlag(self):
        print('OpenCv : testFlag')
        # 원본 컬러 이미지와 복제한 이미지 모양 비교
        if self.color_img.shape == self.clone_img.shape:
            flag = True
        else:
            flag = False

        self.result = flag
        self.assertTrue(flag)

    # 매 테스트 메소드 실행 후 동작
    def tearDown(self):
        print(' 결과 값 : ' + str(self.result))


'''알아 두어야 할 점은 위 메소드 들은 오류가 있어도 실행 된다.'''
if __name__ == "__main__":
    unittest.main()

    # 아래처럼 메소드를 일일이 작성해 줄 필요가 없다.
    # o = OpenCv()
    # o.testShow()
    # o.testEqual()
    # o.testFlag()

