import numpy as np
from PySide6.QtCore import QPointF
from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QDialog,
    QGridLayout,
)

from RectangleList import RectangleList


class TransformationHandler(QHBoxLayout):
    def __init__(self, rectangleList: RectangleList):
        super().__init__()
        self.transformationMatrix = np.eye(3)
        self.rectangleList = rectangleList
        for transformation in [
            "Translation",
            "Euclidean",
            "Similarity",
            "Affine",
            "Projective",
        ]:
            button = QPushButton(transformation)
            button.clicked.connect(self.handleButton)
            self.addWidget(button)

    def handleButton(self):
        buttonName = self.sender().text()
        self.showDialog(buttonName)

    def showDialog(self, buttonName):
        dialog = QDialog()
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
                    entry = QLineEdit("0")
                    entries["matrix"].append((entry, i, j))
                    gridLayout.addWidget(entry, i, j)
                else:
                    gridLayout.addWidget(
                        QLabel(str(self.transformationMatrix[i, j])), i, j
                    )

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(dialog.accept)
        buttonBox.rejected.connect(dialog.reject)

        gridLayout.addWidget(buttonBox, 3, 2, 1, 2)

        dialog.setLayout(gridLayout)

        if dialog.exec():
            self.modifyTransformationMatrix(entries)
            self.applyTransformation()

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

    def applyTransformation(self):
        for rectangle in self.rectangleList.checkBoxes.keys():
            checkbox = self.rectangleList.checkBoxes[rectangle]
            if checkbox.isChecked():

                startPoint = rectangle.startPoint
                bottomLeft = rectangle.bottomLeft
                bottomRight = rectangle.bottomRight
                topRight = rectangle.topRight

                vecStartPoint = np.array([startPoint.x(), startPoint.y(), 1])
                vecBottomLeft = np.array([bottomLeft.x(), bottomLeft.y(), 1])
                vecBottomRight = np.array([bottomRight.x(), bottomRight.y(), 1])
                vecTopRight = np.array([topRight.x(), topRight.y(), 1])

                vecStartPoint = np.dot(self.transformationMatrix, vecStartPoint)
                vecBottomLeft = np.dot(self.transformationMatrix, vecBottomLeft)
                vecBottomRight = np.dot(self.transformationMatrix, vecBottomRight)
                vecTopRight = np.dot(self.transformationMatrix, vecTopRight)

                startPoint = QPointF(vecStartPoint[0], vecStartPoint[1]) / vecStartPoint[2]
                bottomLeft = QPointF(vecBottomLeft[0], vecBottomLeft[1]) / vecBottomLeft[2]
                bottomRight = QPointF(vecBottomRight[0], vecBottomRight[1]) / vecBottomRight[2]
                topRight = QPointF(vecTopRight[0], vecTopRight[1]) / vecTopRight[2]

                rectangle.updateRect(startPoint, topRight, bottomRight, bottomLeft)
                self.transformationMatrix = np.eye(3)
