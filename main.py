import sys
import numpy as np
from PySide6.QtGui import QAction, Qt
from PySide6.QtWidgets import (
    QApplication,
    QGraphicsScene,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QMenu,
    QHBoxLayout,
    QPushButton,
    QDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QDialogButtonBox, QDockWidget, QCheckBox,
)

from DrawRectangle import DrawRectangle, RectangleSignalEmitter
from CartesianGrid import CartesianGrid


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
        self.rectangleSignalEmitter.rectangle.connect(self.handleCheckbox)
        self.view = DrawRectangle(self.scene, self.rectangleSignalEmitter)
        self.transformationMatrix = np.eye(3)

        # Create buttons for transformations
        transformationLayout = QHBoxLayout()
        for transformation in [
            "Translation",
            "Euclidean",
            "Similarity",
            "Affine",
            "Projective",
        ]:
            button = QPushButton(transformation)
            button.clicked.connect(self.handleButton)
            transformationLayout.addWidget(button)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addLayout(transformationLayout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.dock = QDockWidget("Rectangles", self)
        self.dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.dock.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)
        self.sidebar_layout = QVBoxLayout()
        self.sidebar_widget = QWidget()
        self.sidebar_widget.setMinimumWidth(150)
        self.sidebar_widget.setLayout(self.sidebar_layout)
        self.dock.setWidget(self.sidebar_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)
        self.show()

    def handleButton(self):
        buttonName = self.sender().text()
        self.showDialog(buttonName)

    def showDialog(self, buttonName):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Specify Matrix for {buttonName}-Transformation")
        gridLayout = QGridLayout()

        entries = {"matrix": [], "angle": None, "scale": None}
        iVals, jVals = [], []
        if buttonName == "Translation":
            iVals, jVals = [0, 1], [2]

        elif buttonName == "Euclidean":
            entry_angle = QLineEdit()
            entries["angle"] = entry_angle
            gridLayout.addWidget(QLabel("Angle:"), 0, 3)
            gridLayout.addWidget(entry_angle, 0, 4)

            iVals, jVals = [0, 1], [2]

        elif buttonName == "Similarity":
            entry_angle = QLineEdit()
            entries["angle"] = entry_angle
            gridLayout.addWidget(QLabel("Angle:"), 0, 3)
            gridLayout.addWidget(entry_angle, 0, 4)

            entry_scale = QLineEdit()
            entries["scale"] = entry_scale
            gridLayout.addWidget(QLabel("Scale:"), 1, 3)
            gridLayout.addWidget(entry_scale, 1, 4)

            iVals, jVals = [0, 1], [2]

        elif buttonName == "Affine":
            iVals, jVals = [0, 1], [0, 1, 2]

        elif buttonName == "Projective":
            iVals, jVals = [0, 1, 2], [0, 1, 2]

        for i in range(3):
            for j in range(3):
                if (i in iVals) and (j in jVals):
                    entry = QLineEdit()
                    entries["matrix"].append((entry, i, j))
                    gridLayout.addWidget(entry, i, j)
                else:
                    gridLayout.addWidget(QLabel(str(self.transformationMatrix[i, j])), i, j)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(dialog.accept)
        buttonBox.rejected.connect(dialog.reject)

        gridLayout.addWidget(buttonBox, 3, 2, 1, 2)

        dialog.setLayout(gridLayout)

        if dialog.exec():
            self.modifyTransformationMatrix(entries)

    def modifyTransformationMatrix(self, entries: dict):
        if entries["angle"] is not None:
            angle = float(entries["angle"].text())
            angle = np.deg2rad(angle)
            self.transformationMatrix = np.array(
                [
                    [np.cos(angle), -np.sin(angle), 0],
                    [np.sin(angle), np.cos(angle), 0],
                    [0, 0, 1],
                ]
            )
        if entries["scale"] is not None:
            scale = float(entries["scale"].text())
            self.transformationMatrix[:2, :2] *= scale

        for entry, i, j in entries["matrix"]:
            self.transformationMatrix[i, j] = float(entry.text())

    def handleCheckbox(self):
        self.rectangleCount += 1
        checkbox = QCheckBox(f"Rectangle {self.rectangleCount}")
        self.sidebar_layout.addWidget(checkbox)
        self.dock.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
