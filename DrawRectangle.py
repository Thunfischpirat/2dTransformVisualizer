from PySide6.QtCore import Qt, Signal, QObject
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from Rectangle import Rectangle


class RectangleSignalEmitter(QObject):
    rectangle = Signal()


class DrawRectangle(QGraphicsView):
    def __init__(self, scene: QGraphicsScene, signalEmitter: RectangleSignalEmitter):
        super().__init__(scene)
        self.currentRectangle = None
        self.rectangle_signal_emitter = signalEmitter

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            item = self.itemAt(self.mapToScene(event.pos()).toPoint())
            if not item or not isinstance(item, Rectangle):
                startPoint = self.mapToScene(event.pos())
                self.currentRectangle = Rectangle(startPoint)
                self.rectangle_signal_emitter.rectangle.emit()
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
