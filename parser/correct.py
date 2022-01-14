import sys

class FixExport:
    def __init__(self, filename=None):
        self.filename = filename

        self.run()

    def run(self):
        if self.filename:
            pattern_map = {}

            try:
                with open(self.filename, 'r+') as export_file:
                    for line in export_file:
                        if line.startswith('ORDER'):
                            parts = line.split(':')

                            pattern_register = parts[1].rstrip('\n')
                            pattern_register = pattern_register.lstrip()
                            pattern_register = pattern_register.split(' ')

                            pattern_map[str(parts[0].replace('ORDER ', '').strip())] = {}

            except OSError as ex:
                """Terminate if an invalid path has been provided."""
                sys.stdout.write(ex.strerror + '\n')
                sys.exit()
            except Exception as ex:
                """Any uncaught errors should still result in the application closing."""
                sys.stdout.write('Error encountered during FamiTracker export correction. Terminating...\n')
                sys.exit()
