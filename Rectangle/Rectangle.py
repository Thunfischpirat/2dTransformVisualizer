from PySide6.QtCore import QPointF
from PySide6.QtGui import QAction, QBrush, QColor, QPolygonF
from PySide6.QtWidgets import QGraphicsPolygonItem, QMenu
from Rectangle.RectangleSignalEmitter import RectangleSignalEmitter


class Rectangle(QGraphicsPolygonItem):
    """A rectangle that can be drawn on the scene."""
    def __init__(
        self,
        startPoint: QPointF,
        bottomLeft: QPointF,
        bottomRight: QPointF,
        topRight: QPointF,
    ):
        super().__init__(QPolygonF([startPoint, topRight, bottomRight, bottomLeft]))
        self.startPoint = startPoint
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight
        self.topRight = topRight
        self.signalEmitter = RectangleSignalEmitter()
        self.setBrush(QBrush(QColor(255, 0, 0, 127)))
        self.setFlag(QGraphicsPolygonItem.ItemIsSelectable, True)

    def resize(self, endPoint: QPointF):
        x1, y1 = self.startPoint.x(), self.startPoint.y()
        self.startPoint = QPointF(min(x1, endPoint.x()), min(y1, endPoint.y()))
        self.bottomLeft = QPointF(min(x1, endPoint.x()), max(y1, endPoint.y()))
        self.bottomRight = QPointF(max(x1, endPoint.x()), max(y1, endPoint.y()))
        self.topRight = QPointF(max(x1, endPoint.x()), min(y1, endPoint.y()))
        rect = QPolygonF(
            [self.startPoint, self.topRight, self.bottomRight, self.bottomLeft]
        )
        self.setPolygon(rect)

    def updateRect(
        self,
        startPoint: QPointF,
        bottomLeft: QPointF,
        bottomRight: QPointF,
        topRight: QPointF,
    ):
        self.startPoint = startPoint
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight
        self.topRight = topRight
        rect = QPolygonF(
            [self.startPoint, self.topRight, self.bottomRight, self.bottomLeft]
        )
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

    def updateCoordinates(self):
        new_pos = self.pos()
        self.startPoint += new_pos
        self.bottomLeft += new_pos
        self.bottomRight += new_pos
        self.topRight += new_pos
        rect = QPolygonF(
            [self.startPoint, self.topRight, self.bottomRight, self.bottomLeft]
        )
        self.setPolygon(rect)
        self.setPos(0, 0)

    def enableMove(self):
        self.setFlag(QGraphicsPolygonItem.ItemIsMovable, True)
        self.setBrush(QBrush(QColor(0, 255, 0, 127)))

    def disableMove(self):
        self.updateCoordinates()
        self.setFlag(QGraphicsPolygonItem.ItemIsMovable, False)
        self.setBrush(QBrush(QColor(255, 0, 0, 127)))

    def mouseReleaseEvent(self, event):
        self.disableMove()

    def delete(self):
        self.signalEmitter.emitSignal("deleted", self)
        self.scene().removeItem(self)
