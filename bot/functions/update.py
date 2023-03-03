import os

def updateq():
    return os.popen('ls').read()