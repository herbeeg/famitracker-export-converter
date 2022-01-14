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
                    pattern_id = '00'

                    for line in export_file:
                        if line.startswith('ORDER'):
                            parts = line.split(':')

                            pattern_register = parts[1].rstrip('\n')
                            pattern_register = pattern_register.lstrip()
                            pattern_register = pattern_register.split(' ')

                            pattern_map[str(parts[0].replace('ORDER ', '').strip())] = [{register : []} for register in pattern_register]
                            """Generate empty lists to populate with individual channel data on a per-pattern basis."""
                        elif line.startswith('PATTERN'):
                            parts = line.split(' ')
                            pattern_id = parts[1].rstrip('\n')
                        elif line.startswith('ROW'):
                            parts = line.split(':')

            except OSError as ex:
                """Terminate if an invalid path has been provided."""
                sys.stdout.write(ex.strerror + '\n')
                sys.exit()
            except Exception as ex:
                """Any uncaught errors should still result in the application closing."""
                sys.stdout.write('Error encountered during FamiTracker export correction. Terminating...\n')
                sys.exit()
