"""
Created by SungMin Yoon on 2019-12-17..
Copyright (c) 2019 year SungMin Yoon. All rights reserved.
"""
import os
import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from TDD.common.path import file_manager
from TDD.common.util import convert
from TDD.common.util import thumbnail
from TDD.task06.view.main_view import View
from TDD.task06.view.mounting import Mounting
from TDD.task06.provider import Provider


IMAGE_SAVE_PATH = 'TDD/image/'
IMAGE_START_PATH = 'TDD'
TITLE_WINDOW = 'ROI TOOL'
TITLE_DICOM_PNG = 'DICOM all change png'
TITLE_PNG_LOAD = 'Load PNG'
TITLE_SELECTION_SAVE = 'Save ROI'
WINDOW_SIZE_WIDTH = 712
WINDOW_SIZE_HEIGHT = 600


class Window(QWidget):

    view_event = None           # 뷰 이벤트 (call_back 객체 입니다.)
    view = None                 # 이미지 편집 뷰 입니다

    png_btn = None              # dicom 폴더의 모든 dicom 에서 이미지를 꺼내 png 로 변환 합니다.
    load_btn = None             # png 폴더의 모든 이미지를 스크롤에 불러 옵니다.
    save_btn = None             # selection 된 영역을 저장하는 버튼 입니다.
    scroll = None               # 스크롤
    mounting = None             # 스크롤 장착될 내용
    label_title = None          # 'Threshold'
    label_threshold = None      # 현재 threshold 값을 표시합니다.
    text_input = None           # 사용자 입력 threshold 값 입니다.
    provider = None             # 데이터 관리
    activation_path = None      # 현재 뷰에 활성화된 이미지 경로

    def __init__(self):
        super().__init__()

        # 뷰 이벤트 메서드 등록
        self.view_event = self.reSetting

        # 윈도우 세팅
        self.setWindowTitle(TITLE_WINDOW)
        self.setGeometry(0, 0, WINDOW_SIZE_WIDTH, WINDOW_SIZE_HEIGHT)

        # 위젯: DICOM 파일에서 사진 파일 꺼내기
        self.png_btn = QPushButton(TITLE_DICOM_PNG)
        self.png_btn.clicked.connect(self.pngButtonClicked)

        # 위젯: PNG 폴더 불러오기 버튼
        self.load_btn = QPushButton(TITLE_PNG_LOAD)
        self.load_btn.clicked.connect(self.loadButtonClicked)

        # 위젯: selection 영역 저장 버튼
        self.save_btn = QPushButton(TITLE_SELECTION_SAVE)
        self.save_btn.clicked.connect(self.saveButtonClicked)

        # 스크롤에 버튼 장착
        self.scroll = QScrollArea()
        self.mounting = Mounting()
        self.mounting.call_back = self.view_event

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

        # 그리기 뷰 와 툴 로드
        self.view = View(self)

        # 공급자 생성
        self.provider = Provider()

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
        _left.addWidget(self.load_btn)
        _left.addWidget(self.save_btn)
        _label.addWidget(self.label_title, alignment=Qt.AlignLeft)
        _label.addWidget(self.label_threshold, alignment=Qt.AlignRight)
        _text.addWidget(self.text_input, alignment=Qt.AlignTop)
        _left.addLayout(_label)
        _left.addLayout(_text)

        _left.addWidget(self.scroll)
        _right.addWidget(self.view)

        # 전체 폼박스에 배치
        form_box.addLayout(_left)
        form_box.addLayout(_right)
        form_box.setStretchFactor(_left, 0)
        form_box.setStretchFactor(_right, 1)

        # 레이아웃에 폼박스 등록
        self.setLayout(form_box)
        self.show()

    # mark - Event method
    def pngButtonClicked(self):
        print('Window: pngButtonClicked')
        full_path = QFileDialog.getOpenFileName(self)
        file_path = f'{full_path[0]}'

        # 사용자가 선택한 파일이름
        last_name = file_path[file_path.rfind('/') + 1:]

        # 파일이름의 경로 폴더명
        source_folder = file_path.replace(last_name, '', 1)

        # 폴더에 들어 있는 DICOM 에서 PNG 파일 내보내기
        png_folder = file_manager.create_folder_png(IMAGE_SAVE_PATH)
        roi_folder = file_manager.create_folder_roi(png_folder)
        convert.dicom_imageToImg(source_folder, png_folder)
        print('DICOM 파일에서 PNG 파일 내보내기 완료!')

        # 0.1초 delay 후 썸내일 이미지 만들기
        time.sleep(0.1)
        thumbnail.img_toThumbnail(png_folder)
        print('썸네일 이미지 만들기 완료!')

        # 0.1초 delay 후 이미지 주석 data 생성
        time.sleep(0.1)

        # 사용자가 선택한 파일이름
        time.sleep(0.1)
        roi_list = file_manager.find_png_list(roi_folder)

        time.sleep(0.1)
        self.provider.data_create(png_folder, roi_list)

        time.sleep(0.1)
        print('png 이미지의 추가 속성 데이터 생성완료')

        self.mounting.create(self.provider.data_list)
        self.scroll.setWidget(self.mounting.top_widget)

    # mark - Event method
    def loadButtonClicked(self):
        print('Window: loadButtonClicked')
        full_path = QFileDialog.getOpenFileName(self)
        file_path = f'{full_path[0]}'

        # 사용자가 선택한 파일이름
        last_name = file_path[file_path.rfind('/') + 1:]
        png_folder = file_path.replace(last_name, '', 1)
        roi_folder = file_manager.create_folder_roi(png_folder)

        time.sleep(0.1)
        roi_list = file_manager.find_png_list(roi_folder)

        time.sleep(0.1)
        self.provider.data_create(png_folder, roi_list)

        time.sleep(0.1)
        print('png 이미지의 추가 속성 데이터 생성완료')

        self.mounting.create(self.provider.data_list)
        self.scroll.setWidget(self.mounting.top_widget)

        # 생성 데이터 확인
        # print(self.provider.data_read())

    # mark - Event method
    def saveButtonClicked(self):
        print('Window: saveButtonClicked')
        # Open cv 를 위한 상대 경로를 만들어 줍니다.
        image_path = file_manager.relative_path(self.activation_path, IMAGE_START_PATH)

        # 마스크 이미지 저장 경로
        mask_path = file_manager.get_roi_path(image_path)

        # 마스크 이미지 저장과 데이터 등록
        self.view.save_image(mask_path)
        last_name = self.activation_path[self.activation_path.rfind('/') + 1:]
        self.provider.data_update_roi(last_name, mask_path)

        # 스크롤 갱신
        self.mounting.create(self.provider.data_list)
        self.scroll.setWidget(self.mounting.top_widget)

    # mark - Event method
    def lineChanged(self):
        # 라벨값을 텍스트 입력값으로 변경
        print('Window: lineChanged')
        self.label_threshold.setText(self.text_input.text())
        self.view.threshold = int(self.text_input.text())
        print(self.view.threshold)

    # mark -  Event call back method
    def reSetting(self, path):
        print('window: view_resetting', path)
        # 활성화 할 이미지 경로
        self.activation_path = path

        # 보여지는 view 에 들어갈 이미지 입니다.
        img = QPixmap(path)

        # Open cv 를 위한 상대 경로를 만들어 줍니다.
        image_path = file_manager.relative_path(path, IMAGE_START_PATH)

        # 보여지는 view 에 이미지를 넣어 주고
        self.view.q_graphic.setPixmap(img)
        self.view.repaint()
        self.view.re_setting(image_path)

        # roi 폴더에 mask 이미지 "절대경로"를 가져 옵니다.
        roi_path = file_manager.get_roi_path(self.activation_path)

        # roi 폴더 속에 mask 이미지 "상대경로"를 가져 옵니다.
        mask_path = file_manager.relative_path(roi_path, IMAGE_START_PATH)

        # 절대 경로로 roi 폴더에 마스크 이미지 파일이 있는지 확인하고
        # 있다면 마스크 상대 경로를 사용해 화면에 표시합니다.
        if os.path.isfile(roi_path):
            self.view.set_mask(mask_path)
