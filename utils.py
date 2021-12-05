from os import path

def getRootPath() -> str:
    """
    Get the root execution path for the
    project for reference when dealing 
    with export directories.

    Returns:
        str: Project path root
    """
    return path.dirname(path.realpath(__file__))
