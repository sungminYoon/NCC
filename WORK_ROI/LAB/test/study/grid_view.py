"""
Created by SungMin Yoon on 2020-04-22..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QApplication,
                             QLineEdit, QHBoxLayout, QVBoxLayout)


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 숫자가 보이는 라인에딧 위젯
        leLayout = QHBoxLayout()
        le = QLineEdit(self)
        leLayout.addWidget(le)

        # button 모음 그리드 레이아웃
        grid = QGridLayout()
        names = ['Cls', 'Bck', '', 'Close',
                 '7', '8', '9', '/',
                 '4', '5', '6', '*',
                 '1', '2', '3', '-',
                 '0', '.', '=', '+']

        positions = [(i, j) for i in range(5) for j in range(4)]

        for position, name in zip(positions, names):
            if name == '':
                continue
            button = QPushButton(name)
            grid.addWidget(button, *position)

        # h_layout 과 grid 를 하나로 만들어줄 v_layout
        vbox = QVBoxLayout()
        vbox.addLayout(leLayout)
        vbox.addLayout(grid)

        self.setGeometry(300, 150, 300, 250)
        self.setLayout(vbox)

        self.setWindowTitle('GridLayout')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

