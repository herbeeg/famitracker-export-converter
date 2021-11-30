import sys

from os import path

from utils import getRootPath

class DataExporter:
    def __init__(self, timestamp=0):
        if 0 < timestamp:
            self.filenames = [
                path.join(getRootPath(), '') + 'exp/' + 'ft2vis_json_{time}.json'.format(time=timestamp),
                path.join(getRootPath(), '') + 'exp/' + 'ft2vis_csv_{time}.csv'.format(time=timestamp)
            ]

        self.state = 'init'

    def start(self):
        if self.filenames[0]:
            try:
                with open(self.filenames[0], 'w+') as json_file:
                    file_contents = self.exportConfig()
                    json_file.write(file_contents)
                    json_file.close()
            except TypeError as ex:
                """We expect a str to be passed for writing."""
                sys.stdout.write('{error}: Attempted to write invalid data type.\n'.format(error=str(type(ex))))
                sys.exit()
            except Exception as ex:
                """Any uncaught errors should still result in the application closing."""
                sys.stdout.write('Error encountered during file reading.\n')
                sys.exit()
            finally:
                if 'eof_json' != self.state:
                    """Terminate the application if we don't read all necessary JSON data."""
                    sys.stdout.write('Didn\'t reach end of JSON config correctly. Terminating...\n')
                    sys.exit()

        if self.filenames[1]:
            try:
                with open(self.filenames[1], 'w+') as csv_file:
                    file_contents = self.exportData()
                    csv_file.write(file_contents)
                    csv_file.close()
            except TypeError as ex:
                """We expect a str to be passed for writing."""
                sys.stdout.write('{error}: Attempted to write invalid data type.\n'.format(error=str(type(ex))))
                sys.exit()
            except Exception as ex:
                """Any uncaught errors should still result in the application closing."""
                sys.stdout.write('Error encountered during file reading.\n')
                sys.exit()
            finally:
                if 'eof' != self.state:
                    """Terminate the application if we don't read entire temporary data file."""
                    sys.stdout.write('Didn\'t complete parsing of temp data file. Terminating...\n')
                    sys.exit()

        sys.stdout.write('Succesfully wrote config to {path} in {size} bytes.\n'.format(path=self.filenames[0], size=path.getsize(self.filenames[0])))
        sys.stdout.write('Succesfully wrote data to {path} in {size} bytes.\n'.format(path=self.filenames[1], size=path.getsize(self.filenames[1])))

    def exportConfig(self):
        return None
    
    def exportData(self):
        return None
