import sounddevice as sd
from typing import TypedDict, Iterable, Callable
import numpy as np
from scipy import signal
from music_py.music_math import sum_waves

DEFAULT_SAMPLE_RATE = 48000


class SoundData(TypedDict):
    intensities: Iterable[float]
    frequencies: Iterable[float]
    phases: Iterable[float]


class SoundGenerator:
    def __init__(self, get_freqs_fun: Callable[[], SoundData]):
        self._get_freqs_fun = get_freqs_fun
        self._stream = sd.OutputStream(
            callback=self.callback,
            channels=1,
            samplerate=DEFAULT_SAMPLE_RATE,
            latency=1 / 5,
        )
        self._lowpass = signal.butter(4, 500, fs=DEFAULT_SAMPLE_RATE, output="sos")
        self._filter_initial = np.zeros((self._lowpass.shape[0], 2))

    def callback(self, outdata: np.ndarray, frames: int, cb_time, status):
        sounddata = self._get_freqs_fun()

        if len(sounddata["frequencies"]) > 0:
            self._lowpass = signal.butter(
                4, max(sounddata["frequencies"]), fs=DEFAULT_SAMPLE_RATE, output="sos"
            )

        out = generate_waveform(
            sounddata["frequencies"],
            sounddata["intensities"],
            sounddata["phases"],
            frames,
            cb_time.inputBufferAdcTime,
            self._stream.samplerate,
        )

        if np.max(out) > 0.8:
            out /= np.max(out) * (1 / 0.8)

        out, zf = signal.sosfilt(self._lowpass, out, zi=self._filter_initial)
        self._filter_initial = zf
        outdata[:] = out.reshape(outdata.shape)

    def start(self):
        self._stream.start()

    def stop(self):
        self._stream.stop()
        self._stream.close()


def generate_waveform(
    frequencies: Iterable[float],
    intensities: Iterable[float],
    phases: Iterable[float],
    frames: int,
    starttime: float,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
) -> np.ndarray:
    if len(frequencies) < 1:
        return np.zeros((frames))
    t = np.linspace(
        starttime, starttime + float(frames) / sample_rate, frames, endpoint=False
    )
    return sum_waves(frequencies, intensities, phases, t).flatten()
