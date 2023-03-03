import subprocess

def updateq():
    result = ""
    try:
        # Выполняем команду git pull в терминале
        p1 = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = p1.communicate() # выводим результат выполнения из терминала
        result += output.decode("utf-8") + "\n" + error.decode("utf-8")
        
        # После успешного выполнения первой команды - выполняем pm2 restart run
        if not error:
            p2 = subprocess.Popen(["pm2", "restart", "run"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = p2.communicate() # выводим результат выполнения из терминала
            result += output.decode("utf-8") + "\n" + error.decode("utf-8")
    except Exception as e:
        result = "An error occurred while executing the command: {}\n{}".format(str(e), result)
    return result
