from PySide6.QtCore import QObject, Slot, Property, Signal
from keyboard_model import QKeyboard
from settings import Settings

from threading import Thread, Lock
import time

UPDATE_RATE = 1 / 30  # s
HOLD_DURATION = 2.0  # s


class Backend(QObject):
    def __init__(self):
        super().__init__()
        self._settings = Settings()
        self._keyboard = QKeyboard()
        self._active_keys_lock = Lock()
        self._active_keys = {}
        self._hold = True
        self._stop_processing = False
        self._intensity_processing_thread = None

    def __del__(self):
        self.cleanup()

    def cleanup(self):
        if self._intensity_processing_thread is not None:
            self._stop_processing = True
            self._intensity_processing_thread.join()

    keyboard_changed = Signal()

    @Property(QObject, notify=keyboard_changed)
    def keyboard(self):
        return self._keyboard

    @Slot(str)
    def submit_keypress(self, key: str, intensity: float = 1.0):
        assert (
            intensity >= 0.0 and intensity <= 1.0
        ), "Intensity must be between 0 and 1"
        with self._active_keys_lock:
            if key not in self._active_keys or not self._hold:
                self._active_keys[key] = {
                    "intensity": intensity,
                    "frequency": self._keyboard.get_frequency(key),
                    "intensity_initial": intensity,
                    "press_time": time.time(),
                }
            else:
                del self._active_keys[key]
        self.active_keys_changed.emit()

    active_keys_changed = Signal()

    @Property(list, notify=active_keys_changed)
    def active_keys(self):
        with self._active_keys_lock:
            return list(self._active_keys.keys())

    @Property(list, notify=active_keys_changed)
    def active_notes(self):
        with self._active_keys_lock:
            return [
                {"frequency": key["frequency"], "intensity": key["intensity"]}
                for key in self._active_keys.values()
            ]

    hold_changed = Signal()

    @Property(bool, notify=hold_changed)
    def hold(self):
        return self._hold

    @Slot()
    def toggle_hold(self):
        self._hold = not self._hold
        if not self._hold:
            self._stop_processing = False
            self._intensity_processing_thread = Thread(
                target=self.intensity_processing_process
            )
            self._intensity_processing_thread.start()
        else:
            self._stop_processing = True
            self._intensity_processing_thread.join()
            self._intensity_processing_thread = None

        self.hold_changed.emit()

    def intensity_processing_process(self):
        print("Starting process")
        while not self._stop_processing:
            start_time = time.time()
            with self._active_keys_lock:
                keys_to_remove = []
                for key in self._active_keys.keys():
                    key_data = self._active_keys[key]
                    elapsed_time = start_time - key_data["press_time"]
                    self._active_keys[key]["intensity"] = self.linear_decay(
                        key_data["intensity_initial"], elapsed_time
                    )
                    if self._active_keys[key]["intensity"] <= 0:
                        keys_to_remove.append(key)
                for key in keys_to_remove:
                    del self._active_keys[key]
            self.active_keys_changed.emit()
            elapsed_time = time.time() - start_time
            time_to_sleep = UPDATE_RATE - elapsed_time
            time.sleep(time_to_sleep if time_to_sleep > 0 else 0)
        print("Ending process")

    @staticmethod
    def linear_decay(
        value_init: float, elapsed_time_s: int, slope: float = 0.5
    ) -> float:
        value = value_init - elapsed_time_s * slope
        return value if value > 0 else 0

    settings_changed = Signal()

    @Property(QObject, notify=settings_changed)
    def settings(self):
        return self._settings

    @Slot(int)
    def computer_keypress(self, key: int):
        if key in self._settings.key_map:
            self.submit_keypress(self._settings.key_map[key])
