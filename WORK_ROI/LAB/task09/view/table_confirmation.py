"""
Created by SungMin Yoon on 2020-12-08..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
from PyQt5.QtCore import QSize
from PyQt5.QtGui import *
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import *

TABLE_BOX_SIZE = 600
TABLE_SELL_SIZE = 512


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

        for i in range(0, len(mask_list)):
            if mask_list[i] == 0:
                print('TableConfirmation: mask_list =', i)
            else:
                mask, index = mask_list[i]

                cv_image, _ = cv_list[i]
                # 스크롤 박스에 장착될 그룹 박스
                group_box = QGroupBox()
                group_box.setMaximumWidth(TABLE_BOX_SIZE * 2)
                group_box.setMaximumHeight(TABLE_BOX_SIZE)
                group_box.setTitle(f'{index}')
                self.group_layout = QHBoxLayout(group_box)

                # Button image setting
                grey_image = QImage(mask, TABLE_SELL_SIZE, TABLE_SELL_SIZE, QImage.Format_Grayscale8)
                pix_image = QPixmap.fromImage(grey_image)
                icon_mask = QIcon(pix_image)

                # 마스크 선택 리스트
                t = (f'{index}', i, True)
                self.mask_disable.append(t)
                self.copy_mask.append(icon_mask)

                q_image = QImage(cv_image, TABLE_SELL_SIZE, TABLE_SELL_SIZE, QImage.Format_Grayscale8)
                pix_image_cv = QPixmap.fromImage(q_image)
                icon_cv = QIcon(pix_image_cv)

                # Image mask button
                button_mask = QPushButton()
                button_mask.setCheckable(True)
                button_mask.setObjectName(f'{i}')
                button_mask.setGeometry(0, 0, TABLE_BOX_SIZE, TABLE_BOX_SIZE)
                button_mask.clicked.connect(self.click_event_mask)
                button_mask.setIcon(icon_mask)
                button_mask.setIconSize(QSize(TABLE_SELL_SIZE, TABLE_SELL_SIZE))
                self.group_layout.addWidget(button_mask)

                # Image open_cv button
                button_image = QPushButton()
                button_mask.setObjectName(f'{i}')
                button_image.setGeometry(0, 0, TABLE_BOX_SIZE, TABLE_BOX_SIZE)
                button_image.clicked.connect(self.click_event_image)
                button_image.setIcon(icon_cv)
                button_image.setIconSize(QSize(TABLE_SELL_SIZE, TABLE_SELL_SIZE))
                self.group_layout.addWidget(button_image)

                # 스크롤의 가장 위에 보여질 그룹박스
                self.top_layout.addWidget(group_box)
                self.top_widget.setLayout(self.top_layout)

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