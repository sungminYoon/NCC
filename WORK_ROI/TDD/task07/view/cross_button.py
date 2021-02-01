"""
Created by SungMin Yoon on 2020-04-28..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

TITLE = 'Cross Button'
BUTTON_IDLE = 'background-color: lightBlue'
BUTTON_CLICK = 'background-color: lightGreen'


class CrossButton(QHBoxLayout):

    button_list = []

    pushButton2 = None      # left button
    pushButton4 = None      # top button
    pushButton5 = None      # center button
    pushButton6 = None      # down button
    pushButton8 = None      # right button

    def __init__(self, parent=None):
        super(CrossButton, self).__init__(parent)

        # 십자 방향 버튼을 생성 합니다.
        self.pushButton1 = QPushButton()
        self.pushButton2 = QPushButton()
        self.pushButton3 = QPushButton()
        self.pushButton4 = QPushButton()
        self.pushButton5 = QPushButton()
        self.pushButton6 = QPushButton()
        self.pushButton7 = QPushButton()
        self.pushButton8 = QPushButton()
        self.pushButton9 = QPushButton()

        # 십자 버튼 색입니다.
        self.pushButton2.setStyleSheet(BUTTON_IDLE)
        self.pushButton4.setStyleSheet(BUTTON_IDLE)
        self.pushButton5.setStyleSheet(BUTTON_IDLE)
        self.pushButton6.setStyleSheet(BUTTON_IDLE)
        self.pushButton8.setStyleSheet(BUTTON_IDLE)

        # 기능없는 십자영역 밖의 버튼은 숨김
        self.pushButton1.hide()
        self.pushButton3.hide()
        self.pushButton7.hide()
        self.pushButton9.hide()

        # 번튼 이벤트 등록
        self.pushButton2.clicked.connect(self.leftButtonClicked)
        self.pushButton4.clicked.connect(self.topButtonClicked)
        self.pushButton5.clicked.connect(self.centerButtonClicked)
        self.pushButton6.clicked.connect(self.downButtonClicked)
        self.pushButton8.clicked.connect(self.rightButtonClicked)

        self.pushButton2.setText('left')
        self.pushButton4.setText('top')
        self.pushButton5.setText('center')
        self.pushButton6.setText('down')
        self.pushButton8.setText('right')

        # 버튼 리스트에 버튼 등록
        self.button_list.append(self.pushButton2)
        self.button_list.append(self.pushButton4)
        self.button_list.append(self.pushButton5)
        self.button_list.append(self.pushButton6)
        self.button_list.append(self.pushButton8)

        # 레이아웃에 버튼 배치
        a_layout = QVBoxLayout()
        b_layout = QVBoxLayout()
        c_layout = QVBoxLayout()
        a_layout.addWidget(self.pushButton1, alignment=Qt.AlignRight)
        a_layout.addWidget(self.pushButton2, alignment=Qt.AlignRight)
        a_layout.addWidget(self.pushButton3, alignment=Qt.AlignRight)
        b_layout.addWidget(self.pushButton4, alignment=Qt.AlignRight)
        b_layout.addWidget(self.pushButton5, alignment=Qt.AlignRight)
        b_layout.addWidget(self.pushButton6, alignment=Qt.AlignRight)
        c_layout.addWidget(self.pushButton7, alignment=Qt.AlignRight)
        c_layout.addWidget(self.pushButton8, alignment=Qt.AlignRight)
        c_layout.addWidget(self.pushButton9, alignment=Qt.AlignRight)

        # 박스 레이아웃에 버튼 레이아웃 넣기 && 그리드 레이아웃 으로 만드는것 보다 보기 좋아 사용
        self.addLayout(a_layout)
        self.addLayout(b_layout)
        self.addLayout(c_layout)

    def leftButtonClicked(self):
        print('CrossButton : leftButtonClicked')
        text = self.pushButton2.text()
        self.color_controller(text)

    def topButtonClicked(self):
        print('CrossButton : topButtonClicked')
        text = self.pushButton4.text()
        self.color_controller(text)

    def centerButtonClicked(self):
        print('CrossButton : centerButtonClicked')
        text = self.pushButton5.text()
        self.color_controller(text)

    def downButtonClicked(self):
        print('CrossButton : downButtonClicked')
        text = self.pushButton6.text()
        self.color_controller(text)

    def rightButtonClicked(self):
        print('CrossButton : rightButtonClicked')
        text = self.pushButton8.text()
        self.color_controller(text)

    def color_controller(self, active_button):
        print('CrossButton : color_controller')

        for button in self.button_list:
            btn: QPushButton = button
            text = btn.text()
            if text != active_button:
                change: QPushButton = button
                change.setStyleSheet(BUTTON_IDLE)
            else:
                change: QPushButton = button
                change.setStyleSheet(BUTTON_CLICK)