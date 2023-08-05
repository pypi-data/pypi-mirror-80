from PyQt5.QtCore import QLineF, QPointF, Qt, QRectF, pyqtSignal
from PyQt5.QtGui import QPolygonF, QPen, QPainterPath, QColor, QPainter, QBrush
from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsItem, QGraphicsSceneMouseEvent, QGraphicsObject, \
    QStyleOptionGraphicsItem, QWidget

COLOR_NORMAL = QColor(212, 227, 242)
COLOR_HOVER = QColor(255, 200, 00)
COLOR_HOVER_PORT = QColor(0, 0, 50)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .flowchart_widget import Node


class CustomLine(QGraphicsLineItem):
    '''
    CustomLine不是QObject，没有办法绑定信号，只能用回调函数的方式。
    '''
    repaint_callback = None

    def __init__(self, start_port: 'CustomPort', end_port: 'CustomPort', canvas: 'PMGraphicsScene' = None):
        super(CustomLine, self).__init__()
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)  # 拖动
        self.start_port = start_port
        self.end_port = end_port
        self.center_points = [CustomCenterPoint(self)]

        # self.center_point =
        for p in self.center_points:
            canvas.addItem(p)
        # map(canvas.addItem,self.center_points)
        center_point = self.center_points[0]
        center_point.setPos(self.start_port.x(), self.end_port.y())
        center_point.point_dragged.connect(self.refresh)

        self.refresh()
        self.canvas = canvas

    def refresh(self):
        self.setLine(QLineF(self.start_port.center_pos, self.end_port.center_pos))
        self.update()

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        print('mouse clicked!!')

    def draw_arrow(self, QPainter, point_1: QPointF, point_2: QPointF) -> 'QPolygonF':

        l = QLineF(point_1, point_2)
        v = l.unitVector()

        v.setLength(20)  # 改变单位向量的大小，实际就是改变箭头长度
        v.translate(QPointF(int(l.dx() / 2), int(l.dy() / 2)))

        n = v.normalVector()  # 法向量
        n.setLength(n.length() * 0.2)  # 这里设定箭头的宽度
        n2 = n.normalVector().normalVector()  # 两次法向量运算以后，就得到一个反向的法向量
        p1 = v.p2()
        p2 = n.p2()
        p3 = n2.p2()
        QPainter.drawPolygon(p1, p2, p3)
        return QPolygonF([p1, p2, p3, p1])

    def paint(self, q_painter:'QPainter', style_option_graphics_item:'QStyleOptionGraphicsItem', widget:'QWidget'=None):
        # setPen
        pen = QPen()
        pen.setWidth(5)
        pen.setJoinStyle(Qt.MiterJoin)  # 让箭头变尖
        q_painter.setPen(pen)

        path = QPainterPath()

        point1 = self.start_port
        path.moveTo(self.start_port.center_pos)
        for p in self.center_points + [self.end_port]:
            q_painter.drawLine(QLineF(point1.center_pos, p.center_pos))
            arrow = self.draw_arrow(q_painter, point1.center_pos, p.center_pos)
            path.addPolygon(arrow)
            point1 = p

        if self.repaint_callback is not None:
            self.repaint_callback()


class CustomCenterPoint(QGraphicsObject):
    point_dragged = pyqtSignal(QGraphicsObject)

    def __init__(self, line: 'CustomLine'):
        super(CustomCenterPoint, self).__init__()
        # self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)  # 拖动
        self.setAcceptHoverEvents(True)  # 接受鼠标悬停事件
        self.relative_pos = (0, 0)
        self.color = COLOR_NORMAL
        self.size = (10, 10)
        self.line = line

    def boundingRect(self):
        return QRectF(0, 0, self.size[0], self.size[1])

    @property
    def center_pos(self):
        return QPointF(self.x() + self.size[0] / 2, self.y() + self.size[1] / 2)

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        mouse_x, mouse_y = event.scenePos().x(), event.scenePos().y()
        self.setPos(QPointF(mouse_x, mouse_y))
        self.point_dragged.emit(self)
        print('dr')

    def paint(self, painter, styles, widget=None):
        pen1 = QPen(Qt.SolidLine)
        pen1.setColor(QColor(128, 128, 128))
        painter.setPen(pen1)

        brush1 = QBrush(Qt.SolidPattern)
        brush1.setColor(self.color)
        painter.setBrush(brush1)

        painter.setRenderHint(QPainter.Antialiasing)  # 反锯齿
        painter.drawRoundedRect(self.boundingRect(), 10, 10)

    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        self.color = COLOR_HOVER_PORT

        self.update()

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        self.color = COLOR_NORMAL
        self.update()

    def mousePressEvent(self, evt: QGraphicsSceneMouseEvent):
        print('clicked on port')
        if evt.button() == Qt.LeftButton:
            print("左键被按下")
            pos = (evt.scenePos().x(), evt.scenePos().y())
            # print(self.x(), type(self.x()), type(pos[1]))
            self.relative_pos = (pos[0] - self.x(), pos[1] - self.y())

        elif evt.button() == Qt.RightButton:
            print("左键被按下")
        elif evt.button() == Qt.MidButton:
            print("中间键被按下")

    def paintEvent(self, QPaintEvent):
        pen1 = QPen()
        pen1.setColor(QColor(166, 66, 250))
        painter = QPainter(self)
        painter.setPen(pen1)
        painter.begin(self)
        painter.drawRoundedRect(self.boundingRect(), 10, 10)  # 绘制函数
        painter.end()


