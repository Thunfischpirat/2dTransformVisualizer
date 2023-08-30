import sys

import numpy as np
from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QAction, Qt
from PySide6.QtWidgets import (QApplication, QCheckBox, QGraphicsScene,
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

        self.scene = QGraphicsScene()
        grid = CartesianGrid(1200, 1000, 10)
        self.scene.addItem(grid)
        self.rectangleSignalEmitter.connect_signal(self.createCheckbox)
        self.view = DrawRectangle(self.scene)

        transformationHandler = TransformationHandler()

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addLayout(transformationHandler)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.dock = RectangleList()
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)
        self.show()

    def createCheckbox(self):
        self.rectangleCount += 1
        checkbox = QCheckBox(f"Rectangle {self.rectangleCount}")
        self.dock.sidebar_layout.addWidget(checkbox)
        self.dock.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
