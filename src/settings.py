from PySide6.QtCore import QObject, Property, Signal, Slot


class Settings(QObject):
    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
