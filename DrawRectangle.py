from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from Rectangle import Rectangle
from RectangleSignalEmitter import RectangleSignalEmitter


class DrawRectangle(QGraphicsView):
    def __init__(self, scene: QGraphicsScene):
        super().__init__(scene)
        self.currentRectangle = None
        self.rectangleSignalEmitter = RectangleSignalEmitter()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            item = self.itemAt(self.mapToScene(event.pos()).toPoint())
            if not item or not isinstance(item, Rectangle):
                startPoint = self.mapToScene(event.pos())
                bottomRight = QPoint(startPoint.x() + 10, startPoint.y() + 10)
                topRight = QPoint(startPoint.x() + 10, startPoint.y())
                bottomLeft = QPoint(startPoint.x(), startPoint.y() + 10)
                self.currentRectangle = Rectangle(startPoint, bottomLeft, bottomRight, topRight)
                self.rectangleSignalEmitter.emitSignal("created", self.currentRectangle)
                self.scene().addItem(self.currentRectangle)
            else:
                super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.currentRectangle:
            endPoint = self.mapToScene(event.pos())
            self.currentRectangle.resize(endPoint)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.currentRectangle = None
        super().mouseReleaseEvent(event)
