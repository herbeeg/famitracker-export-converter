import json
import sys

from os import path

from utils import getRootPath

class DataExporter:
    def __init__(self, timestamp=0, temp=None):
        if 0 < timestamp:
            self.filenames = [
                path.join(getRootPath(), '') + 'exp/' + 'ft2vis_json_{time}.json'.format(time=timestamp),
                path.join(getRootPath(), '') + 'exp/' + 'ft2vis_csv_{time}.csv'.format(time=timestamp)
            ]

        self.tempfile = temp
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
        config = {}
        saved_line = ''

        if self.tempfile:
            try:
                with open(self.tempfile, 'r') as temp_file:
                    config['title'] = temp_file.readline().replace('0x0', '').strip()
                    config['author'] = temp_file.readline().replace('0x1', '').strip()
                    config['copyright'] = temp_file.readline().replace('0x2', '').strip()
                    config['expansion'] = temp_file.readline().replace('0x3', '').strip()
                    
                    config['song'] = {}
                    config['song']['frames'] = temp_file.readline().replace('0x4', '').strip()
                    config['song']['speed'] = temp_file.readline().replace('0x5', '').strip()
                    config['song']['bpm'] = temp_file.readline().replace('0x6', '').strip()

                    config['frames'] = []

                    isFrame = True
                    """Manual validation required to check if we're still processing frame information."""

                    while isFrame:
                        next_line, saved_line = temp_file.readline()
                        next_line = next_line[4:].strip()

                        if next_line.isalnum():
                            """Non-alphanumeric characters will exist in the pattern data so safe assumption here."""
                            k = 2
                            config['frames'].append([next_line[i:i+k] for i in range(0, len(next_line), k)])
                            """Frame pattern information comes in pairs so we can use list comprehension along with a range"""
                            """to increment over each string section to append to the config file."""
                        else:
                            isFrame = False

            except OSError as ex:
                """Terminate if an invalid temporary path has been provided."""
                sys.stdout.write(ex.strerror + '\n')
                sys.exit()
            except Exception as ex:
                """Any uncaught errors should still result in the application closing."""
                sys.stdout.write('Error encountered during JSON export. Terminating...\n')
                sys.exit()
            finally:
                temp_file.close()
        
        self.state = 'eof_json'

        return (json.dumps(config), saved_line)
    
    def exportData(self):
        return None
