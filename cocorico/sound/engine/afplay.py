import subprocess


class Afplay:
    def start(self, path):
        subprocess.run(['afplay', path])

    def stop(self):
        pass