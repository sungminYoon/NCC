"""
Created by SungMin Yoon on 2020-04-27..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import time
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from TDD.common.util import convert
from TDD.common.util import thumbnail
from TDD.common.path import file_manager

TITLE = 'File Menu'
TITLE_DICOM_PNG = 'DICOM all change png'
TITLE_PNG_LOAD = 'Load PNG'
TITLE_SELECTION_SAVE = 'Save ROI'
TITLE_SELECTION_IMAGE = 'No select image'


class Menu(QVBoxLayout):

    call_scroll = None              # call_back 객체 입니다. 스크롤 데이터를 생성 또는 가지고 옵니다.
    call_save = None                # call_back 객체 입니다. 프로바이더 DATA 객체에 활성화된 mask 이미지 경로를 저장합니다.
    call_open_path = None           # call_back 객체 입니다. 사용자 지정 파일을 경로를 가지고 옵니다.
    call_activation = None          # call_back 객체 입니다. view 에서 mask 활성화된 이미지 경로를 가지고 옵니다.
    call_threshold = None           # call_back 객체 입니다. threshold 값을 업데이트 합니다.

    image_save_path = None          # 이미지가 저장될 경로 입니다.
    image_start_path = None         # "상대경로"를 만들기 위한 경로 시작 디렉토리 입니다.

    png_btn = None                  # dicom 폴더의 모든 dicom 에서 이미지를 꺼내 png 로 변환 합니다.
    load_btn = None                 # png 폴더의 모든 이미지를 스크롤에 불러 옵니다.
    save_btn = None                 # selection 된 영역을 저장하는 버튼 입니다.

    label_title = None              # 'Threshold'
    label_threshold = None          # 현재 threshold 값을 표시합니다.
    label_current_image = None      # 현재 선택된 이미지 입니다.
    text_input = None               # 사용자 입력 threshold 값 입니다.

    def __init__(self, parent=None):
        super(Menu, self).__init__(parent)

        # Title label
        title_label = QLabel()
        title_label.setText(TITLE)
        title_label.setStyleSheet("background-color: lightGreen")
        self.addWidget(title_label, alignment=Qt.AlignLeft)

        # 위젯: DICOM 파일에서 사진 파일 꺼내기
        self.png_btn = QPushButton(TITLE_DICOM_PNG)
        self.png_btn.clicked.connect(self.changButtonClicked)

        # 위젯: PNG 폴더 불러오기 버튼
        self.load_btn = QPushButton(TITLE_PNG_LOAD)
        self.load_btn.clicked.connect(self.loadButtonClicked)

        # 위젯: selection 영역 저장 버튼
        self.save_btn = QPushButton(TITLE_SELECTION_SAVE)
        self.save_btn.clicked.connect(self.saveButtonClicked)

        # Label
        self.label_title = QLabel()
        self.label_title.setText('Threshold')
        self.label_title.setFixedHeight(30)

        self.label_threshold = QLabel()
        self.label_threshold.setText('5')
        self.label_threshold.setFixedHeight(30)

        self.label_current_image = QLabel()
        self.label_current_image.setText(TITLE_SELECTION_IMAGE)
        self.label_current_image.setFixedHeight(30)

        # LineEdit
        self.text_input = QLineEdit()
        self.text_input.setText('')
        self.text_input.setAlignment(Qt.AlignRight)
        self.text_input.returnPressed.connect(self.lineChanged)

        # background-color
        self.label_title.setStyleSheet("background-color: lightYellow")
        self.label_threshold.setStyleSheet("background-color: lightPink")
        self.text_input.setStyleSheet("background-color: lightBlue")

        # 레이아웃
        _label = QHBoxLayout()
        _text = QHBoxLayout()

        # 박스에 위젯 넣기
        self.addWidget(self.png_btn)
        self.addWidget(self.load_btn)
        self.addWidget(self.save_btn)

        # 위젯 위치 정렬
        _label.addWidget(self.label_current_image, alignment=Qt.AlignTop)
        _label.addWidget(self.label_title, alignment=Qt.AlignLeft)
        _label.addWidget(self.label_threshold, alignment=Qt.AlignRight)
        _text.addWidget(self.text_input, alignment=Qt.AlignTop)

        self.addLayout(_label)
        self.addLayout(_text)

    def changeLabel(self, text):
        print('Window: changeLabel')
        self.label_current_image.setText(text)

    # mark - Event method
    def changButtonClicked(self):
        print('Window: pngButtonClicked')
        # 사용자가 선택한 파일경로
        call_file = self.call_open_path
        file_path = call_file()

        # 사용자가 선택한 파일이름
        last_name = file_path[file_path.rfind('/') + 1:]

        # 파일이름의 경로 폴더명
        dicom_folder = file_path.replace(last_name, '', 1)

        # 폴더에 들어 있는 DICOM 에서 PNG 파일 내보내기
        png_folder = file_manager.create_folder_img(self.image_save_path)
        roi_folder = file_manager.create_folder_roi(png_folder)
        convert.dicom_imageToImg(dicom_folder, png_folder)
        print('DICOM 파일에서 PNG 파일 내보내기 완료!')

        # 0.1초 delay 후
        time.sleep(0.1)

        # 썸내일 이미지 만들기
        thumbnail.img_toThumbnail(png_folder)
        print('썸네일 이미지 만들기 완료!')
        time.sleep(0.1)

        # roi 폴더의 mask 파일 리스트
        roi_list = file_manager.find_png_list(roi_folder)
        time.sleep(0.1)

        # Window 메소드를 호출하여 scroll 에 경로 데이터를 보냅니다.
        call_data = self.call_scroll
        call_data(png_folder, roi_list)

    # mark - Event method
    def loadButtonClicked(self):
        print('Window: loadButtonClicked')
        # 사용자가 선택한 파일경로
        call_file = self.call_open_path
        file_path = call_file()

        # 사용자가 선택한 파일이름
        last_name = file_path[file_path.rfind('/') + 1:]
        png_folder = file_path.replace(last_name, '', 1)
        roi_folder = file_manager.create_folder_roi(png_folder)
        time.sleep(0.1)

        # roi 폴더의 mask 파일 리스트
        roi_list = file_manager.find_png_list(roi_folder)
        time.sleep(0.1)

        # Window 메소드를 호출하여 scroll 에 경로 데이터를 보냅니다.
        call_data = self.call_scroll
        call_data(png_folder, roi_list)

    # mark - Event method
    def saveButtonClicked(self):
        print('Window: saveButtonClicked')
        call_path = self.call_activation
        activation_path = call_path()

        # Open cv 를 위한 "상대경로" 를 만들어 줍니다.
        image_path = file_manager.relative_path(activation_path, self.image_start_path)

        # 마스크 이미지 저장 "절대경로"
        mask_path = file_manager.get_roi_path(image_path)

        # Window 메소드를 호출 하여 마스크를 저장합니다.
        call = self.call_save
        call(mask_path)

    # mark - Event method
    def lineChanged(self):
        # 라벨값을 텍스트 입력값으로 변경
        print('Window: lineChanged')
        self.label_threshold.setText(self.text_input.text())

        # view 의 threshold 값을 업데이트 합니다.
        call = self.call_threshold
        call(self.text_input.text())

