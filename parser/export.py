import csv
import json
import sys

from os import path

import constants
from utils import getRootPath

class DataExporter:
    """
    Handles the full conversion of our temporary
    encoded FamiTracker export data and split
    into two separate files for config and
    raw pattern information.
    """
    def __init__(self, timestamp=0, temp=None, expansion=None):
        """
        Store the full directory paths that we
        will write the config and data to as
        well as initialising the exporter
        state to begin writing.

        Args:
            timestamp (int): Unique file identifier based on when execution began. Defaults to 0.
            temp (str): Full path to the temporary storage for reference. Defaults to None.
        """
        if 0 < timestamp:
            self.filenames = [
                path.join(getRootPath(), '') + 'exp/' + 'ft2vis_json_{time}.json'.format(time=timestamp),
                path.join(getRootPath(), '') + 'exp/' + 'ft2vis_csv_{time}.csv'.format(time=timestamp)
            ]

        self.tempfile = temp
        self.chip = expansion

        self.state = 'init'

    def start(self):
        """
        Handle the opening, writing and cleaning up of
        the JSON config and CSV data exports for 
        users to input into the visualiser.
        """
        first_pattern = ''

        if self.filenames[0]:
            try:
                with open(self.filenames[0], 'w+') as json_file:
                    file_contents = self.exportConfig()
                    json_file.write(file_contents[0])
                    """Reference first element of tuple."""
                    json_file.close()

                    first_pattern = file_contents[1]
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
                with open(self.filenames[1], 'w+', newline='', encoding='utf-8') as csv_file:
                    file_contents = self.exportData(first_pattern)

                    writer = csv.writer(csv_file)
                    writer.writerows(file_contents)
                    """csv Python library allows us to write valid CSV data cleanly in a similar manner to other formats."""

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

    def exportConfig(self) -> tuple:
        """
        Build a dictionary of configurations to
        be handled, encode them as a JSON
        object and export.

        Returns:
            tuple: JSON data we want to write to the config and the next line of data, as a pair.
        """
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
                    """There is a lot of variance in the amount of frames a song can have so a list is far more flexible to add to."""

                    isFrame = True
                    """Manual validation required to check if we're still processing frame information."""

                    while isFrame:
                        next_line = saved_line = temp_file.readline()
                        """Assign same value to a variable so that no data is lost when we move onto detailed pattern information."""
                        next_line = next_line[4:].strip()
                        """This will strip the encoding and any whitespace if the encoding only covers three characters."""

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
        """Keep track of the application status."""

        return (json.dumps(config), saved_line)
    
    def exportData(self, first='') -> list:
        """
        Structure the pattern data into lists that 
        represent columns in a CSV file so they
        can be written cleanly in one sweep 
        during the export process.

        Args:
            first (str): The first line of the pattern data that gets collected before validation begins. Defaults to ''.

        Returns:
            list: Combined pattern data that will be exported as a CSV.
        """
        pattern_data = []

        if self.tempfile:
            try:
                with open(self.tempfile, 'r') as temp_file:
                    next_line = temp_file.readline()

                    while first != next_line:
                        """Re-reading existing config lines that have already been parsed."""
                        next_line = temp_file.readline()

                    headers = constants.columns(self.chip)

                    if not headers:
                        """Terminate if the expansion chip is still invalid for whatever reason."""
                        sys.stdout.write('Passed expansion chip is invalid. Terminating...\n')
                        sys.exit()

                    pattern_data.append(headers[1])

                    column_increment = int(headers[0])
                    line_number = 0
                    pattern_buffer = []
                        
                    while next_line:
                        next_line = temp_file.readline()

                        if 0 == line_number:
                            """We've already got the first line of data so we use that and immediately move onto the next line."""
                            pattern_buffer.append(self.decodePattern(first))
                        else:      
                            if 0 == line_number % column_increment:
                                pattern_data.append(pattern_buffer)
                                """Store what's in the buffer once we're ready for the next line."""
                                
                                pattern_buffer = []
                                """Assign a new list object rather than emptying the buffer contents as existing data was being overwritten."""
                                
                            pattern_buffer.append(self.decodePattern(next_line))
                        
                        line_number = line_number + 1
            except OSError as ex:
                """Terminate if an invalid temporary path has been provided."""
                sys.stdout.write(ex.strerror + '\n')
                sys.exit()
            except Exception as ex:
                """Any uncaught errors should still result in the application closing."""
                sys.stdout.write('Error encountered during CSV export. Terminating...\n')
                sys.exit()
            finally:
                temp_file.close()

        self.state = 'eof'
        """Final application state."""

        return pattern_data

    def decodePattern(self, raw_line='') -> str:
        """
        Extract the note information from the
        compressed channel data and run it
        past validation and replacement
        checks for consistency.

        Args:
            raw_line (str): The line in its base form to decode. Defaults to ''.

        Returns:
            str: Decoded note data, otherwise empty string.
        """
        decoded = ''

        try:
            pattern = raw_line.split(' ')[1].strip()
            decoded = pattern[:3]
            """Note data consists of three alphanumeric and special characters."""

            decoded = decoded.replace('---', 'NOP')
            """Run the triple dash replacement before the single dash to easily avoid any unwarranted conversions."""
            decoded = decoded.replace('-', 'n')
            """Regular notes."""
            decoded = decoded.replace('#', 'h')
            """Sharp notes."""
            decoded = decoded.replace('...', '')
            """Save space by removing any pattern data that holds no information."""
        except IndexError as ex:
            """Catch EoF endings and reset any decoded data before the file is closed."""
            decoded = ''

        return decoded