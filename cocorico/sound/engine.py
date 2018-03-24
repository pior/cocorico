import atexit
import logging
import wave

import pyaudio

log = logging.getLogger(__name__)

CHUNK = 1024


class Engine:
    def __init__(self):
        self._pyaudio = pyaudio.PyAudio()
        self._stream = None
        atexit.register(self.close)

        self._show_devices_info()

    def start(self, path):
        self.stop()

        wf = wave.open(path, 'rb')
        format_ = self._pyaudio.get_format_from_width(wf.getsampwidth())

        def callback(in_data, frame_count, time_info, status):
            data = wf.readframes(frame_count)
            return (data, pyaudio.paContinue)

        self._stream = self._pyaudio.open(
            format=format_,
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True,
            stream_callback=callback,
        )
        self._stream.start_stream()

    def stop(self):
        if not self._stream:
            return
        self._stream.stop_stream()

    def close(self):
        if self._pyaudio:
            self._pyaudio.terminate()
            self._pyaudio = None

    def is_playing(self):
        if not self._stream:
            return False
        return self._stream.is_active()

    def _show_devices_info(self):
        from pprint import pformat
        log.info("Default: %s", pformat(self._pyaudio.get_default_output_device_info()))
        for device_num in range(self._pyaudio.get_device_count()):
            log.info("Device %s: %s", device_num, pformat(self._pyaudio.get_device_info_by_index(device_num)))
