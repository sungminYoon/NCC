"""
Created by SungMin Yoon on 2019-12-17..
Copyright (c) 2019 year SungMin Yoon. All rights reserved.
"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from LAB.common.util import monitor
from LAB.task01.draw_view import DrawView

TITLE_WINDOW = 'ROI TOOL'
TOOL_OPEN = 'IMAGE Open'

'''간단한 큐티 뷰 테스트'''


class Window(QWidget):

    file_btn = None
    view = None

    def __init__(self):
        super().__init__()

        # 윈도우 세팅
        width, height = monitor.get_size()
        self.setWindowTitle(TITLE_WINDOW)
        self.setGeometry(0, 0, width / 2, height / 2)

        # UI 초기화
        self.ui_setup()

    def ui_setup(self):
        print('ui_setup')

        # 전체폼 박스
        form_box = QHBoxLayout()

        # 레이아웃 박스
        _left = QVBoxLayout()
        _right = QVBoxLayout()

        # 위젯: 파일 열기, 뷰에 이미지 보이기
        self.file_btn = QPushButton(TOOL_OPEN)
        self.file_btn.clicked.connect(self.fileButtonClicked)

        # 그리기 뷰
        self.view = DrawView(self)

        # 박스에 위젯 넣기
        _left.addWidget(self.file_btn)
        _right.addWidget(self.view)

        # 전체 폼박스에 배치
        form_box.addLayout(_left)
        form_box.addLayout(_right)
        form_box.setStretchFactor(_left, 0)
        form_box.setStretchFactor(_right, 1)

        # 레이아웃에 폼박스 등록
        self.setLayout(form_box)
        self.show()

    def fileButtonClicked(self):
        file_name = QFileDialog.getOpenFileName(self)
        path = f'{file_name[0]}'
        img = QPixmap(path)
        self.view.pix_map.setPixmap(img)
        self.view.repaint()
