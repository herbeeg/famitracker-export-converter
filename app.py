import sys
import time

import constants
import parser.read as read
import parser.export as export

class App:
    """
    Base container class to divert all export
    file conversions and error handling to
    their respective packages and 
    libraries.
    """
    def __init__(self, expansion=None, filename=None):
        """
        Initialise the command line session, using
        the correct expansion type to convert
        and output readable data for our
        visualiser to parse.
        
        Args:
            expansion (String): FamiTracker expansion chip to use as reference for parsing channel data. Defaults to None.
            filename (String): Name of local file to be housed in same directory as script execution. Defaults to None.
        """
        self.expansion = expansion
        self.filename = filename

        self.validateParameters()

        self.reader = read.FileReader(self.filename)
        full_path = self.reader.start()
        """Attempt to start reading the file if validation passes."""

        timestamp = int(time.time())
        """Remove decimal places created by time.time() floating point precision for clean filenames."""
        self.exporter = export.DataExporter(timestamp, full_path)
        self.exporter.start()
        """Attempt to start writing to JSON config and CSV data files."""

    def validateParameters(self):
        """
        Ensure that the information passed to the
        parser by the user via the command line
        is in the correct format.
        """
        if self.expansion is None:
            """Terminate execution if no expansion chip is provided."""
            sys.stdout.write('Please provide a valid expansion chip name for parsing. Terminating...\n')
            sys.exit()
        elif self.expansion.lower() not in constants.expansions():
            """Ensure case-sensitivity doesn't get in the way of conversions."""
            sys.stdout.write('Invalid expansion chip provided. Please reference the README for accepted formats. Terminating...\n')
            sys.exit()

        if self.filename is None:
            """Terminate execution if no filename is provided."""
            sys.stdout.write('Please provide a valid .txt file for parsing. Terminating...\n')
            sys.exit()
        elif not self.filename.lower().endswith('.txt'):
            """Ensure case-sensitivity doesn't get in the way of conversions."""
            sys.stdout.write('Invalid filename provided. Please reference the README for accepted formats. Terminating...\n')
            sys.exit()

if '__main__' == __name__:
    """Initialise root app when file is executed via the command line."""
    if 2 < len(sys.argv):
        app = App(sys.argv[1], sys.argv[2])
    elif 1 < len(sys.argv):
        app = App(sys.argv[1])
    else:
        app = App()
