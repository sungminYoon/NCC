"""
Created by SungMin Yoon on 2020-12-08..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
from PyQt5.QtCore import QSize
from PyQt5.QtGui import *
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import *


class TableConfirmation:
    table_list = None
    top_widget = None
    top_layout = None
    group_layout = None
    call_back = None
    copy_mask: list         # 마스크 icon 리스트
    mask_disable: list      # 필요 없는 마스크

    def __init__(self):
        self.copy_mask = []
        self.mask_disable = []

    def list_clear(self):
        self.copy_mask.clear()
        self.mask_disable.clear()

    def create(self, mask_list, cv_list):
        self.top_widget = QWidget()
        self.top_layout = QVBoxLayout()

        '''
        table_cell_count = 0
        중요한 카운트 입니다.
        테이블 셀 갯수만 세어
        click_event_mask 어긋남을 방지 합니다.
        '''
        table_cell_count = 0
        for count in range(0, len(mask_list)):
            if mask_list[count] == 0:
                print('TableConfirmation: mask_list =', count)
            else:
                mask, index = mask_list[count]
                h, w = mask.shape[:2]

                cv_image, _ = cv_list[count]
                # 스크롤 박스에 장착될 그룹 박스
                group_box = QGroupBox()
                group_box.setMaximumWidth(w * 2)
                group_box.setMaximumHeight(h)
                group_box.setTitle(f'{index}')
                self.group_layout = QHBoxLayout(group_box)

                # 버튼 이미지 세팅
                grey_image = QImage(mask, w, h, QImage.Format_Grayscale8)
                pix_image = QPixmap.fromImage(grey_image)
                icon_mask = QIcon(pix_image)

                # 마스크 선택 리스트
                t = (f'{index}', count, True)
                self.mask_disable.append(t)
                self.copy_mask.append(icon_mask)

                q_image = QImage(cv_image, w, h, QImage.Format_Grayscale8)
                pix_image_cv = QPixmap.fromImage(q_image)
                icon_cv = QIcon(pix_image_cv)

                # Image mask button
                button_mask = QPushButton()
                button_mask.setCheckable(True)
                button_mask.setObjectName(f'{table_cell_count}')
                button_mask.setGeometry(0, 0, w, h)
                button_mask.clicked.connect(self.click_event_mask)
                button_mask.setIcon(icon_mask)
                button_mask.setIconSize(QSize(w, h))
                self.group_layout.addWidget(button_mask)

                # Image open_cv button
                button_image = QPushButton()
                button_mask.setObjectName(f'{table_cell_count}')
                button_image.setGeometry(0, 0, w, h)
                button_image.clicked.connect(self.click_event_image)
                button_image.setIcon(icon_cv)
                button_image.setIconSize(QSize(w, h))
                self.group_layout.addWidget(button_image)

                # 스크롤의 가장 위에 보여질 그룹박스
                self.top_layout.addWidget(group_box)
                self.top_widget.setLayout(self.top_layout)

                table_cell_count = table_cell_count + 1

    # mark - Event Method
    def click_event_mask(self):
        print('Confirmation: click_event_mask')
        button: QPushButton = self.group_layout.sender()

        if button.isCheckable():
            button.setCheckable(False)
            button.setIcon(QIcon('./LAB/resource/big_x.png'))
            name = button.objectName()
            index = int(name)
            _1, _2, _ = self.mask_disable[index]
            t = (_1, _2, False)
            self.mask_disable[index] = t

        else:
            button.setCheckable(True)
            name = button.objectName()
            index = int(name)
            mask = self.copy_mask[index]
            button.setIcon(mask)
            _1, _2, _ = self.mask_disable[index]
            t = (_1, _2, True)
            self.mask_disable[index] = t

    # mark - Event Method
    def click_event_image(self):
        print('Confirmation: click_event_image')
        button: QPushButton = self.group_layout.sender()
        index = button.objectName()
        print(index)