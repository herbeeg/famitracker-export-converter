import sys

from os import path

from utils import getRootPath

class DataExporter:
    def __init__(self, timestamp=0):
        if 0 < timestamp:
            self.filenames = [
                path.join(getRootPath(), '') + 'exp/' + 'ft2vis_json_{0}.json'.format(timestamp),
                path.join(getRootPath(), '') + 'exp/' + 'ft2vis_csv_{0}.csv'.format(timestamp)
            ]

        self.state = 'init'

    def start(self):
        if self.filenames[0]:
            try:
                with open(self.filenames[0], 'w+') as json_file:
                    file_contents = self.exportConfig()
                    json_file.write(file_contents)
                    json_file.close()
            except Exception as ex:
                """Any uncaught errors should still result in the application closing."""
                sys.stdout.write('Error encountered during file reading. Terminating...\n')
                sys.exit()

    def exportConfig(self):
        return
    
    def exportData(self):
        return
