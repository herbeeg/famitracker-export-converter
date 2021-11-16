import sys

import constants

class App():
    """
    Base container class to divert all export
    file conversions and error handling to
    their respective packages and 
    libraries.
    """
    def __init__(self, expansion=None, filename=None):
        """
        Initialise the command line session, using
        the correct expansion type to convert
        and output readable data for our
        visualiser to parse.
        
        Args:
            expansion (String): FamiTracker expansion chip to use as reference for parsing channel data. Defaults to None.
        """

        if expansion is None:
            """Terminate execution if any invalid parameters are provided."""
            sys.stdout.write('No expansion chip provided. Please reference the README for accepted formats. Terminating...\n')
            sys.exit()
        elif str.lower(expansion) not in constants.expansions():
            """Ensure case-sensitivity doesn't get in the way of conversions."""
            sys.stdout.write('Invalid expansion chip provided. Please reference the README for accepted formats. Terminating...\n')
            sys.exit()

        return

if '__main__' == __name__:
    """Initialise root app when file is executed via the command line."""
    if 2 < len(sys.argv):
        app = App(sys.argv[1], sys.argv[2])
    if 1 < len(sys.argv):
        app = App(sys.argv[1])
    else:
        app = App()
