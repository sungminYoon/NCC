"""
Created by SungMin Yoon on 2020-01-09..
Copyright (c) 2019 year SungMin Yoon. All rights reserved.
"""
import time
import cv2 as cv
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

CONNECTIVITY = 4  # 연결성
MASK_LIST = []
MOUSE_LIST = []


# 마법봉 윤곽 찾기 좌표 리스트
def _find_exterior_contours(img):
    ret = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    if len(ret) == 2:
        return ret[0]
    elif len(ret) == 3:
        return ret[1]


class View(QtWidgets.QGraphicsView):

    threshold = None
    mask_select_count = None

    # view 세팅에 사용 됩니다.
    q_graphic = None
    screen_img = None
    screen_rect = None

    # 내부 에서 사용되는 GRAY SCALE 이미지
    gray_scale_img = None

    flood_mask = None
    flood_fill_flags = None

    mouse_position_list: list = []

    def __init__(self, parent=None):
        super(View, self).__init__(parent)
        MASK_LIST.clear()
        MOUSE_LIST.clear()
        self.mask_select_count = 1
        self.scene = QtWidgets.QGraphicsScene(self)
        self.q_graphic = QtWidgets.QGraphicsPixmapItem()
        self.scene.addItem(self.q_graphic)
        self.setScene(self.scene)

    def setup(self, width, height):
        self.screen_rect: QtCore.QRectF = QtCore.QRectF(0.0, 0.0, width, height)
        self.setSceneRect(QtCore.QRectF(self.screen_rect))
        self.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)

    # 초기화
    def re_default(self):

        self.gray_scale_img = None
        self.flood_mask = None
        self.flood_fill_flags = None

    # 사용자 선택 이미지 준비
    def re_setting(self, path):
        print('View: resetting')
        self.re_default()

        img = cv.imread(path, 1)
        cv_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        cv_color = cv.cvtColor(img, cv.COLOR_BGR2RGB)

        # cv 이미지 사이즈
        h, w = cv_gray.shape[:2]

        # open cv image 준비시간 0.1 초 Delay
        self.screen_img = cv_color.copy()
        self.gray_scale_img = cv_gray.copy()
        time.sleep(0.1)
        self.flood_mask = np.zeros((h + 2, w + 2), np.uint8)
        time.sleep(0.1)
        self.flood_fill_flags = (CONNECTIVITY | cv.FLOODFILL_FIXED_RANGE | cv.FLOODFILL_MASK_ONLY | 255 << 8)
        time.sleep(0.1)

    @classmethod
    def get_mask_list(cls):
        return MASK_LIST

    @classmethod
    def mouseButtonKind(cls, buttons):
        if buttons & QtCore.Qt.LeftButton:
            print('LEFT')
        if buttons & QtCore.Qt.MidButton:
            print('MIDDLE')
        if buttons & QtCore.Qt.RightButton:
            print('RIGHT')

    # mark -  Event method
    def moveEvent(self, e):
        print('View: moveEvent')

    # mark -  Event method
    def mousePressEvent(self, e):
        print('View: mousePressEvent')

        # 이미지 예외 처리
        if self.gray_scale_img is None:
            print('View: Not image')
            return

        # 마우스 위치 예외 처리
        h, w = self.gray_scale_img.shape
        if h < e.y() or w < e.x():
            print('View: mouse_position OVER')
            return

        # 사용자 마우스 클릭 이벤트
        self.mouseButtonKind(e.buttons())
        mouse_position = [e.x(), e.y()]

        # 마스크 영역 채우기
        self.flood_mask[:] = 0
        cv.floodFill(self.gray_scale_img, self.flood_mask, (e.x(), e.y()), 1,
                     self.threshold,
                     self.threshold,
                     self.flood_fill_flags)
        mask_copy = self.flood_mask[1:-1, 1:-1].copy()

        # 마스크 5개 가능
        mask_count = len(MASK_LIST)
        if mask_count >= self.mask_select_count:
            MOUSE_LIST.clear()
            MASK_LIST.clear()

        # 마스크 뷰에 업데이트
        MASK_LIST.append(mask_copy)
        MOUSE_LIST.append(mouse_position)
        self._update()

    # mark -  Event method
    def mouseMoveEvent(self, e):
        print('View: mouseMoveEvent')

    # mark -  Event method
    def mouseReleaseEvent(self, e):
        print('View: mouseReleaseEvent')

    def _update(self):
        print('View: _update')

        # 화면에 보여질 칼라 이미지
        viz = self.screen_img.copy()

        # 마스크 마법봉 외각 색을 입힙니다.
        color: int = 127
        i: int = 0

        # 뷰 와 마스크 불투명도 0.5, 0.5 = 1
        viz = cv.addWeighted(self.screen_img, 0.5, viz, 0.5, 0)

        # MASK_LIST 카운트 만큼 색을 구분 합니다.
        for mask_image in MASK_LIST:
            contours = _find_exterior_contours(mask_image)

            # 바닥 밝기를 조금 주고
            viz = cv.drawContours(viz, contours, 0, color=(64, 64, 64))
            j = divmod(i, 3)

            if j[0] > 0:
                one_color = 255
                two_color = i * j[0] + color
                three_color = 255 - (i * j[0])
            else:
                one_color = 255
                two_color = 0
                three_color = 0

            if j[1] == 0:
                viz = cv.drawContours(viz, contours, 0, color=(one_color, 0, two_color))

            if j[1] == 1:
                viz = cv.drawContours(viz, contours, 0, color=(three_color, one_color, two_color))

            if j[1] == 2:
                viz = cv.drawContours(viz, contours, 0, color=(two_color, three_color, one_color))

            i = i + 1

        # 뷰에 마스크 보이기
        height, width = viz.shape[:2]

        # cv 8 비트 칼라에 대응하는 Format_BGR888
        color_image = QtGui.QImage(viz, width, height, QtGui.QImage.Format_BGR888)
        pix_image = QtGui.QPixmap.fromImage(color_image)
        self.q_graphic.setPixmap(pix_image)
        self.repaint()


