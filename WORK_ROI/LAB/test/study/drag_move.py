"""
Created by SungMin Yoon on 2020-04-22..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import sys
import time
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget)
from PyQt5.QtGui import QPainter


class MyThread(QThread):
    signal = pyqtSignal(int)

    def __init__(self, parent=None):
        super(MyThread, self).__init__(parent=parent)
        self.value = None
        self.vel = None

    def setValue(self, value):
        self.value = value

    def setVelocity(self, vel):
        self.vel = vel

    def run(self):
        while True:
            self.value += 1
            self.signal.emit(self.value)
            time.sleep(1/self.vel)


class MouseTracker(QWidget):
    distance_from_target = 0
    mouse_x_pos = 0
    mouse_y_pos = 0
    target_x_pos = 500
    target_y_pos = 250
    vel = 60  # pixels per second

    def __init__(self, parent=None):
        super(MouseTracker, self).__init__(parent=parent)
        self.initUI()
        self.setMouseTracking(True)
        self.thread = MyThread(self)
        self.thread.setValue(self.target_x_pos)
        self.thread.setVelocity(self.vel)
        self.thread.signal.connect(self.updatePosition)
        self.thread.start()

    def updatePosition(self, val):
        self.target_x_pos = val
        self.update()

    def initUI(self):
        self.setGeometry(200, 200, 1000, 500)
        self.setWindowTitle('Mouse Tracker')
        self.label = QLabel(self)
        self.label.resize(500, 40)
        self.show()

    def mouseMoveEvent(self, event):
        distance_from_target = round(
            ((event.y() - self.target_y_pos) ** 2 + (event.x() - self.target_x_pos) ** 2) ** 0.5)
        self.label.setText(
            'Coordinates: (%d : %d)' % (event.x(), event.y()) + "   Distance from target: " + str(distance_from_target))
        self.mouse_x_pos = event.x()
        self.mouse_y_pos = event.y()
        self.update()

    def mousePressEvent(self, event):
        self.target_x_pos = event.x()
        self.thread.setValue(self.target_x_pos)
        self.target_y_pos = event.y()
        self.update()

    def paintEvent(self, event):
        q = QPainter()
        q.begin(self)
        q.drawLine(self.mouse_x_pos, self.mouse_y_pos, self.target_x_pos, self.target_y_pos)


app = QApplication(sys.argv)
w = MouseTracker()
sys.exit(app.exec_())