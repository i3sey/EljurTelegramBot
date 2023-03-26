import hashlib
import requests


def cleanup(dictionary):
    return '\n'.join([f'<b>{key.capitalize() if isinstance(key, str) else " "}:</b> {value.capitalize() if isinstance(value, str) else " "}' for key, value in dictionary.items()])


def hwcleanup(dictionary):
    return '\n'.join([f'<b>{value["name"].capitalize()}:</b> {value["hometask"]}\n' for key, value in dictionary.items() if value["hometask"] is not None])


def dailyCleanup(dictionary):
    urls = {}
    for i, d in dictionary.items():
        if d['attach']:
            urls.update(d['attach'])
    return '\n'.join([f'<b>{key.capitalize()}.</b> {value["name"].capitalize()}' for key, value in dictionary.items()]), urls


# Defines a function to loop through a list and yield a result or -2 
def magicLoop(ist, page):
    # Initializes an empty list
    result = []

    # Iterates through the list argument "ist" and uses enumerate() to add a counter to it
    for key, i in enumerate(ist):
    
        # Extends the list "result" by adding a number and incrementing by 1 for each element
        # that is equal to an element in the second argument "page"
        result.extend(key + 1 for l in page if i == l and ist[key + 1].isnumeric())
    # Returns the result, or if the list is empty, returns -2
    return result or -2



def merge(ist, Letter):
    e = []
    count = multiply(ist, Letter)
    for key, value in count.items():
        e.extend(ist[key + i] for i in range(value))
    return e


def multiply(ist, Letter):
    count = {}
    for e in Letter:
        count[e] = 1
        for _ in ist:
            try:
                test = ist[e + count[e]]
            except IndexError:
                break
            if f'{test}'.isdigit():
                count[e] += 1
            else:
                break
    return count

def download(url, name):
    header = { 
        'authority': 'httpbin.org', 
        'cache-control': 'max-age=0', 
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"', 
        'sec-ch-ua-mobile': '?0', 
        'upgrade-insecure-requests': '1', 
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 
        'sec-fetch-site': 'none', 
        'sec-fetch-mode': 'navigate', 
        'sec-fetch-user': '?1', 
        'sec-fetch-dest': 'document', 
        'accept-language': 'en-US,en;q=0.9', 
    }
    r = requests.get(url, headers=header)
    with open(name, 'wb') as f:
        f.write(r.content)
        
def calculate_hash(file_path):
    with open(file_path, 'rb') as f:
        hsh = hashlib.sha1()
        while True:
            data = f.read(2048)
            if not data:
                break
            hsh.update(data)
    return hsh.hexdigest()