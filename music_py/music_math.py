import numpy as np
from typing import Iterable


def sum_waves(
    frequencies: Iterable[float],
    intensities: Iterable[float],
    phases: Iterable[float],
    t: np.ndarray,
) -> np.ndarray:
    assert len(frequencies) == len(
        intensities
    ), "Frequencies and intensities must match length"
    return np.sum(
        np.sin(2 * np.pi * np.array(frequencies) * t.reshape(-1, 1) + np.array(phases))
        * np.array(intensities),
        axis=1,
    )
