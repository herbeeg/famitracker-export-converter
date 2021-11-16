import tempfile

class Temp:
    def __init__(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
