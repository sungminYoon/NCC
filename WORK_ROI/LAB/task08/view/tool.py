"""
Created by SungMin Yoon on 2020-04-27..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

TITLE = 'Selected reference image ->'
TITLE_ROI = 'ROI Image'
TITLE_BTN_ALGORITHM = 'Algorithm'
VALUE_SELECT_IMAGE = 'No select image'


class Tool(QHBoxLayout):

    call_data_set = None
    call_mask_set = None
    call_slider_level = None
    call_algorithm = None

    def __init__(self, parent=None):
        super(Tool, self).__init__(parent)

        self.verticalBox = QVBoxLayout()
        self.topBox = QHBoxLayout()
        self.levelBox = QHBoxLayout()
        self.algorithm_Box = QHBoxLayout()

        self.title_label = QLabel(TITLE)
        self.title_label.setStyleSheet("background-color: lightGreen")
        self.title_count = QLabel(TITLE_ROI)
        self.select_label = QLabel(VALUE_SELECT_IMAGE)

        # Push button
        self.algorithm_btn = QPushButton(TITLE_BTN_ALGORITHM)
        self.algorithm_btn.clicked.connect(self.algorithm_button_clicked)

        self.ui_setup()

    def ui_setup(self):

        # Mount to Widget
        self.topBox.addWidget(self.title_label,  alignment=Qt.AlignLeft)
        self.topBox.addWidget(self.select_label,  alignment=Qt.AlignRight)
        self.algorithm_Box.addWidget(self.algorithm_btn)

        self.verticalBox.addLayout(self.topBox)
        self.verticalBox.addLayout(self.algorithm_Box)
        self.addLayout(self.verticalBox)

    def set_select_image(self, value):
        index = f'path: {value}'
        self.select_label.setText(index)

    # mark - Event method
    def algorithm_button_clicked(self):
        print('Tool : algorithm_button_clicked')
        call = self.call_algorithm
        call()



