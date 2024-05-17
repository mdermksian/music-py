from PySide6.QtCore import QObject, Slot, Property, Signal
from keyboard_model import QKeyboard
from settings import Settings

from threading import Thread, Lock
from typing import Callable, Union
import time
from functools import partial

from sounds import SoundData, SoundGenerator

UPDATE_RATE = 1 / 30  # s
HOLD_DURATION = 2.0  # s


class TickThread:
    def __init__(self, loop_rate: float = UPDATE_RATE):
        self._stop_processing: bool = False
        self._thread: Union[None, Thread] = None
        self._update_rate: float = loop_rate

    def stop(self):
        self._stop_processing = True
        if self._thread is not None:
            self._thread.join()
            self._thread = None

    def start(self, process: Callable):
        self._stop_processing = False
        self._thread = Thread(target=partial(self.__tick, process))
        self._thread.start()

    def __tick(self, process: Callable) -> Callable:
        while not self._stop_processing:
            start_time = time.time()
            process()
            elapsed_time = time.time() - start_time
            time_to_sleep = self._update_rate - elapsed_time
            time.sleep(time_to_sleep if time_to_sleep > 0 else 0)


class Backend(QObject):
    def __init__(self):
        super().__init__()
        self._settings = Settings()
        self._keyboard = QKeyboard()
        self._active_keys_lock = Lock()
        self._active_keys = {}
        self._hold = True
        self._adjustable_volume = False
        self._intensity_processing = TickThread()
        self._sound_generator = SoundGenerator(self.get_sounddata)
        self._sound_generator.start()

    def __del__(self):
        self.cleanup()

    def cleanup(self):
        self._intensity_processing.stop()
        self._sound_generator.stop()

    def get_sounddata(self) -> SoundData:
        with self._active_keys_lock:
            return {
                "frequencies": [
                    value["frequency"] for value in self._active_keys.values()
                ],
                "intensities": [
                    value["intensity"] for value in self._active_keys.values()
                ],
                "phases": [value["phase"] for value in self._active_keys.values()],
            }

    keyboard_changed = Signal()

    @Property(QObject, notify=keyboard_changed)
    def keyboard(self):
        return self._keyboard

    @Slot(str)
    @Slot(str, float)
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
                    "phase": 0,
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
                {
                    "frequency": key["frequency"],
                    "intensity": key["intensity"],
                    "phase": key["phase"],
                }
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
            self._intensity_processing.start(self.intensity_processing_process)
        else:
            self._intensity_processing.stop()

        self.hold_changed.emit()

    adjustable_volume_changed = Signal()

    @Property(bool, notify=adjustable_volume_changed)
    def adjustable_volume(self):
        return self._adjustable_volume

    @Slot()
    def toggle_adjustable_volume(self):
        self._adjustable_volume = not self._adjustable_volume
        self.adjustable_volume_changed.emit()

    @Slot(str, str, result=float)
    def get_active_value(self, note: str, property: str):
        with self._active_keys_lock:
            if not note in self._active_keys:
                return 0.0
            note_data = self._active_keys[note]
            assert property in note_data, "Invalid value"
            return note_data[property]

    def intensity_processing_process(self):
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

    @staticmethod
    def linear_decay(
        value_init: float, elapsed_time_s: int, note_duration: float = HOLD_DURATION
    ) -> float:
        value = value_init * (note_duration - elapsed_time_s) / note_duration
        return value if value > 0 else 0

    settings_changed = Signal()

    @Property(QObject, notify=settings_changed)
    def settings(self):
        return self._settings

    @Slot(int)
    def computer_keypress(self, key: int):
        if key in self._settings.key_map:
            self.submit_keypress(self._settings.key_map[key])
