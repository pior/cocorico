from threading import Event

import alsaaudio


FORMAT_MAP = {
    1: alsaaudio.PCM_FORMAT_U8,
    2: alsaaudio.PCM_FORMAT_S16_LE,
    3: alsaaudio.PCM_FORMAT_S24_LE,
    4: alsaaudio.PCM_FORMAT_S32_LE,
}


def _get_period_size(wavefile):
    return wavefile.getframerate() // 8


def _get_format(wavefile):
    sampling_width = wavefile.getsampwidth()
    format_ = FORMAT_MAP.get()
    if not format_:
        raise ValueError('Unsupported format: sampling_width=%s' % sampling_width)


class AlsaPlayer:
    def __init__(self):
        self.device = alsaaudio.PCM()
        self.should_stop = Event()

    def start(self, path):
        wavefile = wave.open(path, 'rb')
        try:
            self._play(wavefile)
        finally:
            wavefile.close()

    def _play(self, wavefile):
        period_size = _get_period_size(wavefile)

        self.device.setchannels(wavefile.getnchannels())
        self.device.setrate(wavefile.getframerate())
        self.device.setformat(_get_format(wavefile))
        self.device.setperiodsize(period_size)

        while True:
            frames = wavefile.readframes(period_size)
            if not frames:
                break
            if self.should_stop.is_set():
                self.should_stop.clear()
                break
            self.device.write(frames)

    def stop(self):
        self.should_stop.set()
