"""
Created by SungMin Yoon on 2019-12-24..
Copyright (c) 2019 year SungMin Yoon. All rights reserved.
"""

import unittest
import math


class TddTest(unittest.TestCase):

    a = 0
    b = 0
    result = 0

    # 매 테스트 메소드 실행 전 동작
    def setUp(self):

        self.a = 10
        self.b = 20

    def testAdd(self):
        self.result = math.add(self.a, self.b)

        # 결과 값이 일치 여부 확인
        self.assertEqual(self.result, 31)

    def testSubstract(self):
        self.result = math.substract(self.a, self.b)

        if self.result > 10:
            boolval = True
        else:
            boolval = False

        # 결과 값이 True 여부 확인
        self.assertTrue(boolval)

    def testDivision(self):
        # 결과 값이 ZeroDivisionError 예외 발생 여부 확인
        self.assertRaises(ZeroDivisionError, math.division, 4, 1)

    def testMultiply(self):
        nonechk = True

        self.result = math.multiply(10, 9)

        if self.result > 100:
            nonechk = None

        # 결과 값이 None 여부 확인
        self.assertIsNone(nonechk)

    # 매 테스트 메소드 실행 후 동작
    def tearDown(self):
        print(' 결과 값 : ' + str(self.result))


if __name__ == '__main__':
    unittest.main()