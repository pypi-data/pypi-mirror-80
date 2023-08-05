from typing import List, Callable

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QToolBar, QPushButton, QMenu, QToolButton, QAction, QWidget, QLabel, QSizePolicy,\
QGraphicsOpacityEffect

class ActionWithMessage(QAction):
    def __init__(self, text: str = '', icon: QIcon = None,
                 parent: QWidget = None, message: str = ''):
        super().__init__(parent)
        self.setText(text)
        if icon is not None:
            self.setIcon(icon)
        self.message = message


class TopToolBar(QToolBar):
    def __init__(self):
        super().__init__()
        self.setFloatable(False)
        self.setLayoutDirection(Qt.LeftToRight)
        self.setMovable(False)
        self.setContentsMargins(0, 0, 0, 0)

    def add_button(self, text: str):
        b = QPushButton(text)
        b.setObjectName('pmtopToolbarButton')
        b.setProperty('stat', 'unselected')
        self.addWidget(b)

        label = QLabel('  ')
        op = QGraphicsOpacityEffect()
        op.setOpacity(0)
        label.setGraphicsEffect(op)

        self.addWidget(label)  # 增加一段空间。

        return b

    def get_button(self, name: str):
        return self.findChild(QPushButton, name)


class TopToolBarRight(QToolBar):
    def __init__(self):
        super().__init__()
        self.setFloatable(False)
        self.setMovable(False)

        self.setContentsMargins(0, 0, 0, 0)
        self.setLayoutDirection(Qt.RightToLeft)
        self.hide_button = QToolButton()
        self.hide_button.setMaximumWidth(15)
        self.hide_button.setArrowType(Qt.UpArrow)
        self.addWidget(self.hide_button)


class PMGToolBar(QToolBar):
    tab_button: QPushButton = None
    _control_widget_dic = {}

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedHeight(100)
        self.setMinimumHeight(100)
        self.setMaximumHeight(100)
        self._control_widget_dic = {}
        self.add_height_occupation()

    def get_control_widget(self, widget_name: str) -> QPushButton:
        w = self._control_widget_dic.get(widget_name)
        if w is None:
            raise Exception(
                'Toolbar \'%s\' has no widget named \'%s\'' %
                widget_name)
        return w

    def add_tool_button(self, name: str, text: str = '',
                        icon: QIcon = None, menu: QMenu = None):
        tb = QToolButton()
        tb.setPopupMode(QToolButton.InstantPopup)
        tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        tb.setText(text)

        tb.setStyleSheet('QToolButton{height:60px;width:60px;border:0px;}')
        if icon is not None:
            tb.setIcon(icon)
            tb.setIconSize(QSize(40, 40))
        if menu is not None:
            tb.setMenu(menu)
        self.addWidget(tb)
        self._control_widget_dic[name] = tb
        return tb

    def add_height_occupation(self):
        button_num = 3
        texts = ['', '', '']
        from pmgwidgets import PMPushButtonPane

        pp = PMPushButtonPane()
        button_list = pp.add_height_occu_buttons()
        self.addWidget(pp)
        return button_list

    def add_buttons(self, button_num: int, names: List[str], texts: List[str], icons_path: List[str] = None) -> List[
        'QPushButton']:
        from pmgwidgets import PMPushButtonPane

        pp = PMPushButtonPane()
        button_list = pp.add_buttons(button_num, texts, icons_path)
        for i, name in enumerate(names):
            self._control_widget_dic[name] = button_list[i]
        self.addWidget(pp)
        return button_list

    def add_widget(self, name: str, widget: 'QWidget'):
        self._control_widget_dic[name] = widget
        self.addWidget(widget)
        return widget

    def add_menu_to(self, button_name: str,
                    action_texts: List[str], action_commands: List['Callable']) -> None:
        button = self.get_control_widget(button_name)
        if button is not None:
            menu = QMenu(self)
            for text, cmd in zip(action_texts, action_commands):
                a = QAction(text=text, parent=menu)
                menu.addAction(a)
                a.triggered.connect(cmd)
            button.setMenu(menu)

    def append_menu(self, button_name: str, action_text: str, action_command: 'Callable') -> 'QAction':
        button: 'QPushButton' = self.get_control_widget(button_name)
        if button is not None:
            menu = button.menu()
            if menu is None:
                self.add_menu_to(button_name, [action_text], [action_command])
                return

            a = QAction(text=action_text, parent=menu)
            menu.addAction(a)
            print(menu, action_text)
            a.triggered.connect(action_command)
            return a
        return None
