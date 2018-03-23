import simpleaudio


class AlsaPlayer:
    def __init__(self):
        self._play_obj = None

    def start(self, path):
        wave_object = simpleaudio.WaveObject.from_wave_file(path)
        self._play_obj = wave_object.play()

    def stop(self):
        simpleaudio.stop_all()
