import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget)
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt

class MouseTracker(QWidget):
    distance_from_target = 0
    mouse_x_pos = 0
    mouse_y_pos = 0
    target_x_pos = 500
    target_y_pos = 250

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)

    def initUI(self):
        self.setGeometry(200, 200, 1000, 500)
        self.setWindowTitle('Mouse Tracker')
        self.label = QLabel(self)
        self.label.resize(500, 40)
        self.show()

    def mouseMoveEvent(self, event):
        distance_from_target = round(((event.y() - self.target_y_pos)**2 + (event.x() - self.target_x_pos)**2)**0.5)
        self.label.setText('Coordinates: (%d : %d)' % (event.x(), event.y()) + "   Distance from target: " + str(distance_from_target))
        self.mouse_x_pos = event.x()
        self.mouse_y_pos = event.y()
        self.update()

    def mousePressEvent(self, event):
        self.target_x_pos = event.x()
        self.target_y_pos = event.y()
        self.update()

    def paintEvent(self, event):
        q = QPainter()
        q.begin(self)
        q.drawLine(self.mouse_x_pos, self.mouse_y_pos, self.target_x_pos, self.target_y_pos)

app = QApplication(sys.argv)
ex = MouseTracker()
sys.exit(app.exec_())