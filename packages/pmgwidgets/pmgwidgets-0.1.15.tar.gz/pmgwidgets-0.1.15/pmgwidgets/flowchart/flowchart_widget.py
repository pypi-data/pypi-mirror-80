import sys

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QToolButton, QSpacerItem, QSizePolicy, QGraphicsView, \
    QFrame, QApplication, QGraphicsObject, QGraphicsScene, QGraphicsSceneMouseEvent
from PyQt5.QtCore import QSize, QCoreApplication, QRectF, Qt, QPointF, pyqtSignal, QLineF, QObject
from PyQt5.QtGui import QIcon, QPixmap, QPen, QColor, QBrush, QPainter, QPainterPath

from pmgwidgets.flowchart.flow_items import CustomRect, CustomPort

COLOR_NORMAL = QColor(212, 227, 242)
COLOR_HOVER = QColor(255, 200, 00)
COLOR_HOVER_PORT = QColor(0, 0, 50)


class PMGraphicsScene(QGraphicsScene):
    signal_item_dragged = pyqtSignal(str)
    signal_port_clicked = pyqtSignal(str)

    def __init__(self, parent=None, graphics_view: 'QGraphicsView' = None):
        super().__init__(parent)
        self.drawing_lines = False
        self.line_start_port = None
        self.line_start_point = None
        self.line_end_port = None
        self.line = self.addLine(0, 0, 100, 100, QPen())
        self.graphics_view = graphics_view

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        super(PMGraphicsScene, self).mouseMoveEvent(event)
        if self.drawing_lines == True:
            self.line.show()
            self.line_end_point = event.scenePos()
            self.line.setLine(QLineF(self.line_end_point, self.line_start_point))

    def connect_port(self, end_port):
        from pmgwidgets.flowchart.flow_items import CustomLine
        self.line.hide()
        line = CustomLine(self.line_start_port, end_port, self)
        line.repaint_callback = lambda: self.graphics_view.viewport().update()
        self.addItem(line)
        self.signal_item_dragged.connect(line.refresh)
        self.drawing_lines = False


class Node(QObject):
    def __init__(self, canvas: 'PMGraphicsScene'):
        super(Node, self).__init__()
        self.base_rect = CustomRect(self)
        self.input_ports = [CustomPort(0), CustomPort(1)]
        self.output_ports = [CustomPort(2), CustomPort(3)]
        self.canvas = canvas
        self.setup()

    def refresh_pos(self):
        y = self.base_rect.y()
        dy_input = self.base_rect.boundingRect().height() / (1 + len(self.input_ports))
        dy_output = self.base_rect.boundingRect().height() / (1 + len(self.output_ports))
        x_input = self.base_rect.x() + 5
        x_output = self.base_rect.x() + self.base_rect.boundingRect().width() - 15
        for i, p in enumerate(self.input_ports):
            p.setPos(x_input, y + int(dy_input * (1 + i)))
        for i, p in enumerate(self.output_ports):
            p.setPos(x_output, y + int(dy_output * (1 + i)))
        self.canvas.signal_item_dragged.emit('')

    def setup(self):
        self.base_rect.setPos(80, 80)
        self.refresh_pos()

        self.canvas.addItem(self.base_rect)
        for p in self.input_ports + self.output_ports:
            self.canvas.addItem(p)
            p.port_clicked.connect(self.on_port_clicked)

    def on_port_clicked(self, port: 'CustomPort'):
        if self.canvas.drawing_lines == True:
            if not self.canvas.line_start_port is port:
                self.canvas.connect_port(port)
            else:
                self.canvas.drawing_lines = False
        else:
            self.canvas.drawing_lines = True
            self.canvas.line_start_point = port.center_pos
            self.canvas.line_start_port = port


