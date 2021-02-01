"""
Created by SungMin Yoon on 2021-01-06..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
from PyQt5.QtWidgets import *


def message(title, msg):
    print('Window: notice')
    buttonReply = QMessageBox.question(None, title, msg, QMessageBox.Yes)
    if buttonReply == QMessageBox.Yes:
        print('Yes clicked.')