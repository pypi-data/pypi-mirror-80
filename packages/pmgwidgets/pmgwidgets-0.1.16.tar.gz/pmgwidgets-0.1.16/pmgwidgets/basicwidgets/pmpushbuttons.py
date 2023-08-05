'''
pmpushbuttons是一个按钮组，专门负责向工具栏中插入按钮。
其中PMPushButtonPane是按钮的载体，可以插入竖向排布的两个到三个按钮。
作者：Zhanyi Hou
'''
from typing import List

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMenu,QSizePolicy,QLabel


from pmgwidgets.sourcemgr import create_icon


class PMPushButtonPane(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

    def add_height_occu_buttons(self):
        button_num = 3
        text = ['','','']
        if text is None:
            text = [''] * button_num


        height = 25
        font_size = 12
        btn_list = []
        for i in range(button_num):
            b = QLabel()
            b.setText('aaaaa')
            b.setObjectName('occu')
            b.setStyleSheet('QLabel{height:33px;}')
            b.setMinimumHeight(33)
            b.setMinimumWidth(1)
            b.setMaximumWidth(1)
            btn_list.append(b)

            b.setObjectName('space_occupation_button')
            print('add_button')
            self.layout.addWidget(b)
        return btn_list

    def add_buttons(self, button_num: int = 2, text: list = None, icon_path: list = None,
                    menu: list = None) -> List[QPushButton]:
        if text is None:
            text = [''] * button_num
        if icon_path is None:
            icon_path = [None] * button_num
        if menu is None:
            menu = [None] * button_num
        if len(text) != button_num or len(
                icon_path) != button_num or len(menu) != button_num:
            raise Exception('text,icon和menu参数都必须为长为2的可迭代对象。')
        if button_num == 2:
            height = 35
            font_size = 12
        else:
            height = 25
            font_size = 12
        btn_list = []
        for i in range(button_num):
            b = self.add_button(text=text[i], icon=create_icon(icon_path[i]), menu=menu[i], height=height,
                                font_size=font_size)
            btn_list.append(b)
        return btn_list

    def add_button(self, text: str = '', icon: QIcon = None, menu: QMenu = None, height: int = 30,
                   font_size: int = 12) -> QPushButton:
        b = QPushButton()
        b.setText(text)
        if icon is not None:
            b.setIcon(icon)
        if menu is not None:
            b.setMenu(menu)
        b.setStyleSheet(
            'QPushButton{border:0px;font-size:%dpx;padding:2px 2px;height:%dpx;text-align:left;}' % (
                font_size, height))
        self.layout.addWidget(b)
        return b
