import sys

class FileReader:
    def __init__(self, filename=None):
        self.filename = filename
        self.state = 'init'

    def start(self):
        if self.filename:
            try:
                with open(self.filename, 'r') as export_file:
                    self.state = 'headers'

                    for line in export_file:
                        if '' == line:
                            """Immediately move onto the next if the line is blank."""
                            continue

                        if 'headers' == self.state:
                            if self.shouldChangeState(line):
                                self.state = 'patterns'

                                continue
                            else:
                                continue
                        elif 'patterns' == self.state:
                            if self.shouldChangeState(line):
                                self.state = 'rows'

                                continue
                            else:
                                continue
                        elif 'rows' == self.state:
                            if self.shouldChangeState(line):
                                self.state = 'eof'

                                continue
                            else:
                                continue
                        elif 'eof' == self.state:
                            break
            except OSError as ex:
                """Terminate if an invalid path has been provided."""
                sys.stdout.write(ex.strerror + '\n')
                sys.exit()
            except Exception as ex:
                """Any uncaught errors should still result in the application closing."""
                sys.stdout.write('Invalid file provided. Terminating...\n')
                sys.exit()

    def extractHeaders(self, next_line=''):
        return ''

    def shouldChangeState(self, next_line=''):
        """
        Define what part of the FamiTracker export
        file we are currently reading to allow
        for specific actions and functions
        to be called.
        
        Args:
            next_line (String): The next line in the .txt file to read. Defaults to ''.

        Returns:
            boolean: True if we want to switch state, otherwise False
        """
        if next_line.startswith(('COLUMNS', 'PATTERN 00', '#End of export')):
            return True

        return False
