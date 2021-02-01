"""
Created by SungMin Yoon on 2019-12-17..
Copyright (c) 2019 year SungMin Yoon. All rights reserved.
"""
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from TDD.common.path import file_manager
from TDD.task08.view.main_view import View
from TDD.task08.view.tool import Tool
from TDD.task08.view.menu import Menu
from TDD.task08.view.mounting import Mounting
from TDD.task08.control.provider import Provider
from TDD.task08.control.auto import Auto


TITLE_WINDOW = 'ROI TOOL'
WINDOW_SIZE_WIDTH = 1024
WINDOW_SIZE_HEIGHT = 768
IMAGE_SAVE = 'TDD/image/'
IMAGE_START = 'TDD'
DEFAULT_THRESHOLD = 15


class Window(QWidget):

    auto = None                     # ROI 자동 추출
    view = None                     # 이미지 편집 뷰 입니다
    menu = None                     # 좌측 상단 File Menu 버튼 모음 입니다.
    tool = None                     # 상단 도구 버튼 모음 입니다.
    scroll = None                   # 스크롤
    mounting = None                 # 스크롤 장착될 내용
    provider = None                 # 데이터 공급관리
    active_path = None              # 뷰에 활성화된 이미지 경로
    active_image_index = None       # 뷰에 활성화된 이미지 인덱스 번호

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # 윈도우 세팅
        self.setWindowTitle(TITLE_WINDOW)
        self.setGeometry(0, 0, WINDOW_SIZE_WIDTH, WINDOW_SIZE_HEIGHT)

        # View, Menu, Tool 생성
        self.view = View()
        self.view.setup(WINDOW_SIZE_WIDTH, WINDOW_SIZE_HEIGHT)
        self.view.threshold = DEFAULT_THRESHOLD
        self.menu = Menu()
        self.tool = Tool()

        # 스크롤에 버튼 장착 생성
        self.scroll = QScrollArea()
        self.mounting = Mounting()

        # ROI 자동화 처리 생성
        self.auto = Auto()

        # DATA 공급관리 생성
        self.provider = Provider()

        # 콜백 객체에 Window 메소드를 등록합니다.
        self.menu.call_notice = self.notice
        self.menu.call_scroll = self.scroll_data
        self.menu.call_open_path = self.file_open
        self.menu.call_save = self.mask_save
        self.menu.call_activation = self.get_activation
        self.menu.call_threshold = self.threshold_input

        self.tool.call_data_set = self.data_set
        self.tool.call_algorithm = self.algorithm

        self.mounting.call_back = self.re_setting

        # 이미지 "파일" 저장 경로
        self.menu.image_save_path = IMAGE_SAVE
        self.menu.image_start_path = IMAGE_START

        # ui 설정
        self.ui_setup()

    def ui_setup(self):
        print('ui_setup')

        # 전체폼 박스
        form_box = QHBoxLayout()
        _left = QVBoxLayout()
        _right = QVBoxLayout()

        # left layout
        _left.addLayout(self.menu)
        _left.addWidget(self.scroll)

        # right layout
        _right.addLayout(self.tool)

        # image view 좌측 상단 고정
        self.view.setAlignment(Qt.AlignTop)
        _right.addWidget(self.view, alignment=Qt.AlignLeft)

        # 전체 폼박스에 배치
        form_box.addLayout(_left)
        form_box.addLayout(_right)
        form_box.setStretchFactor(_left, 0)
        form_box.setStretchFactor(_right, 1)

        # 레이아웃에 폼박스 등록
        self.setLayout(form_box)
        self.show()

    # mark -  Call back method: menu
    def get_activation(self):
        return self.active_path

    # mark -  Call back method: menu
    def file_open(self):
        full_path = QFileDialog.getOpenFileName(self)
        file_path = f'{full_path[0]}'
        return file_path

    # mark -  Call back method: menu
    def threshold_input(self, update):
        int_value = int(update)
        self.view.threshold = int_value

    # 마스크 이미지 저장과 데이터 등록
    # mark -  Call back method: menu
    def mask_save(self, mask_path):
        self.view.save_image(mask_path)
        last_name = self.active_path[self.active_path.rfind('/') + 1:]
        self.provider.data_update_roi(last_name, mask_path)

        # 스크롤 갱신
        self.mounting.create(self.provider.info_list)
        self.scroll.setWidget(self.mounting.top_widget)

        # 스크롤 포커스 이동
        v: QScrollBar = self.scroll.verticalScrollBar()
        v.setSliderPosition(500)

    # 공급자 클래스의 데이타 생성
    # mark -  Call back method: menu
    def scroll_data(self, img_folder, roi_list):
        # provider.data_list "데이터 초기화"
        self.provider.info_list = []
        self.provider.create(IMAGE_START, img_folder, roi_list)
        self.provider.data_read()
        self.mounting.create(self.provider.info_list)
        self.scroll.setWidget(self.mounting.top_widget)
        print('Window: 이미지 속성 데이터 생성완료')

    # mark -  Call back method: tool
    def data_set(self):
        dicom_folder = self.file_open()

        if dicom_folder is '':
            return

        self.provider.create_dicom(dicom_folder)

    # mark -  Call back method: tool
    def algorithm(self):
        print('window: algorithm')

        i: int = 0
        for mask in self.view.get_mask_list():
            best_list = self.auto.roi_designation(self.provider.image_container,
                                                  self.active_image_index,
                                                  mask)
            i = i + 1
            print(best_list)

    # mark -  Call back method: mounting
    def re_setting(self, path, index):
        print('window: re_setting', path)
        # 활성화 할 이미지 경로
        self.active_path = path
        self.active_image_index = index
        self.tool.set_select_image(path)

        # 메뉴에 선택된 현재 이미지를 표시 합니다.
        current_image_text = f'Current :{index}'
        self.menu.changeLabel(current_image_text)

        # 보여지는 view 에 들어갈 이미지 입니다.
        img = QPixmap(path)

        # Open cv 를 위한 상대 경로를 만들어 줍니다.
        image_path = file_manager.relative_path(path, IMAGE_START)

        # 보여지는 view 에 이미지를 넣어 주고
        self.view.q_graphic.setPixmap(img)
        self.view.repaint()
        self.view.re_setting(image_path)

        # roi 폴더에 mask 이미지 "절대경로"를 가져 옵니다.
        roi_path = file_manager.get_roi_path(self.active_path)

        # roi 폴더에 mask 이미지 "상대경로"를 가져 옵니다.
        mask_path = file_manager.relative_path(roi_path, IMAGE_START)

        # roi 폴더에 마스크 이미지 파일이 있는지 "절대경로" 확인하고
        # 있다면 마스크 "상대경로"를 사용해 화면에 표시합니다.
        if os.path.isfile(roi_path):
            self.view.set_mask(mask_path)

    # mark -  Call back method: menu, tool
    def notice(self, title, msg):
        print('Window: notice')
        buttonReply = QMessageBox.question(self, title, msg, QMessageBox.Yes)
        if buttonReply == QMessageBox.Yes:
            print('Yes clicked.')

