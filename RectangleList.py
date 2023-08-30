from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QCheckBox


class RectangleList(QDockWidget):
    def __init__(self):
        super().__init__("Rectangles")
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)
        self.sidebar_layout = QVBoxLayout()
        self.sidebar_widget = QWidget()
        self.sidebar_widget.setMinimumWidth(150)
        self.sidebar_widget.setLayout(self.sidebar_layout)
        self.setWidget(self.sidebar_widget)
        self.countRectangles = 0

    def handleCheckbox(self):
        self.countRectangles += 1
        checkbox = QCheckBox(f"Rectangle {self.countRectangles}")
        self.sidebar_layout.addWidget(checkbox)
        self.update()
