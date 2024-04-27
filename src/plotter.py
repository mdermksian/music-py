from PySide6.QtCore import Qt, QPointF, Signal, Property
from PySide6.QtGui import QPainter, QPen
from PySide6.QtQuick import QQuickPaintedItem

import numpy as np


class SineWavePlot(QQuickPaintedItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._notes = []

    def get_notes(self):
        return self._notes

    def set_notes(self, value):
        if value != self._notes:
            self._notes = value
            self.update()
            self.notes_changed.emit()

    notes_changed = Signal()
    notes = Property(list, get_notes, set_notes, notify=notes_changed)

    def paint(self, painter: QPainter):
        painter.setRenderHint(QPainter.Antialiasing)
        self.draw_axes(painter)
        self.draw_sin_wave(painter)

    def draw_axes(self, painter: QPainter):
        pen = QPen("#000000")
        pen.setWidth(2)
        painter.setPen(pen)

        # Draw x-axis
        painter.drawLine(0, self.height() / 2, self.width(), self.height() / 2)

        # Draw y-axis
        painter.drawLine(self.width() / 2, 0, self.width() / 2, self.height())

    def draw_sin_wave(self, painter: QPainter):
        if len(self._notes) == 0:
            return

        freqs = np.array([note["frequency"] for note in self._notes])
        intens = np.array([note["intensity"] for note in self._notes])

        # Always plot 8 periods of slowest frequency
        x_scale = 30 / min(freqs) / self.width()  # seconds / pixel
        y_scale = self.height() / 2 / len(self._notes)

        pen = QPen("#41FF00")
        pen.setWidth(2)
        painter.setPen(pen)

        x = np.arange(0, self.width())
        t = (x * x_scale).reshape(-1, 1)
        sinusoids = np.sin(2 * np.pi * freqs * t) * intens
        y = np.sum(sinusoids, axis=1) * y_scale + self.height() / 2
        pts = np.vstack((x, y)).T
        qpts = [QPointF(pt[0], pt[1]) for pt in pts]

        painter.drawPolyline(qpts)
