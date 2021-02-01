"""
Created by SungMin Yoon on 2020-01-09..
Copyright (c) 2019 year SungMin Yoon. All rights reserved.
"""
import cv2 as cv
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from TDD.common.util import convert


CONNECTIVITY = 4    # 연결성


def _find_exterior_contours(img):
    ret = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    if len(ret) == 2:
        return ret[0]
    elif len(ret) == 3:
        return ret[1]


class DrawView(QGraphicsView):

    q_graphic = None
    q_image = None

    img = None
    mask = None
    threshold = 32

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

    # 화면 좌측 상단 부터 좌표와 이미지 위치를 맞추기 위해 사용한다.
    def moveEvent(self, e):
        print('moveEvent')
        rect = QRectF(self.rect())
        rect.adjust(0, 0, -2, -2)

        self.scene.setSceneRect(rect)
        print(rect)

    def mousePressEvent(self, e):
        print('mousePressEvent')
        print('x =', e.x(), ': y =', e.y())

        self._flood_mask[:] = 0
        cv.floodFill(self.img, self._flood_mask, (e.x(), e.y()), 0, self.threshold, self.threshold, self._flood_fill_flags)
        flood_mask = self._flood_mask[1:-1, 1:-1].copy()
        self.mask = flood_mask
        self._update()

    def mouseMoveEvent(self, e):
        print('mouseMoveEvent')

    def mouseReleaseEvent(self, e):
        print('mouseReleaseEvent')

    def tool_init(self):
        print('DrawView : tool_init')
        # pix -> q image -> cv
        pix_map = self.q_graphic.pixmap()
        q_image = QImage(pix_map)
        cv_image = convert.q_imageToMat(q_image)

        gray = cv.cvtColor(cv_image, cv.COLOR_BGR2GRAY)

        h, w = gray.shape[:2]
        self.img = gray.copy()

        self.mask = np.zeros((h, w), np.uint8)
        self._flood_mask = np.zeros((h + 2, w + 2), np.uint8)

        self._flood_fill_flags = (CONNECTIVITY | cv.FLOODFILL_FIXED_RANGE | cv.FLOODFILL_MASK_ONLY | 255 << 8)

    def _update(self):
        print('_update')
        viz = self.img.copy()
        contours = _find_exterior_contours(self.mask)
        viz = cv.drawContours(viz, contours, -1, color=(255,) * 3, thickness=-1)
        viz = cv.addWeighted(self.img, 0.75, viz, 0.25, 0)
        viz = cv.drawContours(viz, contours, -1, color=(255,) * 3, thickness=1)

        height, width = viz.shape
        gray_image = QImage(viz, width, height, QImage.Format_Grayscale8)
        pix_image = QPixmap.fromImage(gray_image)
        self.q_graphic.setPixmap(pix_image)
        self.repaint()

        # cv -> qimage
        # qt_image = convert.cv_imageToQimage(cv_image)
        # pix_image = QPixmap.fromImage(qt_image)
        # self.q_graphic.setPixmap(pix_image)
        # self.repaint()