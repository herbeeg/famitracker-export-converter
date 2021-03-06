import sys

import constants
import parser.store as store

class FileReader:
    """
    Convert the provided FamiTracker export file
    into compressed encoded data for use when 
    splitting and exporting into separate 
    config and data files.
    """
    def __init__(self, filename=None):
        """
        Store the path of the text file we
        want to convert and prepare the 
        reader for execution.

        Args:
            filename (str): Relative path to the FamiTracker export file. Defaults to None.
        """
        self.filename = filename
        self.state = 'init'

    def start(self) -> str:
        """
        Read, encode and store the FamiTracker
        song information and pattern data in
        a compressed format that will be 
        used during the export phase.

        Returns:
            str: Full absolute path to the temporary file if encoding was successful
        """
        if self.filename:
            try:
                temp_store = store.Temp()
                """Open up a temporary file to write local information to."""

                with open(self.filename, 'r') as export_file:
                    self.state = 'headers'

                    for line in export_file:
                        if '' == line:
                            """Immediately move onto the next if the line is blank."""
                            continue

                        if self.shouldChangeState(line):
                            if 'headers' == self.state:
                                self.state = 'patterns'
                                continue
                            elif 'patterns' == self.state:
                                self.state = 'rows'
                                continue
                            elif 'rows' == self.state:
                                self.state = 'eof'
                                continue
                            elif 'eof' == self.state:
                                break
                        else:
                            if 'headers' == self.state:
                                line_extract = self.extractHeaders(line)
                            elif 'patterns' == self.state:
                                line_extract = self.extractPatterns(line)
                            elif 'rows' == self.state:
                                line_extract = self.extractRows(line)
                            
                            for item in line_extract:
                                """Only store temporary data if we require it for the export."""
                                temp_store.write(item)
            except OSError as ex:
                """Terminate if an invalid path has been provided."""
                sys.stdout.write(ex.strerror + '\n')
                sys.exit()
            except Exception as ex:
                """Any uncaught errors should still result in the application closing."""
                sys.stdout.write('Error encountered during file reading. Terminating...\n')
                sys.exit()
            finally:
                if 'eof' != self.state:
                    """Remove the temporary file that we created if the eof endings were never reached."""
                    temp_store.remove()
                else:
                    temp_store.close()

        return temp_store.getFullPath()

    def extractHeaders(self, next_line='') -> list:
        """
        Yield the data that will eventually be
        stored in the JSON configuration
        file as settings information.

        Args:
            next_line (str): The next line in the .txt file to read. Defaults to ''.
        
        Returns:
            list: Items to be appended to the temporary store, otherwise []
        """
        if next_line.startswith(('TITLE', 'AUTHOR', 'COPYRIGHT')):
            parts = next_line.split('"')

            return [parts[1]]
        elif next_line.startswith('EXPANSION'):
            parts = next_line.split(' ')
            last = int(parts[-1].rstrip('\n'))

            return [constants.globalExpansions()[last]]
        elif next_line.startswith('TRACK'):
            parts = ' '.join(next_line.split()).split(' ')

            return [parts[1], parts[2], parts[3]]

        return []

    def extractPatterns(self, next_line='') -> list:
        """
        Yield the realtime pattern data that will 
        be displayed above each column of 
        notes during playback.

        Args:
            next_line (str): The next line in the .txt file to read. Defaults to ''.
        
        Returns:
            list: Items to be appended to the temporary store, otherwise []
        """
        if next_line.startswith('ORDER'):
            parts = next_line.split(':')
            pattern_numbers = parts[1].rstrip('\n')
            combined = pattern_numbers.replace(' ', '')

            return [combined]

        return []

    def extractRows(self, next_line='') -> list:
        """
        Yield the individual note data for each column 
        that will be displayed and modified in real 
        time for each tick of audio playback.

        Args:
            next_line (str): The next line in the .txt file to read. Defaults to ''.
        
        Returns:
            list: Items to be appended to the temporary store, otherwise []
        """
        if next_line.startswith('ROW'):
            parts = next_line.split(':')
            parts.pop(0)
            channel_data = [channel.rstrip('\n') for channel in parts]
            channel_data = [channel.replace(' ', '') for channel in channel_data]
            
            return channel_data

        return []

    def shouldChangeState(self, next_line='') -> bool:
        """
        Define what part of the FamiTracker export
        file we are currently reading to allow
        for specific actions and functions
        to be called.
        
        Args:
            next_line (str): The next line in the .txt file to read. Defaults to ''.

        Returns:
            bool: True if we want to switch state, otherwise False
        """
        if next_line.startswith(('COLUMNS', 'PATTERN 00', '# End of export')):
            return True

        return False
