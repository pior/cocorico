import atexit
import wave

import pyaudio


CHUNK = 1024


class Engine:
    def __init__(self):
        self._pyaudio = pyaudio.PyAudio()
        atexit.register(self.close)

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
