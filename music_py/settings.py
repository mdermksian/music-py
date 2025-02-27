from PySide6.QtCore import Qt, QObject


KEY_MAP = {
    Qt.Key.Key_A: "C4",
    Qt.Key.Key_W: "C#4",
    Qt.Key.Key_S: "D4",
    Qt.Key.Key_E: "D#4",
    Qt.Key.Key_D: "E4",
    Qt.Key.Key_F: "F4",
    Qt.Key.Key_T: "F#4",
    Qt.Key.Key_G: "G4",
    Qt.Key.Key_Y: "G#4",
    Qt.Key.Key_H: "A4",
    Qt.Key.Key_U: "A#4",
    Qt.Key.Key_J: "B4",
    Qt.Key.Key_K: "C5",
    Qt.Key.Key_O: "C#5",
    Qt.Key.Key_L: "D5",
    Qt.Key.Key_P: "D#5",
    Qt.Key.Key_Semicolon: "E5",
}


class Settings(QObject):
    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.key_map = KEY_MAP