class PMFlowWidget(QWidget):
    def __init__(self):
        # from pyminer2.ui.base.widgets.resources import icon_lc_save, icon_sc_shadowcurser, \
        #     icon_lc_connectorlinesarrowend, icon_lc_undo, \
        #     icon_lc_redo, icon_sc_deletepage, icon_lc_aligncenter, icon_lc_alignmiddle, icon_lc_zoomin, icon_lc_zoomout, \
        #     icon_dataprovider, icon_sc_autosum, icon_lc_drawchart, icon_lc_statisticsmenu, icon_lc_dbreportedit
        _translate = QCoreApplication.translate
        super().__init__()
        self.setObjectName("tab_flow")

        self.verticalLayout_6 = QVBoxLayout(self)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.widget_3 = QWidget(self)
        self.widget_3.setMinimumSize(QSize(0, 30))
        self.widget_3.setObjectName("widget_3")

        self.horizontalLayout_6 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(1)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.toolButton_4 = QToolButton(self.widget_3)
        icon7 = QIcon()
        icon7.addPixmap(QPixmap(":/pyqt/source/images/NavOverFlow_Start.png"), QIcon.Normal,
                        QIcon.Off)
        self.toolButton_4.setIcon(icon7)
        self.toolButton_4.setIconSize(QSize(25, 25))
        self.toolButton_4.setObjectName("toolButton_4")
        self.horizontalLayout_6.addWidget(self.toolButton_4)
        self.toolButton_3 = QToolButton(self.widget_3)
        icon8 = QIcon()
        icon8.addPixmap(QPixmap(":/pyqt/source/images/lc_basicstop.png"), QIcon.Normal, QIcon.Off)
        self.toolButton_3.setIcon(icon8)
        self.toolButton_3.setIconSize(QSize(25, 25))
        self.toolButton_3.setObjectName("toolButton_3")
        self.horizontalLayout_6.addWidget(self.toolButton_3)
        self.toolButton_6 = QToolButton(self.widget_3)

        # self.toolButton_6.setIcon(icon_lc_save)
        self.toolButton_6.setIconSize(QSize(25, 25))
        self.toolButton_6.setObjectName("toolButton_6")
        self.horizontalLayout_6.addWidget(self.toolButton_6)
        self.toolButton_5 = QToolButton(self.widget_3)

        # self.toolButton_5.setIcon(icon_sc_shadowcurser)
        self.toolButton_5.setIconSize(QSize(25, 25))
        self.toolButton_5.setObjectName("toolButton_5")
        self.horizontalLayout_6.addWidget(self.toolButton_5)
        self.toolButton_2 = QToolButton(self.widget_3)

        # self.toolButton_2.setIcon(icon_lc_connectorlinesarrowend)
        self.toolButton_2.setIconSize(QSize(25, 25))
        self.toolButton_2.setObjectName("toolButton_2")
        self.horizontalLayout_6.addWidget(self.toolButton_2)
        self.toolButton = QToolButton(self.widget_3)

        # self.toolButton.setIcon(icon_lc_undo)
        self.toolButton.setIconSize(QSize(25, 25))
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout_6.addWidget(self.toolButton)
        self.toolButton_7 = QToolButton(self.widget_3)

        # self.toolButton_7.setIcon(icon_lc_redo)
        self.toolButton_7.setIconSize(QSize(25, 25))
        self.toolButton_7.setObjectName("toolButton_7")
        self.horizontalLayout_6.addWidget(self.toolButton_7)
        self.toolButton_8 = QToolButton(self.widget_3)

        # self.toolButton_8.setIcon(icon_sc_deletepage)
        self.toolButton_8.setIconSize(QSize(25, 25))
        self.toolButton_8.setObjectName("toolButton_8")
        self.horizontalLayout_6.addWidget(self.toolButton_8)
        self.toolButton_9 = QToolButton(self.widget_3)

        # self.toolButton_9.setIcon(icon_lc_aligncenter)
        self.toolButton_9.setIconSize(QSize(25, 25))
        self.toolButton_9.setObjectName("toolButton_9")
        self.horizontalLayout_6.addWidget(self.toolButton_9)
        self.toolButton_10 = QToolButton(self.widget_3)

        # self.toolButton_10.setIcon(icon_lc_alignmiddle)
        self.toolButton_10.setIconSize(QSize(25, 25))
        self.toolButton_10.setObjectName("toolButton_10")
        self.horizontalLayout_6.addWidget(self.toolButton_10)
        self.toolButton_11 = QToolButton(self.widget_3)

        # self.toolButton_11.setIcon(icon_lc_zoomin)
        self.toolButton_11.setIconSize(QSize(25, 25))
        self.toolButton_11.setObjectName("toolButton_11")
        self.horizontalLayout_6.addWidget(self.toolButton_11)
        self.toolButton_12 = QToolButton(self.widget_3)

        # self.toolButton_12.setIcon(icon_lc_zoomout)
        self.toolButton_12.setIconSize(QSize(25, 25))
        self.toolButton_12.setObjectName("toolButton_12")
        self.horizontalLayout_6.addWidget(self.toolButton_12)
        self.toolButton_13 = QToolButton(self.widget_3)

        # self.toolButton_13.setIcon(icon_dataprovider)
        self.toolButton_13.setIconSize(QSize(25, 25))
        self.toolButton_13.setObjectName("toolButton_13")
        self.horizontalLayout_6.addWidget(self.toolButton_13)
        self.toolButton_16 = QToolButton(self.widget_3)

        # self.toolButton_16.setIcon(icon_sc_autosum)
        self.toolButton_16.setIconSize(QSize(25, 25))
        self.toolButton_16.setObjectName("toolButton_16")
        self.horizontalLayout_6.addWidget(self.toolButton_16)
        self.toolButton_17 = QToolButton(self.widget_3)

        # self.toolButton_17.setIcon(icon_lc_drawchart)
        self.toolButton_17.setIconSize(QSize(25, 25))
        self.toolButton_17.setObjectName("toolButton_17")
        self.horizontalLayout_6.addWidget(self.toolButton_17)
        self.toolButton_14 = QToolButton(self.widget_3)

        # self.toolButton_14.setIcon(icon_lc_statisticsmenu)
        self.toolButton_14.setIconSize(QSize(25, 25))
        self.toolButton_14.setObjectName("toolButton_14")
        self.horizontalLayout_6.addWidget(self.toolButton_14)
        self.toolButton_15 = QToolButton(self.widget_3)

        # self.toolButton_15.setIcon(icon_lc_dbreportedit)
        self.toolButton_15.setIconSize(QSize(25, 25))
        self.toolButton_15.setObjectName("toolButton_15")
        self.horizontalLayout_6.addWidget(self.toolButton_15)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.verticalLayout_6.addWidget(self.widget_3)

        self.graphicsView = QGraphicsView(self)

        self.graphicsView.setFrameShape(QFrame.NoFrame)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout_6.addWidget(self.graphicsView)

        self.toolButton_4.setText(_translate("MainWindow", "..."))
        self.toolButton_3.setText(_translate("MainWindow", "..."))
        self.toolButton_6.setText(_translate("MainWindow", "..."))
        self.toolButton_5.setText(_translate("MainWindow", "..."))
        self.toolButton_2.setText(_translate("MainWindow", "..."))
        self.toolButton.setText(_translate("MainWindow", "..."))
        self.toolButton_7.setText(_translate("MainWindow", "..."))
        self.toolButton_8.setText(_translate("MainWindow", "..."))
        self.toolButton_9.setText(_translate("MainWindow", "..."))
        self.toolButton_10.setText(_translate("MainWindow", "..."))
        self.toolButton_11.setText(_translate("MainWindow", "..."))
        self.toolButton_12.setText(_translate("MainWindow", "..."))
        self.toolButton_13.setText(_translate("MainWindow", "..."))
        self.toolButton_16.setText(_translate("MainWindow", "..."))
        self.toolButton_17.setText(_translate("MainWindow", "..."))
        self.toolButton_14.setText(_translate("MainWindow", "..."))
        self.toolButton_15.setText(_translate("MainWindow", "..."))

        # self.rect = CustomRect()
        # self.rect.setPos(50, 50)
        # self.rect2 = CustomRect()
        # self.rect2.setPos(100, 100)
        #
        self.scene = PMGraphicsScene(graphics_view=self.graphicsView)
        self.scene.setSceneRect(0, 0, 300, 300)
        # self.scene.addItem(self.rect)
        # self.scene.addItem(self.rect2)
        #
        # self.cl = CustomLine()
        # self.cl.start_pos = (0, 30)
        # self.cl.end_pos = (100, 100)
        # self.scene.addItem(self.cl)
        self.n = Node(self.scene)
        self.n2 = Node(self.scene)

        self.graphicsView.setScene(self.scene)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    graphics = PMFlowWidget()
    graphics.show()

    sys.exit(app.exec_())
