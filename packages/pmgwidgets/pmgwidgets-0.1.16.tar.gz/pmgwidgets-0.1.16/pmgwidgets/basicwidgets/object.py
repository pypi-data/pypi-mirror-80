from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget


class PMDockObject(object):
    '''
    修改：
    原先，主窗口中的各个可停靠窗口，在点击右上角关闭按钮的时候会隐藏，可以在视图菜单中打开。
    但是当控件中有on_closed_action属性，且值为‘delete’的时候，控件就会被回收。
    为了实现控件的管理，控件需要继承PMDockObject，并且需要用多继承的方式。

    from pyminer2.ui.generalwidgets import PMDockObject
    这个PMDockObject中定义了一些方法，作为补充。

    class PMDockObject(object):
        on_closed_action = 'hide'  # 或者'delete'。

        def raise_widget_to_visible(self, widget: 'QWidget'):
            pass

        def on_dock_widget_deleted(self):
            pass

    '''
    on_closed_action = 'hide'  # 或者'delete'。

    def raise_widget_to_visible(self, widget: 'QWidget'):
        pass

    def on_dock_widget_deleted(self):
        pass
