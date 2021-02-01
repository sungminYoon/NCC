"""
Created by SungMin Yoon on 2019-12-17..
Copyright (c) 2019 year SungMin Yoon. All rights reserved.
"""
import os
import cv2 as cv
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from TDD.common.path import file_manager
from TDD.task07.view.main_view import View
from TDD.task07.view.tool import Tool
from TDD.task07.view.menu import Menu
from TDD.task07.view.mounting import Mounting
from TDD.task07.control.provider import Provider
from TDD.task07.control.auto import Auto


TITLE_WINDOW = 'ROI TOOL'
WINDOW_SIZE_WIDTH = 1024
WINDOW_SIZE_HEIGHT = 768
IMAGE_SAVE = 'TDD/image/'
IMAGE_START = 'TDD'


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
    level_image_index = None        # 선택된 레벨 이미지
    current_level = None            # 현재 레벨 값

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # 윈도우 세팅
        self.setWindowTitle(TITLE_WINDOW)
        self.setGeometry(0, 0, WINDOW_SIZE_WIDTH, WINDOW_SIZE_HEIGHT)

        # View, Menu, Tool 생성
        self.view = View()
        self.view.setup(WINDOW_SIZE_WIDTH, WINDOW_SIZE_HEIGHT)
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
        self.menu.call_scroll = self.scroll_data
        self.menu.call_open_path = self.file_open
        self.menu.call_save = self.mask_save
        self.menu.call_activation = self.get_activation
        self.menu.call_threshold = self.threshold_value

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
        _right.addWidget(self.view)

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
    def threshold_value(self, update):
        self.view.threshold = int(update)
        print(self.view.threshold)

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
    def scroll_data(self, png_folder, roi_list):
        # provider.data_list "데이터 초기화"
        self.provider.info_list = []
        self.provider.data_create(IMAGE_START, png_folder, roi_list)
        self.provider.data_read()
        self.mounting.create(self.provider.info_list)
        self.scroll.setWidget(self.mounting.top_widget)
        print('Window: 이미지 속성 데이터 생성완료')

    # mark -  Call back method: tool
    def data_set(self):
        dicom_folder = self.file_open()
        self.provider.data_create_dicom(dicom_folder)

    # mark -  Call back method: tool
    def slider_level(self, value):
        print('window: slider_level = ', value)
        self.current_level = value
        dicom_origin = self.provider.dicom_set[self.active_image_index]
        self.view.level_threshold(value, dicom_origin)

    # mark -  Call back method: tool
    def algorithm(self):
        print('window: algorithm')

        # 이미지 들을 auto.py 모듈을 사용해 적용 합니다.
        complete_list = []
        i: int = 0
        for mask in self.view.mask_list:
            print('self.view.mask_list = ', len(self.view.mask_list))
            best_list = self.auto.roi_designation(self.provider.image_container,
                                                  self.view.mouse_position_list[i],
                                                  self.active_image_index,
                                                  mask)
            complete_list.append(best_list)
            i = i + 1

        # 이미지 리스트가 1개 일 경우
        complete_count = len(complete_list)
        if complete_count == 1:
            j: int = 0
            images = complete_list[0]
            for image in images:
                # 결과 보기
                title = f'{j}'
                cv.imshow(title, image)
                cv.waitKey(0)
                cv.destroyAllWindows()
                j = j + 1

        # 이미지 리스트가 많은 경우
        count_list = []
        for image_list in complete_list:
            if image_list is None:
                break
            count_list.append(len(image_list))

        # 가장긴 이미지 리스트 찾아 기준 만들기
        count_max = max(count_list)
        count_index = count_list.index(count_max)
        standard = complete_list[count_index]

        # 알고리즘 으로 찾은 이미지 리스트들을 돌립니다.
        k: int = 0
        for compare in complete_list:

            # 돌리는 이미지 리스트들 중에 기준이 된는것은 제외
            if count_index != k:

                # 이미지 리스트의 이미지들을 기준 리스트 이미지와 합칩니다.
                r: int = 0
                for image in compare:

                    try:
                        background = standard[r]
                        add_image = cv.add(background, image)

                        # 결과 보기
                        title = f'{r}'
                        cv.imshow(title, add_image)
                        cv.waitKey(0)
                        cv.destroyAllWindows()

                    except ValueError:
                        print('ValueError')

                    r = r + 1
            k = k + 1

    # mark -  Call back method: mounting
    def re_setting(self, path, index):
        print('window: view_resetting', path)
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

