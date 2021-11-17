import tempfile

from os import path

from utils import getRootPath

class Temp:
    """
    Handle the local storage of raw FamiTracker
    export data within a local temporary
    directory that can be referenced
    when conversion takes place.
    """
    def __init__(self):
        """
        Specify the directory and file path(s)
        to be used when creating temporary
        files on the local system.
        """
        self.temp_dir = path.join(getRootPath(), '') + 'tmp/'
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, dir=self.temp_dir)

        self.hex_count = 0
        """Integer base that will be used as an identifier when writing to the local file."""
    
    def write(self, data=''):
        """
        Encode and write the next line into
        the allocated temporary file, to
        which a hexadecimal identifier
        is prepended.

        Args:
            data (str): Raw text data that is read from the export. Defaults to ''.
        """
        if data.strip():
            data = hex(self.hex_count) + ' ' + data + '\n'
            data = data.encode()
            """Hex identifier and newline characters are added to the data to write and byte-encoded."""
            self.temp_file.write(data)

            self.hex_count = self.hex_count + 1
            """Ensure each identifier stays unique for direct list reference later on."""
