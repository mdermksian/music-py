import typing
from PySide6.QtCore import QObject, Property, Signal

NOTES = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]


def note_to_frequency(note: str, octave: int, A4=440):
    note_ind = NOTES.index(note)

    distance_from_A4 = note_ind + 12 * (octave - (4 if note_ind < 3 else 5))

    return A4 * 2 ** (distance_from_A4 / 12)


class Note:
    def __init__(self, note: str, octave: int):
        assert note in NOTES, "Invalid note letter"
        self.note = note
        self.octave = octave

    def __str__(self):
        return f"{self.note}{self.octave}"


class Keyboard:
    KEYBOARD_SEQUENCE = [
        "C",
        "C#",
        "D",
        "D#",
        "E",
        "F",
        "F#",
        "G",
        "G#",
        "A",
        "A#",
        "B",
    ]

    def __init__(self):
        self.keys = []
        self.note_names = []
        for octave in range(9):
            start_ind = 0
            end_ind = None
            if octave == 0:
                start_ind = self.KEYBOARD_SEQUENCE.index("A")
            elif octave == 8:
                end_ind = self.KEYBOARD_SEQUENCE.index("C") + 1
            for key in self.KEYBOARD_SEQUENCE[start_ind:end_ind]:
                note = Note(key, octave)
                self.keys.append(note)
                self.note_names.append(str(note))

        self.frequencies = {
            str(key): note_to_frequency(key.note, key.octave) for key in self.keys
        }


class QKeyboard(QObject):
    def __init__(self):
        super().__init__()
        self._keyboard = Keyboard()

    keysChanged = Signal()

    @Property(list, notify=keysChanged)
    def keys(self):
        return self._keyboard.note_names

    frequenciesChanged = Signal()

    @Property(list, notify=frequenciesChanged)
    def frequencies(self):
        return list(self._keyboard.frequencies.values())

    def get_frequency(self, note: str):
        assert note in self._keyboard.frequencies
        return self._keyboard.frequencies[note]
