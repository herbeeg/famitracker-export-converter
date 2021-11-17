from os import path

def getRootPath() -> str:
    return path.dirname(path.realpath(__file__))