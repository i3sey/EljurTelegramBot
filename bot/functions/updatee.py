import subprocess

def updateq():
    result = subprocess.run(['git', 'pull'], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')
