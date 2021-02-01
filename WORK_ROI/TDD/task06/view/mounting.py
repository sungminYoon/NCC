"""
Created by SungMin Yoon on 2020-04-07..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from TDD.common.model.info import Info


class Mounting:
    table_list = None
    top_widget = None
    top_layout = None
    group_layout = None
    call_back = None

    def __init__(self):
        pass

    def create(self, data_list):
        self.top_widget = QWidget()
        self.top_layout = QVBoxLayout()
        self.table_list = data_list

        i = 0
        for obj in data_list:
            # 버트에 표시 되는 숫자 1부터
            index = f'{i+1}'

            # 데이터 모델 타입으로 형변환 합니다.
            data: Info = obj

            # 스크롤 박스에 장착될 그룹 박스
            group_box = QGroupBox()
            group_box.setTitle(data.image_name)
            self.group_layout = QHBoxLayout(group_box)

            # 그룹박스 레이아웃에 들어가는 버튼
            push_button = QPushButton(group_box)
            push_button.setText(index)
            push_button.clicked.connect(self.click_event)
            push_button.setFixedSize(30, 30)
            self.group_layout.addWidget(push_button)

            # 그룹박스 레이아웃에 들어갈 썸네일 이미지
            thumbnail_path = data.image_thumbnail
            thumbnail = QPixmap(thumbnail_path)
            thumbnail_label = QLabel()
            thumbnail_label.setPixmap(thumbnail)
            thumbnail_label.setGeometry(0, 0, 30, 30)
            self.group_layout.addWidget(thumbnail_label)

            # 그룹박스 레이아웃에 들어갈 roi 여부
            check = 'X'
            if data.image_roi is not None:
                check = 'O'
            roi_label = QLabel()
            roi_label.setText(check)
            roi_label.setGeometry(0, 0, 30, 30)
            self.group_layout.addWidget(roi_label)

            # 스크롤의 가장 위에 보여질 그룹박스
            self.top_layout.addWidget(group_box)
            self.top_widget.setLayout(self.top_layout)

            # FOR 증감
            i = i + 1

    # mark - Event call back Method
    def click_event(self):
        # 스크롤 속의 그룹박스 테이블 에서 버튼을 눌렀을때 sender() 를 가져와서
        # 그룹박스 테이블 리스트의 데이터의 인덱스를 찾아 매칭 시켜 image_path 데이터를 가져 옵니다.
        button: QPushButton = self.group_layout.sender()
        index = button.text()
        num = int(index)

        # 실제 리스트에서 가져 올때는 0부터 가져오기 때문에 -1
        data: Info = self.table_list[num - 1]
        path = data.image_path

        # DATA 에서 경로를 파라미터로 받아 콜백 처리 합니다.
        call = self.call_back
        call(path)
