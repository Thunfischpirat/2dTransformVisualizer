import numpy as np
from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QDialog,
    QGridLayout,
)


class TransformationHandler(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.transformationMatrix = np.eye(3)
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
                    entry = QLineEdit()
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
