"""
Created by SungMin Yoon on 2019-12-13..
Copyright (c) 2019 year SungMin Yoon. All rights reserved.
"""
import sys
from PyQt5.QtWidgets import QApplication

# from LAB.task01.window import Window   # 간단한 QT VIEW
# from LAB.task02.window import Window   # Q 기반 VIEW 에서 마우스 좌표 가져오는 법 테스트
# from LAB.task03.window import Window   # 그레이 이미지를 컴퓨터에서 불러와 Threshold 값을 조정해 마법봉 기능을 구현
# from LAB.task04.window import Window   # Threshold 한 마스크 이미지를 저장
# from LAB.task05.window import Window   # 관심영역 저장 및 불러오기 기능 완료
# from LAB.task06.window import Window   # 스크롤 기능 추가
# from LAB.task07.window import Window   # 쓰레숄드 다중 선택, 알고리즘, 윈도우 레벨, 적용
# from LAB.task08.window import Window   # 템플릿 알고리즘 적용
# from LAB.task09.window import Window   # 관심영역 찾기 기술 구현
from LAB.task10.window import Window    # 관심영역 다중선택 구현


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())



