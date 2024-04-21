from PySide6.QtCore import QPointF, Signal, Property
from PySide6.QtGui import QBrush, QColor, QPainter, QPen
from PySide6.QtQuick import QQuickPaintedItem

import numpy as np


class SineWavePlot(QQuickPaintedItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._frequencies = []

    def get_frequencies(self):
        return self._frequencies

    def set_frequencies(self, value):
        if value != self._frequencies:
            self._frequencies = value
            self.update()
            self.frequencies_changed.emit()
        print(self._frequencies)

    frequencies_changed = Signal()
    frequencies = Property(
        list, get_frequencies, set_frequencies, notify=frequencies_changed
    )

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
        if len(self._frequencies) == 0:
            return

        # Always plot 8 periods of slowest frequency
        x_scale = 30 / min(self._frequencies) / self.width()  # seconds / pixel
        y_scale = self.height() / 2 / len(self._frequencies)

        pen = QPen("#41FF00")
        pen.setWidth(3)
        painter.setPen(pen)

        points = []
        for x in range(0, int(self.width()), 1):
            t = x * x_scale
            y = 0
            for freq in self._frequencies:
                y = y + np.sin(2 * np.pi * freq * t)
            y = y * y_scale + self.height() / 2
            points.append(QPointF(x, y))

        painter.drawPolyline(points)
