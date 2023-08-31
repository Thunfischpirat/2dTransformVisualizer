from PySide6.QtWidgets import QMenu, QGraphicsPolygonItem
from PySide6.QtCore import QPoint
from PySide6.QtGui import QBrush, QColor, QAction, QPolygonF

from RectangleSignalEmitter import RectangleSignalEmitter


class Rectangle(QGraphicsPolygonItem):
    def __init__(
        self,
        startPoint: QPoint,
        bottomLeft: QPoint,
        bottomRight: QPoint,
        topRight: QPoint,
    ):
        super().__init__(QPolygonF([startPoint, topRight, bottomRight, bottomLeft]))
        self.startPoint = startPoint
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight
        self.topRight = topRight
        self.signalEmitter = RectangleSignalEmitter()
        self.setBrush(QBrush(QColor(255, 0, 0, 127)))
        self.setFlag(QGraphicsPolygonItem.ItemIsSelectable, True)

    def resize(self, endPoint: QPoint):
        x1, y1 = self.startPoint.x(), self.startPoint.y()
        self.startPoint = QPoint(min(x1, endPoint.x()), min(y1, endPoint.y()))
        self.bottomLeft = QPoint(min(x1, endPoint.x()), max(y1, endPoint.y()))
        self.bottomRight = QPoint(max(x1, endPoint.x()), max(y1, endPoint.y()))
        self.topRight = QPoint(max(x1, endPoint.x()), min(y1, endPoint.y()))
        rect = QPolygonF([self.startPoint, self.topRight, self.bottomRight, self.bottomLeft])
        self.setPolygon(rect)

    def contextMenuEvent(self, event):
        contextMenu = QMenu()
        deleteAction = QAction("Delete", contextMenu)
        deleteAction.triggered.connect(self.delete)
        moveAction = QAction("Move", contextMenu)
        moveAction.triggered.connect(self.enableMove)
        contextMenu.addAction(deleteAction)
        contextMenu.addAction(moveAction)
        contextMenu.exec(event.screenPos())

    def enableMove(self):
        self.setFlag(QGraphicsPolygonItem.ItemIsMovable, True)
        self.setBrush(QBrush(QColor(0, 255, 0, 127)))

    def disableMove(self):
        self.setFlag(QGraphicsPolygonItem.ItemIsMovable, False)
        self.setBrush(QBrush(QColor(255, 0, 0, 127)))

    def hoverEnterEvent(self, event):
        self.enableMove()

    def hoverLeaveEvent(self, event):
        self.disableMove()

    def mouseReleaseEvent(self, event):
        self.disableMove()

    def delete(self):
        self.signalEmitter.emitSignal("deleted", self)
        self.scene().removeItem(self)
