from PySide6.QtCore import QObject, Property, Signal, Slot


class Settings(QObject):
    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._hold = True

    hold_changed = Signal()

    @Property(bool, notify=hold_changed)
    def hold(self):
        return self._hold

    @Slot()
    def toggle_hold(self):
        self._hold = not self._hold
        self.hold_changed.emit()
