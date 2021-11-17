import os
import tempfile

class Temp:
    def __init__(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, dir=os.path.join(self.getCurrentPath(), ''))
        print(self.temp_file.name)
    
    def write(self, data=''):
        if data.strip():
            self.temp_file.write(data.encode())

    def getCurrentPath(self):
        return os.path.dirname(os.path.realpath(__file__))