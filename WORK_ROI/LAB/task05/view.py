"""
Created by SungMin Yoon on 2020-01-09..
Copyright (c) 2019 year SungMin Yoon. All rights reserved.
"""
import time
import cv2 as cv
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

CONNECTIVITY = 4  # 연결성


def _find_exterior_contours(img):
    ret = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    if len(ret) == 2:
        return ret[0]
    elif len(ret) == 3:
        return ret[1]


class View(QGraphicsView):
    q_graphic = None
    threshold = 32

    screen_img = None
    mask = None

    _flood_mask = None
    _flood_fill_flags = None

    def __init__(self, parent):
        super().__init__(parent)
        print('DrawView Init')
        self.scene = QGraphicsScene()
        self.q_graphic = QGraphicsPixmapItem()

        self.scene.addItem(self.q_graphic)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.HighQualityAntialiasing)

        rect: QRectF = self.scene.sceneRect()
        print('h =', rect.y(), 'w =', rect.x())

    # 화면 좌측 상단 부터 좌표와 이미지 위치를 맞추기 위해 사용한다.
    def moveEvent(self, e):
        print('DrawView: moveEvent')
        rect = QRectF(self.rect())
        rect.adjust(0, 0, -2, -2)

        self.scene.setSceneRect(rect)
        print(rect)

    def mousePressEvent(self, e):
        print('DrawView: mousePressEvent')
        print('x =', e.x(), ': y =', e.y())

        if self.screen_img is None:
            print('Not image')
            return

        self._flood_mask[:] = 0
        cv.floodFill(self.screen_img, self._flood_mask, (e.x(), e.y()), 0, self.threshold, self.threshold,
                     self._flood_fill_flags)
        flood_mask = self._flood_mask[1:-1, 1:-1].copy()
        self.mask = flood_mask
        self._update()

    def mouseMoveEvent(self, e):
        print('DrawView: mouseMoveEvent')

    def mouseReleaseEvent(self, e):
        print('DrawView: mouseReleaseEvent')

    def image_init(self):
        # 이미지 초기화
        self.screen_img = None
        self.mask = None
        self._flood_mask = None
        self._flood_fill_flags = None

    def re_setting(self, path):
        print('DrawView: resetting')
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
        self._flood_mask = np.zeros((h + 2, w + 2), np.uint8)
        time.sleep(0.1)
        self._flood_fill_flags = (CONNECTIVITY | cv.FLOODFILL_FIXED_RANGE | cv.FLOODFILL_MASK_ONLY | 255 << 8)
        time.sleep(0.1)

    def _update(self):
        print('DrawView: _update')
        viz = self.screen_img.copy()
        contours = _find_exterior_contours(self.mask)
        viz = cv.drawContours(viz, contours, -1, color=(255,) * 3, thickness=-1)
        viz = cv.addWeighted(self.screen_img, 0.75, viz, 0.25, 0)
        viz = cv.drawContours(viz, contours, -1, color=(255,) * 3, thickness=1)

        height, width = viz.shape
        gray_image = QImage(viz, width, height, QImage.Format_Grayscale8)
        pix_image = QPixmap.fromImage(gray_image)
        self.q_graphic.setPixmap(pix_image)
        self.repaint()

    def set_mask(self, mask_path):
        print('DrawView: set_mask')
        # 마스크 이미지 업데이트
        cv_image = cv.imread(mask_path, 1)
        gray = cv.cvtColor(cv_image, cv.COLOR_BGR2GRAY)
        self.mask = gray
        self._update()

    def save_image(self, cv_ori_path, cv_mask_path):
        print('DrawView: save_image')
        # ori 와 mask 이미지 저장
        cv.imwrite(cv_ori_path, self.screen_img)
        cv.imwrite(cv_mask_path, self.mask)
