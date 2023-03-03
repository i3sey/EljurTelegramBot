import subprocess   # импортируем модуль subprocess, который позволяет запускать команды в терминале

def updateq():  
    result = subprocess.run(['git', 'pull'], stdout=subprocess.PIPE)  # выполняем команду `git pull` и сохраняем результат в переменной `result`, захватываем вывод команды `stdout`
    return result.stdout.decode('utf-8')   # декодируем вывод команды и возвращаем его из функции в формате строки
