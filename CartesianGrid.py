from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt, QRectF


class CartesianGrid(QGraphicsItem):
    def __init__(self, width, height, cellSize):
        super().__init__()
        self.width = width
        self.height = height
        self.cellSize = cellSize

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    def paint(self, painter, option, widget):
        left, right, top, bottom = 0, self.width, 0, self.height
        for x in range(left, right, self.cellSize):
            painter.setPen(Qt.lightGray)
            painter.drawLine(x, top, x, bottom)

        for y in range(top, bottom, self.cellSize):
            painter.setPen(Qt.lightGray)
            painter.drawLine(left, y, right, y)

        axesPen = QPen(Qt.black)
        axesPen.setWidth(1)
        painter.setPen(axesPen)
        painter.drawLine(left, self.height/2, right, self.height/2)  # X-axis
        painter.drawLine(self.width/2, top, self.width/2, bottom)    # Y-axis

