from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from Rectangle import Rectangle
from RectangleSignalEmitter import RectangleSignalEmitter


class DrawRectangle(QGraphicsView):
    def __init__(self, scene: QGraphicsScene):
        super().__init__(scene)
        self.currentRectangle = None
        self.rectangle_signal_emitter = RectangleSignalEmitter()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            item = self.itemAt(self.mapToScene(event.pos()).toPoint())
            if not item or not isinstance(item, Rectangle):
                startPoint = self.mapToScene(event.pos())
                self.currentRectangle = Rectangle(startPoint)
                self.rectangle_signal_emitter.emitSignal("created", self.currentRectangle)
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
