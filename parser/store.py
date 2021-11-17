import tempfile

from os import path

from utils import getRootPath

class Temp:
    def __init__(self):
        self.temp_dir = path.join(getRootPath(), '') + 'tmp/'
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, dir=self.temp_dir)
    
    def write(self, data=''):
        if data.strip():
            self.temp_file.write(data.encode())