class CustomPort(QGraphicsObject):
    port_clicked = pyqtSignal(QGraphicsObject)

    def __init__(self, port_id: int):
        super(CustomPort, self).__init__()
        self.setAcceptHoverEvents(True)  # 接受鼠标悬停事件
        self.relative_pos = (0, 0)
        self.color = COLOR_NORMAL
        self.id = port_id
        self.size = (10, 10)

    def boundingRect(self):
        return QRectF(0, 0, self.size[0], self.size[1])

    @property
    def center_pos(self):
        return QPointF(self.x() + self.size[0] / 2, self.y() + self.size[1] / 2)

    def paint(self, painter, styles, widget=None):
        pen1 = QPen(Qt.SolidLine)
        pen1.setColor(QColor(128, 128, 128))
        painter.setPen(pen1)

        brush1 = QBrush(Qt.SolidPattern)
        brush1.setColor(self.color)
        painter.setBrush(brush1)

        painter.setRenderHint(QPainter.Antialiasing)  # 反锯齿
        painter.drawRoundedRect(self.boundingRect(), 10, 10)

    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        self.color = COLOR_HOVER_PORT

        self.update()

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        self.color = COLOR_NORMAL
        self.update()

    def mousePressEvent(self, evt: QGraphicsSceneMouseEvent):
        print('clicked on port')
        if evt.button() == Qt.LeftButton:
            print("左键被按下")
            pos = (evt.scenePos().x(), evt.scenePos().y())
            self.relative_pos = (pos[0] - self.x(), pos[1] - self.y())
            # print(self.relative_pos)
            self.port_clicked.emit(self)
        elif evt.button() == Qt.RightButton:
            print("左键被按下")
        elif evt.button() == Qt.MidButton:
            print("中间键被按下")

    def paintEvent(self, QPaintEvent):
        pen1 = QPen()
        pen1.setColor(QColor(166, 66, 250))
        painter = QPainter(self)
        painter.setPen(pen1)
        painter.begin(self)
        painter.drawRoundedRect(self.boundingRect(), 10, 10)  # 绘制函数
        painter.end()


class CustomRect(QGraphicsObject):
    def __init__(self, node: 'Node' = None):
        super(CustomRect, self).__init__()
        # self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)  # 拖动
        self.setAcceptHoverEvents(True)  # 接受鼠标悬停事件
        self.relative_pos = (0, 0)
        self.color = COLOR_NORMAL
        self.node = node

    def boundingRect(self):
        return QRectF(0, 0, 200, 50)

    def paint(self, painter, styles, widget=None):
        pen1 = QPen(Qt.SolidLine)
        pen1.setColor(QColor(128, 128, 128))
        painter.setPen(pen1)

        brush1 = QBrush(Qt.SolidPattern)
        brush1.setColor(self.color)
        painter.setBrush(brush1)

        painter.setRenderHint(QPainter.Antialiasing)  # 反锯齿
        painter.drawRoundedRect(self.boundingRect(), 10, 10)

    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        self.color = COLOR_HOVER
        self.update()
        print('enter')

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        self.color = COLOR_NORMAL
        self.update()

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.setPos(event.scenePos().x() - self.relative_pos[0], event.scenePos().y() - self.relative_pos[1])
        self.node.refresh_pos()

    def mousePressEvent(self, evt: QGraphicsSceneMouseEvent):
        print('鼠标按下')
        if evt.button() == Qt.LeftButton:
            print("左键被按下")
            pos = (evt.scenePos().x(), evt.scenePos().y())
            print(self.x(), type(self.x()), type(pos[1]))
            self.relative_pos = (pos[0] - self.x(), pos[1] - self.y())
            print(self.relative_pos)
        elif evt.button() == Qt.RightButton:
            print("左键被按下")
        elif evt.button() == Qt.MidButton:
            print("中间键被按下")

    def paintEvent(self, QPaintEvent):
        pen1 = QPen()
        pen1.setColor(QColor(166, 66, 250))
        painter = QPainter(self)
        painter.setPen(pen1)
        painter.begin(self)
        painter.drawRoundedRect(self.boundingRect(), 10, 10)  # 绘制函数
        painter.end()
