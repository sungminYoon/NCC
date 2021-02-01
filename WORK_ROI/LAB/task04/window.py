"""
Created by SungMin Yoon on 2019-12-17..
Copyright (c) 2019 year SungMin Yoon. All rights reserved.
"""
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from LAB.task04.draw_view import DrawView

TITLE_WINDOW = 'ROI TOOL'
TITLE_IMAGE_OPEN = 'Image Open'
TITLE_SELECTION_SAVE = 'Selection Save'
WINDOW_SIZE_WIDTH = 600
WINDOW_SIZE_HEIGHT = 600

'''Threshold 한 마스크 이미지를 저장'''


class Window(QWidget):

    file_btn = None             # 이미지 불러오기 버튼 맨버 입니다.
    save_btn = None             # selection 된 영역을 저장하는 버튼 입니다.
    view = None                 # 이미지 편집 뷰 입니다
    label_title = None          # 'Threshold'
    label_threshold = None      # 현재 threshold 값을 표시합니다.
    text_input = None           # 사용자 입력 threshold 값 입니다.

    def __init__(self):
        super().__init__()

        # 윈도우 세팅
        self.setWindowTitle(TITLE_WINDOW)
        self.setGeometry(0, 0, WINDOW_SIZE_WIDTH, WINDOW_SIZE_HEIGHT)

        # 위젯: 파일 열기 뷰에 이미지 보이기
        self.file_btn = QPushButton(TITLE_IMAGE_OPEN)
        self.file_btn.clicked.connect(self.fileButtonClicked)

        # 위젯: selection 영역 저장 버튼
        self.save_btn = QPushButton(TITLE_SELECTION_SAVE)
        self.save_btn.clicked.connect(self.saveButtonClicked)

        # 그리기 뷰
        self.view = DrawView(self)

        # Label
        self.label_title = QLabel("Threshold :", self)
        self.label_title.setFixedHeight(30)
        self.label_threshold = QLabel("0", self)
        self.label_threshold.setFixedHeight(30)

        # LineEdit
        self.text_input = QLineEdit("", self)
        self.text_input.setAlignment(Qt.AlignRight)
        self.text_input.returnPressed.connect(self.lineChanged)

        # background-color
        self.label_title.setStyleSheet("background-color: lightYellow")
        self.label_threshold.setStyleSheet("background-color: lightPink")
        self.text_input.setStyleSheet("background-color: lightBlue")

        # UI 초기화
        string = f'{self.view.threshold}'
        self.label_threshold.setText(string)
        self.ui_setup()

    def ui_setup(self):
        print('ui_setup')

        # 전체폼 박스
        form_box = QHBoxLayout()

        # 레이아웃
        _label = QHBoxLayout()
        _text = QHBoxLayout()
        _left = QVBoxLayout()
        _right = QVBoxLayout()

        # 박스에 위젯 넣기
        _left.addWidget(self.file_btn)
        _left.addWidget(self.save_btn)
        _label.addWidget(self.label_title, alignment=Qt.AlignLeft)
        _label.addWidget(self.label_threshold, alignment=Qt.AlignRight)
        _text.addWidget(self.text_input, alignment=Qt.AlignTop)
        _left.addLayout(_label)
        _left.addLayout(_text)
        _right.addWidget(self.view)

        # 전체 폼박스에 배치
        form_box.addLayout(_left)
        form_box.addLayout(_right)
        form_box.setStretchFactor(_left, 0)
        form_box.setStretchFactor(_right, 1)

        # 레이아웃에 폼박스 등록
        self.setLayout(form_box)
        self.show()

    # MARK: event
    def fileButtonClicked(self):
        file_name = QFileDialog.getOpenFileName(self)
        path = f'{file_name[0]}'
        img = QPixmap(path)
        self.view.q_graphic.setPixmap(img)
        self.view.repaint()
        self.view.tool_init()

    def saveButtonClicked(self):
        print('Window:saveButtonClicked')
        self.view.image_save()

    def lineChanged(self):
        self.label_threshold.setText(self.text_input.text())
        self.view.threshold = int(self.text_input.text())
        print(self.view.threshold)

