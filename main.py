import sys

from PySide6.QtGui import QAction, Qt
from PySide6.QtWidgets import (QApplication, QGraphicsScene,
                               QMainWindow, QMenu, QVBoxLayout,
                               QWidget)

from CartesianGrid import CartesianGrid
from DrawRectangle import DrawRectangle
from RectangleList import RectangleList
from RectangleSignalEmitter import RectangleSignalEmitter
from TransformationHandler import TransformationHandler


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1200, 1000)

        self.rectangleSignalEmitter = RectangleSignalEmitter()
        self.rectangleCount = 0

        menubar = self.menuBar()
        fileMenu = QMenu("File", self)
        exitAction = QAction("Exit", self)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)
        menubar.addMenu(fileMenu)

        self.dock = RectangleList()
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)

        self.scene = QGraphicsScene()
        grid = CartesianGrid(1200, 1000, 10)
        self.scene.addItem(grid)
        self.rectangleSignalEmitter.connectSignalCreated(self.dock.createCheckbox)
        self.rectangleSignalEmitter.connectSignalDeleted(self.dock.deleteCheckbox)
        self.view = DrawRectangle(self.scene)

        transformationHandler = TransformationHandler(self.dock)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addLayout(transformationHandler)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
