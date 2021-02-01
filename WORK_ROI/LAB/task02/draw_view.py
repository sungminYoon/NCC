"""
Created by SungMin Yoon on 2019-12-17..
Copyright (c) 2019 year SungMin Yoon. All rights reserved.
"""
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class DrawView(QGraphicsView):

    pix_map = None

    def __init__(self, parent):
        super().__init__(parent)
        self.scene = QGraphicsScene()
        self.pix_map = QGraphicsPixmapItem()
        self.scene.addItem(self.pix_map)
        self.setScene(self.scene)

        self.items = []

        self.start = QPointF()
        self.end = QPointF()

        self.setRenderHint(QPainter.HighQualityAntialiasing)

    def moveEvent(self, e):
        print('moveEvent')
        rect = QRectF(self.rect())
        rect.adjust(0, 0, -2, -2)

        self.scene.setSceneRect(rect)
        print(rect)

    def mousePressEvent(self, e):
        print('mousePressEvent')
        if e.button() == Qt.LeftButton:
            # 시작점 저장
            self.start = e.pos()
            self.end = e.pos()

    def mouseMoveEvent(self, e):
        print('mouseMoveEvent')
        if e.buttons() & Qt.LeftButton:

            self.end = e.pos()

            pen = QPen(QColor(100, 100, 100), 5)
            path = QPainterPath()
            path.moveTo(self.start)
            path.lineTo(self.end)

            self.scene.addPath(path, pen)
            self.start = e.pos()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            print('mouseReleaseEvent')


