import requests

def siteReq(lesson, number):
    gdzUrl = f'https://gdz.ltd/content/9-class/angliyskiy/Ter-Minasova/exercise/{lesson}/{number}.jpg'
    with open('answers_database.txt', encoding='utf8') as f:
        datafile = f.readlines()
    for line in datafile:
        if gdzUrl in line:
            r = requests.get(gdzUrl)
            return r.content
    return -1