import os
from bot.misc.util import download, calculate_hash
from bot.functions import lessonsToday
from bot.database.main import filesDB
import hashlib
import datetime

files = filesDB()



def filesCheck(urls) -> list:
    done = []
    filesHash = []
    for name, url in urls.items():
        h = files.get(name)
        if h == -1:
            download(url, name)
            rez = calculate_hash(f'{name}')
            filesHash.append({'name': name, 'hash': rez, 'date': datetime.datetime.now()})
        else:
            done.append({'file_id': h['file_id'],
                         'url': url})
    return done, filesHash
            

    