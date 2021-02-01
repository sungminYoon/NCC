"""
Created by SungMin Yoon on 2020-04-27..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

TITLE_PATH = 'Selected reference image ->'
TITLE_ROI = 'ROI Image'
TITLE_BTN_ALGORITHM = 'Algorithm'
TITLE_THRESHOLD_CHOICE = 'Threshold choice'
PATH_EXPANSION_IMAGE = './TDD/resource/btn_expansion.png'
PATH_EXPANSION_IMAGE_X = './TDD/resource/btn_x.png'
VALUE_SELECT_IMAGE = 'No select image'


class Tool(QHBoxLayout):

    call_data_set = None
    call_mask_set = None
    call_slider_level = None
    call_algorithm = None
    call_expansion = None
    call_radio = None
    choice_threshold = None

    radio_1: QRadioButton
    radio_2: QRadioButton
    radio_3: QRadioButton
    radio_4: QRadioButton
    radio_5: QRadioButton

    def __init__(self, parent=None):
        super(Tool, self).__init__(parent)

        self.verticalBox = QVBoxLayout()
        self.topBox = QHBoxLayout()
        self.levelBox = QHBoxLayout()
        self.radio_Box = QHBoxLayout()
        self.expansion_Box = QHBoxLayout()
        self.algorithm_Box = QHBoxLayout()

        self.title_label = QLabel(TITLE_PATH)
        self.title_label.setStyleSheet("background-color: lightGreen")
        self.title_count = QLabel(TITLE_ROI)
        self.select_label = QLabel(VALUE_SELECT_IMAGE)

        # Expansion 버튼
        self.expansion_label = QLabel('FullScreen')
        self.expansion_btn = QPushButton()
        self.expansion_btn.setGeometry(0, 0, 50, 50)
        self.expansion_btn.setIcon(QIcon(PATH_EXPANSION_IMAGE))
        self.expansion_btn.setIconSize(QSize(20, 20))
        self.expansion_btn.clicked.connect(self.expansion_button_clicked)
        self.expansion_btn.setChecked(True)

        # Radio 버튼
        self.radio_title = QLabel()
        self.radio_title.setText(TITLE_THRESHOLD_CHOICE)

        self.radio_1 = QRadioButton('1ea')
        self.radio_1.clicked.connect(self.radio_button_event)

        self.radio_2 = QRadioButton('2ea')
        self.radio_2.clicked.connect(self.radio_button_event)

        self.radio_3 = QRadioButton('3ea')
        self.radio_3.clicked.connect(self.radio_button_event)

        self.radio_4 = QRadioButton('4ea')
        self.radio_4.clicked.connect(self.radio_button_event)

        self.radio_5 = QRadioButton('5ea')
        self.radio_5.geometry()
        self.radio_5.clicked.connect(self.radio_button_event)

        self.radio_6 = QRadioButton('6ea')
        self.radio_6.geometry()
        self.radio_6.clicked.connect(self.radio_button_event)

        self.radio_7 = QRadioButton('7ea')
        self.radio_7.geometry()
        self.radio_7.clicked.connect(self.radio_button_event)

        self.radio_8 = QRadioButton('8ea')
        self.radio_8.geometry()
        self.radio_8.clicked.connect(self.radio_button_event)

        self.radio_9 = QRadioButton('9ea')
        self.radio_9.geometry()
        self.radio_9.clicked.connect(self.radio_button_event)

        # Push button
        self.algorithm_btn = QPushButton(TITLE_BTN_ALGORITHM)
        self.algorithm_btn.clicked.connect(self.algorithm_button_clicked)

        self.ui_setup()

    def ui_setup(self):
        # Mount to Widget
        self.algorithm_Box.addWidget(self.algorithm_btn)
        self.topBox.addWidget(self.title_label,  alignment=Qt.AlignLeft)
        self.topBox.addWidget(self.select_label,  alignment=Qt.AlignRight)

        # 라디오 버튼
        self.radio_Box.addWidget(self.radio_title,  alignment=Qt.AlignLeft)
        self.radio_Box.addWidget(self.radio_1,  alignment=Qt.AlignLeft)
        self.radio_Box.addWidget(self.radio_2,  alignment=Qt.AlignLeft)
        self.radio_Box.addWidget(self.radio_3,  alignment=Qt.AlignLeft)
        self.radio_Box.addWidget(self.radio_4,  alignment=Qt.AlignLeft)
        self.radio_Box.addWidget(self.radio_5,  alignment=Qt.AlignLeft)
        self.radio_Box.addWidget(self.radio_6, alignment=Qt.AlignLeft)
        self.radio_Box.addWidget(self.radio_7, alignment=Qt.AlignLeft)
        self.radio_Box.addWidget(self.radio_8, alignment=Qt.AlignLeft)
        self.radio_Box.addWidget(self.radio_9, alignment=Qt.AlignLeft)

        # 확장 버튼 등록
        self.expansion_Box.addWidget(self.expansion_label, alignment=Qt.AlignRight)
        self.expansion_Box.addWidget(self.expansion_btn, alignment=Qt.AlignRight)
        self.radio_Box.addLayout(self.expansion_Box)

        self.verticalBox.addLayout(self.topBox)
        self.verticalBox.addLayout(self.radio_Box)
        self.verticalBox.addLayout(self.algorithm_Box)
        self.addLayout(self.verticalBox)

    def radio_button_event(self):
        print('Tool: radio_button_event')
        if self.radio_1.isChecked():
            self.choice_threshold = 1
        elif self.radio_2.isChecked():
            self.choice_threshold = 2
        elif self.radio_3.isChecked():
            self.choice_threshold = 3
        elif self.radio_4.isChecked():
            self.choice_threshold = 4
        elif self.radio_5.isChecked():
            self.choice_threshold = 5
        elif self.radio_6.isChecked():
            self.choice_threshold = 6
        elif self.radio_7.isChecked():
            self.choice_threshold = 7
        elif self.radio_8.isChecked():
            self.choice_threshold = 8
        elif self.radio_9.isChecked():
            self.choice_threshold = 9

        call = self.call_radio
        call(self.choice_threshold)

    def set_select_image(self, value):
        index = f'path: {value}'
        self.select_label.setText(index)

    # mark - Event method
    def algorithm_button_clicked(self):
        print('call Window : algorithm_button_clicked')
        call = self.call_algorithm
        call()

    # mark - Event method
    def expansion_button_clicked(self):
        print('call Window : expansion_button_clicked')
        if self.expansion_btn.isChecked():
            self.expansion_btn.setIcon(QIcon(PATH_EXPANSION_IMAGE))
        else:
            self.expansion_btn.setIcon(QIcon(PATH_EXPANSION_IMAGE_X))

        call = self.call_expansion
        call()

