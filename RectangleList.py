from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QCheckBox, QSpacerItem, QSizePolicy


class RectangleList(QDockWidget):
    def __init__(self):
        super().__init__("Rectangles")
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)
        self.sidebar_layout = QVBoxLayout()

        verticalSpacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.sidebar_layout.addSpacerItem(verticalSpacer)

        self.sidebar_widget = QWidget()
        self.sidebar_widget.setMinimumWidth(150)
        self.sidebar_widget.setLayout(self.sidebar_layout)
        self.setWidget(self.sidebar_widget)
        self.checkBoxes = {}

    def createCheckbox(self, rectangle):
        # The spacer item from the constructor counts as one item.
        numRectangles = self.sidebar_layout.count()
        checkboxId = f"Rectangle {numRectangles}"
        checkbox = QCheckBox(checkboxId)
        self.checkBoxes[rectangle] = checkbox
        self.sidebar_layout.insertWidget(self.sidebar_layout.count() - 1, checkbox)
        self.sidebar_layout.update()
        self.update()

    def deleteCheckbox(self, rectangle):
        checkbox = self.checkBoxes[rectangle]
        self.sidebar_layout.removeWidget(checkbox)
        checkbox.deleteLater()
        self.sidebar_layout.update()
        self.update()
