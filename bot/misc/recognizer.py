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
        try:
            lst = hometask.replace('.', '').replace(',', ' ').split()
        except AttributeError:
            return
    ist = [i.lower() for i in lst]
    PageLetter = magicLoop(ist, page)
    NumLetter = magicLoop(ist, number)
    if PageLetter == -2 and NumLetter != -2:
        return {'number': merge(ist, NumLetter)}
    elif NumLetter == -2 and PageLetter != -2:
        return {'page': merge(ist, PageLetter)}
    elif PageLetter == -2:
        return finder(hometask, True) if splitBool == False else -2
    else:
        return {'page': merge(ist, PageLetter), 'number': merge(ist, NumLetter)}

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

def magicLoop(ist, page):
    result = []
    for key, i in enumerate(ist):
        result.extend(key + 1 for l in page if i == l)
    return result or -2

if __name__ == '__main__':
    while True:
        hometask = input('Введи: ')
        # hometask = 'Упр. 3 выполнить письменно, упр. 4 составить рассказ, выучить наизусть.'
        result = finder(hometask, False)
        print(result)
    # hometask = 'стр. 3 32 выполнить письменно, упр. 4, 5 составить рассказ, выучить наизусть.'
    # # hometask = '№749,751, 750'
    # # hometask = 'упр 41, 45 (задания 3-5), повторить правила : чередующиеся гласные в корне слова, правописание н-нн, ъ и ь'
    # # hometask = 'страница 23,24 Упр 23'
    # result = finder(hometask, False)
    # print(result)

