"""
Created by SungMin Yoon on 2020-04-28..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class Color(QWidget):

    def __init__(self, color, *args, **kwargs):
        super(Color, self).__init__(*args, **kwargs)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)
