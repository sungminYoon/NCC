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
PROPERTY_RANGE = 'Lv range       '
PROPERTY_START = 'Lv start       '
PROPERTY_WINDOW = 'Lv window     '
PROPERTY_BONE = 'Lv bone         '
PROPERTY_UNIT = 'Lv unit         '
PROPERTY_OVER = 'Lv overwrite    '


class Menu(QVBoxLayout):

    call_scroll = None              # call_back 객체 입니다. 스크롤 데이터를 생성 또는 가지고 옵니다.
    call_export = None              # call_back 객체 입니다. mask 이미지를 2진 바이너리 데이터로 내보냅니다.
    call_open_path = None           # call_back 객체 입니다. 사용자 지정 파일경로를 가지고 옵니다.
    call_threshold = None           # call_back 객체 입니다. threshold 값을 업데이트 합니다.
    call_max = None                 # call_back 객체 입니다. threshold MAX 값을 업데이트 합니다.
    call_min = None                 # call_back 객체 입니다. threshold MIN 값을 업데이트 합니다.
    call_range = None               # call_back 객체 입니다. level range 값을 업데이트 합니다.
    call_start = None               # call_back 객체 입니다. level scope 값을 업데이트 합니다.
    call_window = None              # call_back 객체 입니다. level window 값을 업데이트 합니다.
    call_bone = None                # call_back 객체 입니다. level bone 값을 업데이트 합니다.
    call_unit = None                # call_back 객체 입니다. level unit 값을 업데이트 합니다.
    call_over = None                # call_back 객체 입니다. level over 값을 업데이트 합니다.

    file_extension = None           # 선택된 파일 확장자 입니다.

    label_current_image = None      # 현재 선택된 이미지 입니다.
    image_save_path = None          # 이미지 저장 경로 입니다.
    image_start_path = None         # "상대경로" 시작 디렉토리 입니다.

    menu_group = None               # 메뉴 그룹 입니다.
    property_widget = None          # 속성 그룹 입니다.
    img_btn = None                  # dicom 폴더의 모든 dicom 에서 이미지를 꺼내 png 로 변환 합니다.
    load_btn = None                 # png 폴더의 모든 이미지를 스크롤에 불러 옵니다.
    export_btn = None               # 이진 바이너리 데이터로 내보냄

    def __init__(self, parent=None):
        super(Menu, self).__init__(parent)

        self.file_extension = 'jpg'

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

        # 위젯: 선택 된 이미지 (넘버)표시 라벨
        self.label_current_image = QLabel()
        self.label_current_image.setText(TITLE_SELECTION_IMAGE)
        self.label_current_image.setFixedHeight(30)

        # Label property
        self.label_threshold = QLabel()
        self.label_threshold_value = QLabel()
        self.setting_label(self.label_threshold, self.label_threshold_value, TITLE_THRESHOLD)

        self.label_max = QLabel()
        self.label_max_value = QLabel()
        self.setting_label(self.label_max, self.label_max_value, PROPERTY_BOUNDARY)

        self.label_min = QLabel()
        self.label_min_value = QLabel()
        self.setting_label(self.label_min, self.label_min_value, PROPERTY_MIN)

        self.label_range = QLabel()
        self.label_range_value = QLabel()
        self.setting_label(self.label_range, self.label_range_value, PROPERTY_RANGE)

        self.label_start = QLabel()
        self.label_start_value = QLabel()
        self.setting_label(self.label_start, self.label_start_value, PROPERTY_START)

        self.label_window = QLabel()
        self.label_window_value = QLabel()
        self.setting_label(self.label_window, self.label_window_value, PROPERTY_WINDOW)

        self.label_bone = QLabel()
        self.label_bone_value = QLabel()
        self.setting_label(self.label_bone, self.label_bone_value, PROPERTY_BONE)

        self.label_unit = QLabel()
        self.label_unit_value = QLabel()
        self.setting_label(self.label_unit, self.label_unit_value, PROPERTY_UNIT)

        self.label_over = QLabel()
        self.label_over_value = QLabel()
        self.setting_label(self.label_over, self.label_over_value, PROPERTY_OVER)

        # LineEdit
        self.threshold_input = QLineEdit()
        self.setting_line_edit(self.threshold_input)

        self.max_input = QLineEdit()
        self.setting_line_edit(self.max_input)

        self.min_input = QLineEdit()
        self.setting_line_edit(self.min_input)

        self.range_input = QLineEdit()
        self.setting_line_edit(self.range_input)

        self.start_input = QLineEdit()
        self.setting_line_edit(self.start_input)

        self.window_input = QLineEdit()
        self.setting_line_edit(self.window_input)

        self.bone_input = QLineEdit()
        self.setting_line_edit(self.bone_input)

        self.unit_input = QLineEdit()
        self.setting_line_edit(self.unit_input)

        self.over_input = QLineEdit()
        self.setting_line_edit(self.over_input)

        # background-color
        self.label_current_image.setStyleSheet("background-color: lightYellow")
        self.threshold_input.setStyleSheet("background-color: lightBlue")

        self.ui_setup()

    def default_setting(self, _threshold, _max, _min, _range, _start, _window, _bone, _unit, _over):

        # 텍스트 상자 표시
        self.label_threshold_value.setText(f'{_threshold}')     # 현재 threshold 값을 표시합니다.
        self.label_max_value.setText(f'{_max}')                 # Threshold 최대 넓이 표시
        self.label_min_value.setText(f'{_min}')                 # Threshold 최소 넓이 표시
        self.label_range_value.setText(f'{_range}')             # 레벨 탐색 범위를 지정합니다.
        self.label_start_value.setText(f'{_start}')             # 레빌 시작 시점을 지정합니다.
        self.label_window_value.setText(f'{_window}')
        self.label_bone_value.setText(f'{_bone}')
        self.label_unit_value.setText(f'{_unit}')
        self.label_over_value.setText(f'{_over}')

        return _threshold, _max, _min, _range, _start, _window, _bone, _unit, _over

    def setting_label(self, q_label: QLabel, q_value: QLabel, text):
        q_label.setText(text)
        q_label.setFixedHeight(30)
        q_value.setFixedHeight(30)

    def setting_line_edit(self, q_line: QLineEdit):
        q_line.setText('')
        q_line.setAlignment(Qt.AlignRight)
        q_line.returnPressed.connect(self.lineChanged)
        q_line.setFixedWidth(30)

    def ui_setup(self):

        # 레이아웃
        _label_threshold = QHBoxLayout()
        _label_max = QHBoxLayout()
        _label_min = QHBoxLayout()
        _label_range = QHBoxLayout()
        _label_start = QHBoxLayout()
        _label_window = QHBoxLayout()
        _label_bone = QHBoxLayout()
        _label_unit = QHBoxLayout()
        _label_over = QHBoxLayout()

        _property_box = QVBoxLayout()
        _property_box.addLayout(_label_threshold)
        _property_box.addLayout(_label_max)
        _property_box.addLayout(_label_min)
        _property_box.addLayout(_label_range)
        _property_box.addLayout(_label_start)
        _property_box.addLayout(_label_window)
        _property_box.addLayout(_label_bone)
        _property_box.addLayout(_label_unit)
        _property_box.addLayout(_label_over)

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

        _label_range.addWidget(self.label_range, alignment=Qt.AlignLeft)
        _label_range.addWidget(self.label_range_value, alignment=Qt.AlignRight)
        _label_range.addWidget(self.range_input, alignment=Qt.AlignRight)

        _label_start.addWidget(self.label_start, alignment=Qt.AlignLeft)
        _label_start.addWidget(self.label_start_value, alignment=Qt.AlignRight)
        _label_start.addWidget(self.start_input, alignment=Qt.AlignRight)

        _label_window.addWidget(self.label_window, alignment=Qt.AlignLeft)
        _label_window.addWidget(self.label_window_value, alignment=Qt.AlignRight)
        _label_window.addWidget(self.window_input, alignment=Qt.AlignRight)

        _label_bone.addWidget(self.label_bone, alignment=Qt.AlignLeft)
        _label_bone.addWidget(self.label_bone_value, alignment=Qt.AlignRight)
        _label_bone.addWidget(self.bone_input, alignment=Qt.AlignRight)

        _label_unit.addWidget(self.label_unit, alignment=Qt.AlignLeft)
        _label_unit.addWidget(self.label_unit_value, alignment=Qt.AlignRight)
        _label_unit.addWidget(self.unit_input, alignment=Qt.AlignRight)

        _label_over.addWidget(self.label_over, alignment=Qt.AlignLeft)
        _label_over.addWidget(self.label_over_value, alignment=Qt.AlignRight)
        _label_over.addWidget(self.over_input, alignment=Qt.AlignRight)

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
            img_folder = file_manager.create_folder_img(self.image_save_path)
            convert.dicom_imageToImg(dicom_folder, img_folder, self.file_extension)
            print('DICOM 파일에서', {self.file_extension}, '파일 내보내기 완료!')

            # 0.1초 delay 후
            time.sleep(0.1)

            # 썸내일 이미지 만들기
            self.check_thumbnail(img_folder)

            # Window 메소드를 호출하여 scroll 에 경로 데이터를 보냅니다.
            call_data = self.call_scroll
            call_data(img_folder, self.file_extension)
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

        # Window 메소드를 호출하여 scroll 에 경로 데이터를 보냅니다.
        call_data = self.call_scroll
        call_data(image_folder, chioce)

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

        if self.range_input.text() is '':
            t_range = self.label_range_value.text()
        else:
            t_range = self.range_input.text()

        if self.start_input.text() is '':
            t_start = self.label_start_value.text()
        else:
            t_start = self.start_input.text()

        if self.window_input.text() is '':
            t_window = self.label_window_value.text()
        else:
            t_window = self.window_input.text()

        if self.bone_input.text() is '':
            t_bone = self.label_bone_value.text()
        else:
            t_bone = self.bone_input.text()

        if self.unit_input.text() is '':
            t_unit = self.label_unit_value.text()
        else:
            t_unit = self.unit_input.text()

        if self.over_input.text() is '':
            t_over = self.label_over_value.text()
        else:
            t_over = self.over_input.text()

        self.label_threshold_value.setText(t_value)
        self.label_max_value.setText(t_max)
        self.label_min_value.setText(t_min)
        self.label_range_value.setText(t_range)
        self.label_start_value.setText(t_start)
        self.label_window_value.setText(t_window)
        self.label_bone_value.setText(t_bone)
        self.label_unit_value.setText(t_unit)
        self.label_over_value.setText(t_over)

        # view 의 threshold 값을 업데이트 합니다.
        call_threshold = self.call_threshold
        call_max = self.call_max
        call_min = self.call_min
        call_range = self.call_range
        call_start = self.call_start
        call_window = self.call_window
        call_bone = self.call_bone
        call_unit = self.call_unit
        call_over = self.call_over

        # 콜백 메소드로 값을 넘깁니다.
        call_threshold(t_value)
        call_max(t_max)
        call_min(t_min)
        call_range(t_range)
        call_start(t_start)
        call_window(t_window)
        call_bone(t_bone)
        call_unit(t_unit)
        call_over(t_over)

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

