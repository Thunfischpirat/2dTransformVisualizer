from PySide6.QtCore import QObject, Signal


class SignalHolder(QObject):
    rectangleCreated = Signal(object)
    rectangleDeleted = Signal(object)


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

    def emitSignal(self, action: str, rectangle=None):
        if action == "created":
            self.signal_holder.rectangleCreated.emit(rectangle)
        elif action == "deleted":
            self.signal_holder.rectangleDeleted.emit(rectangle)
