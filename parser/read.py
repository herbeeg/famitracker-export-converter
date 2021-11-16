import sys

class FileReader:
    def __init__(self, filename=None):
        self.filename = filename

    def start(self):
        if self.filename:
            try:
                with open(self.filename, 'r') as line:
                    print(line)
            except OSError as ex:
                """Terminate if an invalid path has been provided."""
                sys.stdout.write(ex.strerror + '\n')
                sys.exit()
            except Exception as ex:
                """Any uncaught errors should still result in the application closing."""
                sys.stdout.write('Invalid file provided. Terminating...\n')
                sys.exit()
