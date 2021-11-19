class DataExporter:
    def __init__(self, timestamp=0):
        if 0 < timestamp:
            self.filenames = [
                'ft2vis_json_' + str(timestamp),
                'ft2vis_csv_' + str(timestamp)
            ]

    def start(self):
        return

    def exportConfig(self):
        return
    
    def exportData(self):
        return
