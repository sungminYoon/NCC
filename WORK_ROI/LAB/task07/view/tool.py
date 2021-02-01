"""
Created by SungMin Yoon on 2020-04-27..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

TITLE = 'Selected reference image'
TITLE_ROI = 'ROI Image'
TITLE_BTN_DICOM = 'Dicom Load'
TITLE_BTN_ALGORITHM = 'Algorithm'
VALUE_SLIDER_LEVEL = 'LEVEL: 0'
VALUE_SLIDER_COUNT = 'COUNT: 0'
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
        self.slider_label = QLabel(VALUE_SLIDER_LEVEL)
        self.title_count = QLabel(TITLE_ROI)
        self.select_label = QLabel(VALUE_SELECT_IMAGE)

        # Slider
        self.level_slider = QSlider(Qt.Horizontal)
        self.level_slider.move(300, 30)
        self.level_slider.setRange(0, 3000)
        self.level_slider.setSingleStep(1)
        self.level_slider.valueChanged.connect(self.on_changed_level)

        # Push button
        self.extraction_btn = QPushButton(TITLE_BTN_DICOM)
        self.extraction_btn.clicked.connect(self.extraction_button_clicked)
        self.algorithm_btn = QPushButton(TITLE_BTN_ALGORITHM)
        self.algorithm_btn.clicked.connect(self.algorithm_button_clicked)

        self.ui_setup()

    def ui_setup(self):

        # Mount to Widget
        self.topBox.addWidget(self.title_label)
        self.topBox.addWidget(self.select_label)

        self.levelBox.addWidget(self.extraction_btn)
        self.levelBox.addWidget(self.slider_label)
        self.levelBox.addWidget(self.level_slider)

        self.algorithm_Box.addWidget(self.algorithm_btn)

        self.verticalBox.addLayout(self.topBox)
        self.verticalBox.addLayout(self.levelBox)
        self.verticalBox.addLayout(self.algorithm_Box)

        self.addLayout(self.verticalBox)

    def set_select_image(self, value):
        index = f'path: {value}'
        self.select_label.setText(index)

    # mark - Event method
    def extraction_button_clicked(self):
        print('Tool : extraction_button_clicked')
        call = self.call_data_set
        call()
        self.extraction_btn.setText('Level Completion')

    # mark - Event method
    def algorithm_button_clicked(self):
        print('Tool : algorithm_button_clicked')
        call = self.call_algorithm
        call()

    # 슬라이더를 움직일시 발생하는 이벤트
    # mark - Event method
    def on_changed_level(self, value):
        level = f'LEVEL: {value}'
        self.slider_label.setText(level)

        call = self.call_slider_level
        call(value)

        # if value < 300:
        #     mask = self.view.level_images[value]
        #
        #     height, width = mask.shape
        #     gray_image = QImage(mask, width, height, QImage.Format_Grayscale8)
        #     pix_image = QPixmap.fromImage(gray_image)
        #
        #     # 보여지는 view 에 이미지를 넣어 주고
        #     self.view.q_graphic.setPixmap(pix_image)
        #     self.view.repaint()

