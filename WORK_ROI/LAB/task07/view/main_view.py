"""
Created by SungMin Yoon on 2020-01-09..
Copyright (c) 2019 year SungMin Yoon. All rights reserved.
"""
import time
import cv2 as cv
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage
from LAB.common.util import magic_wand


CONNECTIVITY = 4  # 연결성


def _find_exterior_contours(img):
    ret = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    if len(ret) == 2:
        return ret[0]
    elif len(ret) == 3:
        return ret[1]


class View(QtWidgets.QGraphicsView):
    q_graphic = None
    threshold = 5

    screen_img = None
    screen_rect = None
    mask_list = None
    mask = None

    mouse_position = None
    mouse_position_list = None

    flood_mask = None
    flood_fill_flags = None

    def __init__(self, parent=None):
        super(View, self).__init__(parent)
        self.scene = QtWidgets.QGraphicsScene(self)
        self.q_graphic = QtWidgets.QGraphicsPixmapItem()
        self.scene.addItem(self.q_graphic)
        self.setScene(self.scene)
        self.mask_list = []
        self.mouse_position_list = []

    def setup(self, width, height):
        self.screen_rect: QtCore.QRectF = QtCore.QRectF(0.0, 0.0, width, height)
        self.setSceneRect(QtCore.QRectF(self.screen_rect))
        self.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)

    def moveEvent(self, e):
        print('View: moveEvent')

    def mousePressEvent(self, e):
        print('View: mousePressEvent')
        print('View: x =', e.x(), ': y =', e.y())
        self.mouse_position = [e.x(), e.y()]

        if self.screen_img is None:
            print('View: Not image')
            return

        self.flood_mask[:] = 0
        cv.floodFill(self.screen_img, self.flood_mask, (e.x(), e.y()), 0, self.threshold, self.threshold,
                     self.flood_fill_flags)
        flood_mask = self.flood_mask[1:-1, 1:-1].copy()

        mask_count = len(self.mask_list)
        if mask_count > 1:
            self.mask_list = []
            self.mouse_position_list = []

        self.mask_list.append(flood_mask)
        self.mouse_position_list.append(self.mouse_position)
        self._update()

    def mouseMoveEvent(self, e):
        print('View: mouseMoveEvent')
        print('View: x =', e.x(), ': y =', e.y())

    def mouseReleaseEvent(self, e):
        print('View: mouseReleaseEvent')
        print('View: x =', e.x(), ': y =', e.y())

    # 다이콤 이미지 1개를 윈도우 레벨링 합니다.
    def level_threshold(self, value, dicom_image):
        if value < 3000:
            level_image = magic_wand.get_LUT_value(dicom_image, 800, value)
            level_image = cv.convertScaleAbs(level_image)

            # 뷰를 다시 그려 줍니다.
            height, width = level_image.shape
            gray_image: QImage = QtGui.QImage(level_image, width, height, QtGui.QImage.Format_Grayscale8)
            pix_image = QtGui.QPixmap.fromImage(gray_image)
            self.q_graphic.setPixmap(pix_image)
            self.repaint()

    # 이미지 초기화
    def image_init(self):
        self.screen_img = None
        self.mask = None
        self.flood_mask = None
        self.flood_fill_flags = None

    def re_setting(self, path):
        print('View: resetting')
        self.image_init()

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

    def _update(self):
        print('View: _update')
        viz = self.screen_img.copy()

        for mask in self.mask_list:
            contours = _find_exterior_contours(mask)
            viz = cv.drawContours(viz, contours, -1, color=(255,) * 3, thickness=-1)
            viz = cv.addWeighted(self.screen_img, 0.75, viz, 0.25, 0)
            viz = cv.drawContours(viz, contours, -1, color=(255,) * 3, thickness=1)

        height, width = viz.shape
        grey_image = QtGui.QImage(viz, width, height, QtGui.QImage.Format_Grayscale8)
        pix_image = QtGui.QPixmap.fromImage(grey_image)
        self.q_graphic.setPixmap(pix_image)
        self.repaint()

    # 마스크 이미지 업데이트
    def set_mask(self, mask_path):
        print('View: set_mask')
        cv_image = cv.imread(mask_path, 1)
        gray = cv.cvtColor(cv_image, cv.COLOR_BGR2GRAY)
        self.mask = gray
        self._update()

    def save_image(self, cv_mask_path):
        print('View: save_image')
        # 원본이미지 self.screen_img 와 mask 이미지 저장
        # cv.imwrite(cv_ori_path, self.screen_img)
        cv.imwrite(cv_mask_path, self.mask)
