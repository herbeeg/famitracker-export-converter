import tempfile

class Temp:
    def __init__(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
    
    def write(self, data=''):
        if data.strip():
            self.temp_file.write(data.encode())