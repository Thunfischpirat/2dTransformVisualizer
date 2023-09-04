from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QCheckBox, QSpacerItem, QSizePolicy


class RectangleList(QDockWidget):
    """
    This class is responsible for the sidebar on the left side of the application.
    It contains a list of all rectangles that have been created so far. Each rectangle
    has a checkbox next to it, which can be used to select the rectangle. The sidebar
    is updated whenever a new rectangle is created or deleted.
    """
    def __init__(self):
        super().__init__("Rectangles")
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)
        self.sidebarLayout = QVBoxLayout()

        verticalSpacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.sidebarLayout.addSpacerItem(verticalSpacer)

        self.sidebarWidget = QWidget()
        self.sidebarWidget.setMinimumWidth(150)
        self.sidebarWidget.setLayout(self.sidebarLayout)
        self.setWidget(self.sidebarWidget)
        self.checkBoxes = {}

    def createCheckbox(self, rectangle):
        numRectangles = self.sidebarLayout.count()
        checkboxId = f"Rectangle {numRectangles}"
        checkbox = QCheckBox(checkboxId)
        self.checkBoxes[rectangle] = checkbox
        self.sidebarLayout.insertWidget(numRectangles - 1, checkbox)
        self.sidebarLayout.update()
        self.update()

    def deleteCheckbox(self, rectangle):
        checkbox = self.checkBoxes[rectangle]
        del self.checkBoxes[rectangle]
        self.sidebarLayout.removeWidget(checkbox)
        checkbox.deleteLater()
        self.sidebarLayout.update()
        self.update()
