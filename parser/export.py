import sys

class DataExporter:
    def __init__(self, timestamp=0):
        if 0 < timestamp:
            self.filenames = [
                'ft2vis_json_' + str(timestamp),
                'ft2vis_csv_' + str(timestamp)
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
