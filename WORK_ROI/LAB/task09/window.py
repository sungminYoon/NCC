"""
Created by SungMin Yoon on 2019-12-17..
Copyright (c) 2019 year SungMin Yoon. All rights reserved.
"""
import os
import math
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from LAB.common.path import file_manager
from LAB.common.util import img_text
from LAB.common.util import notice
from LAB.task09.view.main_view import View
from LAB.task09.view.tool import Tool
from LAB.task09.view.menu import Menu
from LAB.task09.view.table_mounting import TableMounting
from LAB.task09.view.table_confirmation import TableConfirmation
from LAB.task09.control.provider import Provider
from LAB.task09.control.auto import Auto
from LAB.common.util.img_merge import Merge


WINDOW_SIZE_WIDTH = 800
WINDOW_SIZE_HEIGHT = 700
DEFAULT_THRESHOLD = 10
DEFAULT_THRESHOLD_MAX = '3'
DEFAULT_THRESHOLD_MIN = '20'
TITLE_WINDOW = 'ROI TOOL'
IMAGE_SAVE = 'LAB/image/'
IMAGE_START = 'LAB'


class Window(QWidget):

    auto = None                    # ROI 자동 추출
    view = None                    # 화면에 보여지는 이미지 뷰 입니다
    menu = None                    # 좌측 상단 File Menu 버튼 모음 입니다.
    tool = None                    # 상단 도구 버튼 모음 입니다.
    scroll_img = None              # 스크롤 이미지 테이블
    scroll_mask = None             # 스크롤 마스크 테이블
    mounting = None                # 스크롤 테이블 장착 뷰 내용
    confirmation = None            # 스크롤 테이블 장착 뷰 확인
    provider = None                # 데이터 공급관리
    active_folder = None           # USER 가 선택한 폴더
    active_path = None             # 뷰에 활성화된 이미지 경로
    active_image_index = None      # 뷰에 활성화된 이미지 인덱스 번호
    roi_list: list = None         # roi auto 처리한 open cv image
    mask_list: list = None         # roi auto 처리한 mask image

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.roi_list = []
        self.mask_list = []

        # 윈도우 세팅
        self.setWindowTitle(TITLE_WINDOW)
        self.setGeometry(0, 0, WINDOW_SIZE_WIDTH, WINDOW_SIZE_HEIGHT)

        # View, Menu, Tool 생성
        self.tool = Tool()
        self.view = View()
        self.view.setup(WINDOW_SIZE_WIDTH, WINDOW_SIZE_HEIGHT)
        self.view.threshold = DEFAULT_THRESHOLD

        self.menu = Menu()
        threshold_value = f'{DEFAULT_THRESHOLD}'
        threshold__max = f'{DEFAULT_THRESHOLD_MAX}'
        threshold__min = f'{DEFAULT_THRESHOLD_MIN}'
        self.menu.label_threshold_value.setText(threshold_value)
        self.menu.label_max_value.setText(threshold__max)
        self.menu.label_min_value.setText(threshold__min)

        # 스크롤과 테이블 생성
        self.scroll_img = QScrollArea()
        self.scroll_mask = QScrollArea()
        self.confirmation = TableConfirmation()
        self.mounting = TableMounting()

        # 프로그래시브 바 생성
        self.p_bar = QProgressBar(self)
        self.p_bar.setGeometry(30, 40, 200, 25)
        self.step = 0

        # ROI 자동화 처리 생성
        self.auto = Auto()
        self.auto.call_progress = self.progress_value
        self.roi_merge = Merge()
        self.mask_merge = Merge()

        # DATA 공급관리 생성
        self.provider = Provider()

        # 콜백 객체에 Window 메소드를 등록합니다.
        self.menu.call_scroll = self.scroll_data
        self.menu.call_open_path = self.file_open
        self.menu.call_export = self.mask_export
        self.menu.call_activation = self.get_activation
        self.menu.call_threshold = self.threshold_input
        self.menu.call_max = self.threshold_max
        self.menu.call_min = self.threshold_min

        self.tool.call_data_set = self.data_set
        self.tool.call_algorithm = self.algorithm
        self.tool.call_expansion = self.expansion
        self.tool.call_radio = self.tool_radio
        self.tool.radio_1.setChecked(True)

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
        _center = QVBoxLayout()
        _right = QHBoxLayout()

        # left layout
        _left.addLayout(self.menu)
        _left.addWidget(self.scroll_img)

        # right hide layout
        ly = QVBoxLayout()
        self.scroll_mask.setLayout(ly)
        _right.addWidget(self.scroll_mask)
        self.scroll_mask.hide()

        # center layout
        _center.addLayout(self.tool)

        # image view 좌측 상단 고정
        self.view.setAlignment(Qt.AlignTop)
        _center.addWidget(self.view, alignment=Qt.AlignLeft)

        # 프로그레시브 바 등록
        _center.addWidget(self.p_bar)

        # 전체 폼박스에 배치
        form_box.addLayout(_left)
        form_box.addLayout(_center)
        form_box.addLayout(_right)
        form_box.setStretchFactor(_left, 0)
        form_box.setStretchFactor(_center, 1)
        form_box.setStretchFactor(_right, 2)

        # 레이아웃에 폼박스 등록
        self.setLayout(form_box)
        self.show()

    # mark -  Call back method: menu
    def get_activation(self):
        return self.active_path

    # mark -  Call back method: menu
    def file_open(self):
        full_path = QFileDialog.getOpenFileName(None, 'Open file', './')

        if full_path[0]:
            file_path = f'{full_path[0]}'
            dir_list = os.path.dirname(file_path)
            self.active_folder = dir_list[-1]
            print('Window: file_open = ', self.active_folder)
            return file_path

        else:
            notice.message('Warning', '파일 선택을 하지 않았습니다.')
            return 0

    # mark -  Call back method: menu
    def threshold_input(self, update):
        self.view.threshold = int(update)

    # mark -  Call back method: menu
    def threshold_max(self, update):
        self.auto.max_size = int(update)

    # mark -  Call back method: menu
    def threshold_min(self, update):
        self.auto.min_size = int(update)

    # 마스크 이미지 내보내기
    # mark -  Call back method: menu
    def mask_export(self):
        if len(self.mask_list) is 0:
            notice.message('EXPORT', '선택된 이미지가 없습니다. 알고리즘 처리를 먼저 해 주세요!')
            return

        file_manager.create_folder(self.active_folder)
        notice.message('EXPORT', '내보내기를 시작합니다. 시간이 다소 소요 됩니다.')

        # 마스크 TEXT 파일로 내보내기
        i: int = 0
        for obj in self.mask_list:

            # 사용자 마스크 체크 확인
            _, _, check = self.confirmation.mask_disable[i]
            if check is True:
                img, index = obj
                img_text.to_binary(self.active_folder, img, index)

            i = i + 1
            self.progress_value(len(self.mask_list), i)

        # 종료 로직
        self.progress_value(100, 100)
        self.active_folder = None
        self.mask_list.clear()
        self.roi_list.clear()
        self.menu.exportButtonGrayColor()
        notice.message('EXPORT', '내보내기가 완료 되었습니다.')
        self.progress_value(0, 0)

        # 풀스크린 테이블 초기화
        self.confirmation.list_clear()
        self.confirmation.create(self.mask_list, self.roi_list)
        self.scroll_mask.setWidget(self.confirmation.top_widget)
        self.scroll_mask.show()
        self.view.repaint()

    # 공급자 클래스의 데이타 생성
    # mark -  Call back method: menu
    def scroll_data(self, img_folder, roi_list, extension):
        # provider.data_list "데이터 초기화"
        self.provider.info_list = []
        self.provider.create(IMAGE_START, img_folder, roi_list, extension)
        self.provider.data_read()
        self.mounting.create(self.provider.info_list)
        self.scroll_img.setWidget(self.mounting.top_widget)
        print('Window: 이미지 속성 데이터 생성완료')

    # mark -  Call back method: tool
    def tool_radio(self, chk_number):
        print('window: tool_radio =', chk_number)
        self.view.mask_select_count = chk_number

    # mark -  Call back method: tool
    def data_set(self):
        dicom_folder = self.file_open()

        if dicom_folder is '':
            return

        self.provider.create_dicom(dicom_folder)

    # mark -  Call back method: tool
    def expansion(self):
        print('window: expansion')

        if self.scroll_mask.isHidden() is True:
            self.scroll_mask.show()
            self.showFullScreen()
            self.tool.expansion_btn.setCheckable(True)
        else:
            self.scroll_mask.hide()
            self.showNormal()
            self.tool.expansion_btn.setCheckable(False)

        self.repaint()

    # mark -  Call back method: tool
    def algorithm(self):
        print('window: algorithm')

        # 풀스크린 테이블 초기화
        self.confirmation.list_clear()

        # 이미지 리스트 초기화
        self.roi_merge.clear()
        self.mask_merge.clear()
        self.mask_list.clear()
        self.roi_list.clear()

        if len(self.view.get_mask_list()) is 0:
            notice.message('Algorithm', '선택된 쓰레숄드가 없습니다.')
            return

        # string -> int casting.
        int_max = self.menu.label_max_value.text()
        int_min = self.menu.label_min_value.text()
        self.auto.clear_list()
        self.auto.max_size = int(int_max)
        self.auto.min_size = int(int_min)

        notice.message('알림', '종료 알림창이 보일 때 까지 잠시 기다려 주세요! \n Yes 를 클릭하시면 알고리즘 처리를 시작합니다.')

        # 사용자 선택 이미지 총 갯수
        i: int = 0
        total_count = len(self.provider.image_container)

        # 사용자 선택된 마스크들 처리
        for mask in self.view.get_mask_list():
            roi_result, mask_result = self.auto.roi_designation(self.provider.image_container,
                                                                self.active_image_index,
                                                                mask,
                                                                total_count)

            self.roi_list = self.roi_merge.mask_overwrite(total_count, roi_result)
            self.mask_list = self.mask_merge.mask_overwrite(total_count, mask_result)
            i = i + 1
            print('t = ', i)

        self.progress_value(100, 100)
        notice.message('알림', '알고리즘 처리를 종료 했습니다.')

        # 알고리즘 처리된 결과를 화면에 보여 줍니다.
        self.progress_value(0, 0)
        self.menu.exportButtonGreenColor()
        self.confirmation.create(self.mask_list, self.roi_list)
        self.scroll_mask.setWidget(self.confirmation.top_widget)
        self.scroll_mask.show()
        self.view.repaint()

    # mark -  Call back method: mounting
    def re_setting(self, path, index):
        print('window: re_setting', path)
        # 활성화 할 이미지 경로
        self.active_path = path
        self.active_image_index = index
        self.tool.set_select_image(path)

        # 메뉴에 선택된 현재 이미지를 표시 합니다.
        current_image_text = f'Select image number: {index} '
        self.menu.changeLabel(current_image_text)

        # 보여지는 view 에 들어갈 이미지 입니다.
        img = QPixmap(path)

        # Open cv 를 위한 상대 경로를 만들어 줍니다.
        image_path = file_manager.relative_path(path, IMAGE_START)

        # 보여지는 view 에 이미지를 넣어 주고
        self.view.q_graphic.setPixmap(img)
        self.view.repaint()
        self.view.re_setting(image_path)

    # mark -  Call back method: auto
    def progress_value(self, length, input_value):
        if input_value is 0:
            self.p_bar.setValue(0)
            return
        f_value = float((input_value / length) * 100)
        result = math.floor(f_value)
        self.p_bar.setValue(result)




