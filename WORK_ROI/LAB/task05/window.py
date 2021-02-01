"""
Created by SungMin Yoon on 2019-12-17..
Copyright (c) 2019 year SungMin Yoon. All rights reserved.
"""
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from LAB.common.util import convert
from LAB.task05.view import View
from LAB.task05.tool import Tool

IMAGE_SAVE_PATH = 'LAB/image/'
TITLE_WINDOW = 'ROI TOOL'
TITLE_DICOM_PNG = 'DICOM all change png'
TITLE_IMAGE_OPEN = 'Image open'
TITLE_SELECTION_SAVE = 'Selection save'
TITLE_ZIP_LOAD = 'Load ROI'
WINDOW_SIZE_WIDTH = 712
WINDOW_SIZE_HEIGHT = 600


class Window(QWidget):

    png_btn = None              # 다이콤 파일에서 사진 파일을 꺼내 옵니다.
    file_btn = None             # 이미지 불러오기 버튼 맨버 입니다.
    save_btn = None             # selection 된 영역을 저장하는 버튼 입니다.
    load_btn = None             # zip 파일을 불러 옵니다.
    view = None                 # 이미지 편집 뷰 입니다
    tool = None                 # 윈도우 도구 버튼들 입니다.
    label_title = None          # 'Threshold'
    label_threshold = None      # 현재 threshold 값을 표시합니다.
    text_input = None           # 사용자 입력 threshold 값 입니다.

    def __init__(self):
        super().__init__()

        # 윈도우 세팅
        self.setWindowTitle(TITLE_WINDOW)
        self.setGeometry(0, 0, WINDOW_SIZE_WIDTH, WINDOW_SIZE_HEIGHT)

        # 위젯: DICOM 파일에서 사진 파일 꺼내기
        self.png_btn = QPushButton(TITLE_DICOM_PNG)
        self.png_btn.clicked.connect(self.pngButtonClicked)

        # 위젯: 파일 열기 뷰에 이미지 보이기
        self.file_btn = QPushButton(TITLE_IMAGE_OPEN)
        self.file_btn.clicked.connect(self.fileButtonClicked)

        # 위젯: selection 영역 저장 버튼
        self.save_btn = QPushButton(TITLE_SELECTION_SAVE)
        self.save_btn.clicked.connect(self.saveButtonClicked)

        # 위젯: ZIP 파일 불러오기
        self.load_btn = QPushButton(TITLE_ZIP_LOAD)
        self.load_btn.clicked.connect(self.loadButtonClicked)

        # 그리기 뷰 와 툴 로드
        self.view = View(self)
        self.tool = Tool()

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
        _left.addWidget(self.png_btn)
        _left.addWidget(self.file_btn)
        _left.addWidget(self.save_btn)
        _left.addWidget(self.load_btn)
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
    def pngButtonClicked(self):
        print('Window: photoButtonClicked')
        full_path = QFileDialog.getOpenFileName(self)
        file_path = f'{full_path[0]}'

        # 사용자가 선택한 파일이름
        last_name = file_path[file_path.rfind('/') + 1:]

        # 파일이름의 경로 폴더명
        source_folder = file_path.replace(last_name, '', 1)

        # 폴더에 들어 있는 DICOM 에서 PNG 파일 내보내기
        convert.dicom_imageToImg(source_folder, IMAGE_SAVE_PATH)
        print('DICOM 파일에서 PNG 파일 내보내기 완료!')

    def fileButtonClicked(self):
        print('Window: fileButtonClicked')
        full_path = QFileDialog.getOpenFileName(self)
        path = f'{full_path[0]}'

        # 보여지는 view 에 들어갈 이미지 입니다.
        img = QPixmap(path)

        # Open cv 를 위한 상대 경로를 만들어 줍니다.
        file_name = os.path.basename(path)
        image_path = f'{IMAGE_SAVE_PATH}{file_name}'

        # 보여지는 view 에 이미지를 넣어 주고
        self.view.q_graphic.setPixmap(img)
        self.view.repaint()
        self.view.re_setting(image_path)

    def saveButtonClicked(self):
        print('Window: saveButtonClicked')
        ori, mask, zipfile = self.tool.get_image_path(IMAGE_SAVE_PATH)

        # 이미지 저장과 압축
        self.view.save_image(ori, mask)
        self.tool.image_compression(ori, mask, zipfile)

    def loadButtonClicked(self):
        print('Window: loadButtonClicked')
        full_path = QFileDialog.getOpenFileName(self)
        file_path = f'{full_path[0]}'

        # zip 파일의 경로와 이름을 가져옵니다.
        load_path, ori_name, mask_name = self.tool.load_zip(file_path, IMAGE_SAVE_PATH)
        ori_path = f'{load_path}{ori_name}'
        mask_path = f'{load_path}{mask_name}'

        # 이미지 파일을 불러오고
        img = QPixmap(ori_path)

        # View 에 보여질 이미지 장착
        self.view.q_graphic.setPixmap(img)

        # 수정될 이미지 장착
        self.view.re_setting(ori_path)

        # 마스크 이미지 장착
        self.view.set_mask(mask_path)

    # 라벨값을 텍스트 입력값으로 변경
    def lineChanged(self):
        print('Window: lineChanged')
        self.label_threshold.setText(self.text_input.text())
        self.view.threshold = int(self.text_input.text())
        print(self.view.threshold)

