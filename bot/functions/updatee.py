import os

def updateq():
    return os.popen('git pull').read()