import tempfile

from os import path

from utils import getRootPath

class Temp:
    def __init__(self):
        self.temp_dir = path.join(getRootPath(), '') + 'tmp/'
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, dir=self.temp_dir)

        self.hex_count = 0
    
    def write(self, data=''):
        if data.strip():
            data = hex(self.hex_count) + ' ' + data + '\n'
            data = data.encode()
            self.temp_file.write(data)

            self.hex_count = self.hex_count + 1
