from PySide6.QtCore import QObject, Slot, Property, Signal
from keyboard_model import QKeyboard
from settings import Settings

import time


class Backend(QObject):
    def __init__(self):
        super().__init__()
        self._settings = Settings()
        self._keyboard = QKeyboard()
        self._active_keys = []
        self._active_frequencies = []

    keyboard_changed = Signal()

    @Property(QObject, notify=keyboard_changed)
    def keyboard(self):
        return self._keyboard

    @Slot(str)
    def submit_keypress(self, key: str, intensity: float = 1.0):
        if key not in self._active_keys:
            self._active_keys.append(key)
            self._active_frequencies.append(self._keyboard.get_frequency(key))
        else:
            self._active_keys.remove(key)
            self._active_frequencies.remove(self._keyboard.get_frequency(key))
        self.active_keys_changed.emit()
        self.active_frequencies_changed.emit()

    active_keys_changed = Signal()

    @Property(list, notify=active_keys_changed)
    def active_keys(self):
        return self._active_keys

    active_frequencies_changed = Signal()

    @Property(list, notify=active_frequencies_changed)
    def active_frequencies(self):
        return self._active_frequencies

    settings_changed = Signal()

    @Property(QObject, notify=settings_changed)
    def settings(self):
        return self._settings
