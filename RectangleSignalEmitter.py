from PySide6.QtCore import QObject, Signal


class SignalHolder(QObject):
    rectangleCreated = Signal()
    rectangleDeleted = Signal()


class RectangleSignalEmitter:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RectangleSignalEmitter, cls).__new__(cls)
            cls._instance.signal_holder = SignalHolder()
        return cls._instance

    def connectSignalCreated(self, slot_function):
        self.signal_holder.rectangleCreated.connect(slot_function)

    def connectSignalDeleted(self, slot_function):
        self.signal_holder.rectangleDeleted.connect(slot_function)

    def emit_signal(self, action: str):
        if action == "create":
            self.signal_holder.rectangleCreated.emit()
        elif action == "delete":
            self.signal_holder.rectangleDeleted.emit()
