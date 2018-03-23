import wave

import pyaudio


CHUNK = 1024


class Engine:
    def __init__(self):
        self._pyaudio = pyaudio.PyAudio()

    def start(self, path):
        wf = wave.open(path, 'rb')
        format_ = self._pyaudio.get_format_from_width(wf.getsampwidth())

        stream = self._pyaudio.open(
            format=format_,
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True,
        )

        while True:
            data = wf.readframes(CHUNK)
            if not data:
                break
            stream.write(data)

        stream.stop_stream()
        stream.close()

    def stop(self):
        pass

    def is_playing(self):
        return False
