from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
# from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication
from qtpy.QtWidgets import QVBoxLayout,QWidget,QApplication
import sys
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from matplotlib.axes._subplots import Axes


class PMMatplotlibQt5Widget(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.figure = plt.figure(facecolor='#FFD7C4')  # 可选参数,facecolor为背景颜色
        self.canvas = FigureCanvasQTAgg(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def add_subplot(self, param) -> 'Axes':
        return self.figure.add_subplot(param)

    def draw(self)->None:
        self.canvas.draw()
