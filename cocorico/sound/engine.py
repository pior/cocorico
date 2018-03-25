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

        self._show_devices_info()
        self._device_id = self._find_device_id()
        if self._device_id is None:
            log.warning("Failed to find allowed sound device")
        else:
            log.info("Found desired device as device_id %s", self._device_id)

        atexit.register(self.close)

    def start(self, path):
        log.info("Start playback for %s", path)
        if self._device_id is None:
            log.warning("Ignoring sound request (no device_id)")
            return

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
            output_device_index=self._device_id,
            stream_callback=callback,
        )
        self._stream.start_stream()

    def stop(self):
        if self._stream:
            self._stream.stop_stream()
            self._stream.close()
            self._stream = None

    def close(self):
        if self._pyaudio:
            log.info("Terminate PyAudio")
            self.stop()
            self._pyaudio.terminate()
            self._pyaudio = None

    def is_playing(self):
        if not self._stream:
            return False
        return self._stream.is_active()

    def _show_devices_info(self):
        from pprint import pformat
        for device_info in self._get_devices_info():
            log.info(pformat(device_info))

    def _get_devices_info(self):
        return [
            self._pyaudio.get_device_info_by_index(device_num)
            for device_num in range(self._pyaudio.get_device_count())
        ]

    def _find_device_id(self):
        allowed = [
            'C-Media USB Headphone Set: Audio (hw:1,0)',
            'Built-in Output',  # MacOs
        ]
        for device_info in self._get_devices_info():
            if device_info['name'] in allowed:
                return device_info['index']
