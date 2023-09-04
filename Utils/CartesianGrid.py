from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtGui import QPen
from PySide6.QtCore import Qt, QRectF


class CartesianGrid(QGraphicsItem):
    """Draws a Cartesian grid on the scene"""
    def __init__(self, width, height, cellSize):
        super().__init__()
        self.width = width
        self.height = height
        self.cellSize = cellSize

    def boundingRect(self):
        return QRectF(-self.width/2, -self.height/2, self.width, self.height)

    def paint(self, painter, option, widget):
        left, right, top, bottom = -self.width/2, self.width/2, -self.height/2, self.height/2
        for x in range(int(left), int(right), self.cellSize):
            painter.setPen(Qt.lightGray)
            painter.drawLine(x, top, x, bottom)

        for y in range(int(top), int(bottom), self.cellSize):
            painter.setPen(Qt.lightGray)
            painter.drawLine(left, y, right, y)

        axesPen = QPen(Qt.black)
        axesPen.setWidth(1)
        painter.setPen(axesPen)
        painter.drawLine(left, 0, right, 0)
        painter.drawLine(0, top, 0, bottom)

