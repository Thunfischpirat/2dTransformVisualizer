from PySide6.QtWidgets import QGraphicsRectItem, QMenu
from PySide6.QtCore import QRectF, QPoint
from PySide6.QtGui import QBrush, QColor, QAction

from RectangleSignalEmitter import RectangleSignalEmitter


class Rectangle(QGraphicsRectItem):
    def __init__(self, startPoint: QPoint):
        super().__init__(QRectF(startPoint.x(), startPoint.y(), 0, 0))
        self.startPoint = startPoint
        self.signalEmitter = RectangleSignalEmitter()
        self.setBrush(QBrush(QColor(255, 0, 0, 127)))
        self.setFlag(QGraphicsRectItem.ItemIsSelectable, True)

    def resize(self, endPoint: QPoint):
        x1, y1 = self.startPoint.x(), self.startPoint.y()
        x2, y2 = endPoint.x(), endPoint.y()
        rect = QRectF(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        self.setRect(rect)

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
        self.setFlag(QGraphicsRectItem.ItemIsMovable, True)
        self.setBrush(QBrush(QColor(0, 255, 0, 127)))

    def disableMove(self):
        self.setFlag(QGraphicsRectItem.ItemIsMovable, False)
        self.setBrush(QBrush(QColor(255, 0, 0, 127)))

    def hoverEnterEvent(self, event):
        self.enableMove()

    def hoverLeaveEvent(self, event):
        self.disableMove()

    def mouseReleaseEvent(self, event):
        self.disableMove()

    def delete(self):
        self.scene().removeItem(self)


