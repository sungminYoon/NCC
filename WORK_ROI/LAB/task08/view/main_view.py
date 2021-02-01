"""
Created by SungMin Yoon on 2020-01-09..
Copyright (c) 2019 year SungMin Yoon. All rights reserved.
"""
import time
import cv2 as cv
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from LAB.common.error import messages

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

    # view 세팅에 사용 됩니다.
    q_graphic = None
    screen_img = None
    screen_rect = None

    mask = None
    mouse_position_list = []

    flood_mask = None
    flood_fill_flags = None

    def __init__(self, parent=None):
        super(View, self).__init__(parent)
        MASK_LIST.clear()
        MOUSE_LIST.clear()
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
        self.screen_img = None
        self.mask = None
        self.flood_mask = None
        self.flood_fill_flags = None

    # 사용자 선택 이미지 준비
    def re_setting(self, path):
        print('View: resetting')
        self.re_default()

        img = cv.imread(path, 1)
        color_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # cv 이미지에서 사이즈를 알아내고
        h, w = color_img.shape[:2]

        # open cv image 를 준비하는대 시간이 필요 합니다 0.1 초 Delay
        self.screen_img = color_img.copy()
        time.sleep(0.1)
        self.mask = np.zeros((h, w), np.uint8)
        time.sleep(0.1)
        self.flood_mask = np.zeros((h + 2, w + 2), np.uint8)
        time.sleep(0.1)
        self.flood_fill_flags = (CONNECTIVITY | cv.FLOODFILL_FIXED_RANGE | cv.FLOODFILL_MASK_ONLY | 255 << 8)
        time.sleep(0.1)

    def save_image(self, cv_mask_path):
        print('View: save_image')
        # 원본이미지 self.screen_img 와 mask 이미지 저장
        # cv.imwrite(cv_ori_path, self.screen_img)
        cv.imwrite(cv_mask_path, self.mask)

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
        if self.screen_img is None:
            print('View: Not image')
            return

        # 마우스 위치 예외 처리
        h, w = self.screen_img.shape
        if h < e.y() or w < e.x():
            print('mouse_position OVER')
            return

        # 사용자 마우스 클릭 이벤트
        self.mouseButtonKind(e.buttons())
        mouse_position = [e.x(), e.y()]

        # 마스크 영역 채우기
        self.flood_mask[:] = 0
        cv.floodFill(self.screen_img, self.flood_mask, (e.x(), e.y()), 0,
                     self.threshold,
                     self.threshold,
                     self.flood_fill_flags)
        mask_copy = self.flood_mask[1:-1, 1:-1].copy()

        # 마스크 2개 가능하게 만들기
        mask_count = len(MASK_LIST)
        if mask_count >= 2:
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
        viz = self.screen_img.copy()

        i: int = 0
        for mask_image in MASK_LIST:
            contours = _find_exterior_contours(mask_image)

            if i == 0:
                viz = cv.drawContours(viz, contours, -1, color=(125,) * 3, thickness=-1)
                viz = cv.addWeighted(self.screen_img, 0.75, viz, 0.25, 0)
                viz = cv.drawContours(viz, contours, -1, color=(255,) * 3, thickness=1)
            else:
                viz = cv.drawContours(viz, contours, -1, color=(125,) * 3, thickness=-1)
                viz = cv.drawContours(viz, contours, -1, color=(255,) * 3, thickness=1)

            i = i + 1

        # 뷰에 마스크 보이기
        height, width = viz.shape
        grey_image = QtGui.QImage(viz, width, height, QtGui.QImage.Format_Grayscale8)
        pix_image = QtGui.QPixmap.fromImage(grey_image)
        self.q_graphic.setPixmap(pix_image)
        self.repaint()


