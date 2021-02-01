"""
Created by SungMin Yoon on 2020-04-27..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import os
import time
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from TDD.common.util import convert
from TDD.common.util import thumbnail
from TDD.common.util import notice
from TDD.common.path import file_manager
from TDD.common.error import check
from TDD.common.error import messages


TITLE = 'File menu'
TITLE_THRESHOLD = 'Threshold value'
TITLE_IMG_DICOM = 'DICOM all change'
TITLE_IMG_LOAD = 'Load image'
TITLE_EXPORT = 'Export ROI'
TITLE_SELECTION_IMAGE = 'No select image'
TITLE_PROPERTY = 'Property'
PROPERTY_BOUNDARY = 'Boundary multiply'
PROPERTY_MIN = 'Minimum size'

IMAGE_EXTENSION = 'jpg'


class Menu(QVBoxLayout):

    call_scroll = None              # call_back 객체 입니다. 스크롤 데이터를 생성 또는 가지고 옵니다.
    call_export = None              # call_back 객체 입니다. mask 이미지를 2진 바이너리 데이터로 내보냅니다.
    call_open_path = None           # call_back 객체 입니다. 사용자 지정 파일경로를 가지고 옵니다.
    call_threshold = None           # call_back 객체 입니다. threshold 값을 업데이트 합니다.
    call_max = None                 # call_back 객체 입니다. threshold MAX 값을 업데이트 합니다.
    call_min = None                 # call_back 객체 입니다. threshold MIN 값을 업데이트 합니다.

    image_save_path = None          # 이미지 저장 경로 입니다.
    image_start_path = None         # "상대경로" 시작 디렉토리 입니다.

    menu_group = None               # 메뉴 그룹 입니다.
    property_widget = None           # 속성 그룹 입니다.
    img_btn = None                  # dicom 폴더의 모든 dicom 에서 이미지를 꺼내 png 로 변환 합니다.
    load_btn = None                 # png 폴더의 모든 이미지를 스크롤에 불러 옵니다.
    export_btn = None               # 이진 바이너리 데이터로 내보냄

    label_threshold = None          # 'Threshold'
    label_threshold_value = None    # 현재 threshold 값을 표시합니다.
    label_max_value = None          # Threshold 최대 넓이 표시
    label_min_value = None          # Threshold 최소 넓이 표시
    label_current_image = None      # 현재 선택된 이미지 입니다.
    label_max = None
    label_min = None

    threshold_input = None  # 사용자 입력 threshold 값 입니다.
    max_input = None
    min_input = None

    def __init__(self, parent=None):
        super(Menu, self).__init__(parent)

        # Title label
        title_label = QLabel()
        title_label.setText(TITLE)
        title_label.setStyleSheet("background-color: lightGreen")
        self.addWidget(title_label, alignment=Qt.AlignLeft)

        # 위젯: DICOM 파일에서 사진 파일 꺼내기
        self.img_btn = QPushButton(TITLE_IMG_DICOM)
        self.img_btn.clicked.connect(self.changButtonClicked)

        # 위젯: PNG 폴더 불러오기 버튼
        self.load_btn = QPushButton(TITLE_IMG_LOAD)
        self.load_btn.clicked.connect(self.loadButtonClicked)

        # 위젯: 내보내기 버튼
        self.export_btn = QPushButton(TITLE_EXPORT)
        self.export_btn.clicked.connect(self.exportButtonClicked)

        # 위젯: 속성 버튼
        self.property_btn = QPushButton(TITLE_PROPERTY)
        self.property_btn.clicked.connect(self.propertyButtonClicked)

        # Label
        self.label_threshold = QLabel()
        self.label_threshold.setText(TITLE_THRESHOLD)
        self.label_threshold.setFixedHeight(30)

        self.label_threshold_value = QLabel()
        self.label_threshold_value.setFixedHeight(30)

        self.label_max = QLabel()
        self.label_max.setText(PROPERTY_BOUNDARY)
        self.label_max.setFixedHeight(30)

        self.label_max_value = QLabel()
        self.label_max_value.setFixedHeight(30)

        self.label_min = QLabel()
        self.label_min.setText(PROPERTY_MIN)
        self.label_min.setFixedHeight(30)

        self.label_min_value = QLabel()
        self.label_min_value.setFixedHeight(30)

        self.label_current_image = QLabel()
        self.label_current_image.setText(TITLE_SELECTION_IMAGE)
        self.label_current_image.setFixedHeight(30)

        # LineEdit
        self.threshold_input = QLineEdit()
        self.threshold_input.setText('')
        self.threshold_input.setAlignment(Qt.AlignRight)
        self.threshold_input.returnPressed.connect(self.lineChanged)
        self.threshold_input.setFixedWidth(30)

        self.max_input = QLineEdit()
        self.max_input.setText('')
        self.max_input.setAlignment(Qt.AlignRight)
        self.max_input.returnPressed.connect(self.lineChanged)
        self.max_input.setFixedWidth(30)

        self.min_input = QLineEdit()
        self.min_input.setText('')
        self.min_input.setAlignment(Qt.AlignRight)
        self.min_input.returnPressed.connect(self.lineChanged)
        self.min_input.setFixedWidth(30)

        # background-color
        self.label_current_image.setStyleSheet("background-color: lightYellow")
        self.threshold_input.setStyleSheet("background-color: lightBlue")

        # 레이아웃
        _label_threshold = QHBoxLayout()
        _label_max = QHBoxLayout()
        _label_min = QHBoxLayout()
        _property_box = QVBoxLayout()
        _property_box.addLayout(_label_threshold)
        _property_box.addLayout(_label_max)
        _property_box.addLayout(_label_min)

        # 위젯 위치 정렬
        _label_threshold.addWidget(self.label_threshold, alignment=Qt.AlignLeft)
        _label_threshold.addWidget(self.label_threshold_value, alignment=Qt.AlignRight)
        _label_threshold.addWidget(self.threshold_input, alignment=Qt.AlignRight)

        _label_max.addWidget(self.label_max, alignment=Qt.AlignLeft)
        _label_max.addWidget(self.label_max_value, alignment=Qt.AlignRight)
        _label_max.addWidget(self.max_input, alignment=Qt.AlignRight)

        _label_min.addWidget(self.label_min, alignment=Qt.AlignLeft)
        _label_min.addWidget(self.label_min_value, alignment=Qt.AlignRight)
        _label_min.addWidget(self.min_input, alignment=Qt.AlignRight)

        # 위젯: 그룹
        self.menu_group = QVBoxLayout()
        self.menu_group.addWidget(self.img_btn)
        self.menu_group.addWidget(self.load_btn)
        self.menu_group.addWidget(self.export_btn)
        self.menu_group.addWidget(self.property_btn)
        self.menu_group.addWidget(self.label_current_image)

        self.property_widget = QWidget()
        self.property_widget.setLayout(_property_box)
        self.property_widget.hide()
        self.menu_group.addWidget(self.property_widget)

        self.addLayout(self.menu_group)

    def exportButtonGreenColor(self):
        print('menu: exportButtonGreenColor')
        self.export_btn.setStyleSheet('background-color: lightGreen')

    def exportButtonGrayColor(self):
        print('menu: exportButtonGrayColor')
        self.export_btn.setStyleSheet('background-color: lightGray')

    def changeLabel(self, text):
        print('call Menu: changeLabel')
        self.label_current_image.setText(text)

    # mark - Event method
    def changButtonClicked(self):
        print('call Menu: changButtonClicked')

        # 사용자가 선택한 파일경로
        call_file = self.call_open_path
        file_path = call_file()

        if file_path is 0:
            return

        # 사용자가 선택한 파일이름
        last_name = file_path[file_path.rfind('/') + 1:]

        # 파일이름의 경로 폴더명
        dicom_folder = file_path.replace(last_name, '', 1)

        notice.message('messages..', '아래 Yes 를 누르면 파일 변환을 시작합니다. 잠시만 기다려 주세요...')

        if check.extension_dicom(dicom_folder):
            # 폴더에 들어 있는 DICOM 에서 PNG 파일 내보내기
            img_folder = file_manager.create_folder_img(self.image_save_path, Menu.IMAGE_EXTENSION)
            roi_folder = file_manager.create_folder_roi(img_folder)
            convert.dicom_imageToImg(dicom_folder, img_folder, Menu.IMAGE_EXTENSION)
            print('DICOM 파일에서', {Menu.IMAGE_EXTENSION}, '파일 내보내기 완료!')

            # 0.1초 delay 후
            time.sleep(0.1)

            # 썸내일 이미지 만들기
            self.check_thumbnail(img_folder)

            # roi 폴더의 mask 파일 리스트
            roi_list = file_manager.find_png_list(roi_folder)
            time.sleep(0.1)

            # Window 메소드를 호출하여 scroll 에 경로 데이터를 보냅니다.
            call_data = self.call_scroll
            call_data(img_folder, roi_list)
        else:
            notice.message('Error', messages.ERROR_DICOM)
            return

        notice.message('messages..', '파일 변환이 완료 되었습니다. 아래 Yes 를 눌러 주세요!')

    # mark - Event method
    def loadButtonClicked(self):
        print('call Menu: loadButtonClicked')
        # 사용자가 선택한 파일경로
        call_file = self.call_open_path
        file_path = call_file()

        if file_path is 0:
            return

        # 사용자가 선택한 파일이름
        last_name = file_path[file_path.rfind('/') + 1:]
        _, fileExtension = os.path.splitext(last_name)
        image_folder = file_path.replace(last_name, '', 1)

        # 확장자 확인
        chioce = fileExtension

        # 썸내일 이미지 만들기
        self.check_thumbnail(image_folder)

        # roi 폴더의 mask 파일 리스트
        path = f'{image_folder}thumbnail'
        image_list = file_manager.find_png_list(path)
        time.sleep(0.1)

        # Window 메소드를 호출하여 scroll 에 경로 데이터를 보냅니다.
        call_data = self.call_scroll
        call_data(image_folder, image_list, chioce)

    # mark - Event method
    def exportButtonClicked(self):
        print('call Menu: exportButtonClicked')
        call = self.call_export
        call()

    # mark - Event method
    def propertyButtonClicked(self):
        print('call Menu: propertyButtonClicked')

        if self.property_widget.isHidden():
            self.property_widget.show()
        else:
            self.property_widget.hide()

        # call = self.call_property
        # call()

    # mark - Event method
    def lineChanged(self):
        # 라벨값을 텍스트 입력값으로 변경
        print('call Menu: lineChanged')

        if self.threshold_input.text() is '':
            t_value = self.label_threshold_value.text()
        else:
            t_value = self.threshold_input.text()

        if self.max_input.text() is '':
            t_max = self.label_max_value.text()
        else:
            t_max = self.max_input.text()

        if self.min_input.text() is '':
            t_min = self.label_min_value.text()
        else:
            t_min = self.min_input.text()

        self.label_threshold_value.setText(t_value)
        self.label_max_value.setText(t_max)
        self.label_min_value.setText(t_min)

        # view 의 threshold 값을 업데이트 합니다.
        call_threshold = self.call_threshold
        call_max = self.call_max
        call_min = self.call_min

        call_threshold(t_value)
        call_max(t_max)
        call_min(t_min)

    # 썸내일 이미지 만들기
    @classmethod
    def check_thumbnail(cls, image_folder):
        print('call Menu: check_thumbnail')
        path = f'{image_folder}thumbnail'
        if not (os.path.isdir(path)):
            thumbnail.img_toThumbnail(image_folder, 'jpg')
            print('썸네일 이미지 만들기 완료!')
            time.sleep(0.1)
        else:
            print('썸네일 폴더가 이미 존재 합니다.')

