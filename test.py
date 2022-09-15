import re

# hometask = 'Упр. 122, стр. 10'
# hometask = 'страница 10 упражнение 122'
# hometask = 'стр10№122'
# hometask = 'абоба12олр21'


def finder(hometask, splitBool):
    page = (
        'стр',
        'страница',
        'с'
    )
    number = (
        'номер',
        'упр',
        'упражнение',
        '№'
    )
    if splitBool == True:
        f = re.sub(r'(?<=\d)(?!\d)|(?<!\d)(?=\d)', ' ', hometask)
        lst = f.replace('.', '').replace(',', '').split()
    else:
        lst = hometask.replace('.', '').replace(',', '').split()
    ist = [i.lower() for i in lst]
    PageLetter = magicLoop(ist, page)
    NumLetter = magicLoop(ist, number)
    if PageLetter == -2 and NumLetter != -2:
        result = {'number': ist[NumLetter + 1]}
    elif NumLetter == -2 and PageLetter != -2:
        result = {'page': ist[PageLetter + 1]}
    elif PageLetter == -2:
        return finder(hometask, True) if splitBool == False else -2
    else:
        result = {'page': ist[PageLetter + 1],
                  'number': ist[NumLetter + 1]}
        return result


def magicLoop(ist, page):
    for i in ist:
        for l in page:
            if i == l:
                return ist.index(l)
    return -2


if __name__ == '__main__':
    while True:
        hometask = input('Введи: ')
        result = finder(hometask, False)
        print(result)
