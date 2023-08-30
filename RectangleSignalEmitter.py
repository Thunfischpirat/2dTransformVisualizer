from PySide6.QtCore import QObject, Signal


class SignalHolder(QObject):
    rectangle_created = Signal()


class RectangleSignalEmitter:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RectangleSignalEmitter, cls).__new__(cls)
            cls._instance.signal_holder = SignalHolder()
        return cls._instance

    def connect_signal(self, slot_function):
        self.signal_holder.rectangle_created.connect(slot_function)

    def emit_signal(self):
        self.signal_holder.rectangle_created.emit()
