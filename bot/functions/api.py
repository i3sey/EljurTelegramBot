from bot.database.main import DiaryDB
from Eljur.auth import Authorization
from Eljur.journal import Journal
from Eljur.message import Message
from Eljur.portfolio import Portfolio
from Eljur.profile import Profile

db = DiaryDB('database.db')

idc = ''


def newUser(idc, login, password, domain) -> 1 or dict:

    authorisation = Authorization()

    data = {
        "username": login,
        "password": password
    }
    subdomain = domain

    answer = authorisation.login(subdomain, data)
    if "session" not in answer:
        # print(answer)
        return answer

    db.sets(f'{idc}_login', login)
    db.sets(f'{idc}_password', password)
    db.set(f'{idc}_domain', domain)
    return 0


def getID() -> idc:
    idc = '882076783'
    return idc


def idProfile(idc) -> dict or 1:
    authorisation = Authorization()
    loginTest = db.get(f'{idc}_login')
    if loginTest == False:
        return 1
    data = {
        "username": loginTest,
        "password": db.get(f'{idc}_password')
    }
    subdomain = db.get(f'{idc}_domain')

    answer = authorisation.login(subdomain, data)
    if "session" not in answer:
        print(answer)
        return 1

    profile = Profile()
    return profile.getProfile(subdomain, answer["session"])


def idJournal(idc, week) -> dict or 1:
    authorisation = Authorization()

    loginTest = db.get(f'{idc}_login')
    if loginTest == False:
        return 1
    data = {
        "username": loginTest,
        "password": db.get(f'{idc}_password')
    }
    subdomain = db.get(f'{idc}_domain')

    answer = authorisation.login(subdomain, data)
    if "session" not in answer:
        print(answer)
        return 1

    journal = Journal()
    return journal.journal(subdomain, answer["session"], week)


def idSchoolList(idc) -> list or 1:
    authorisation = Authorization()
    loginTest = db.get(f'{idc}_login')
    if loginTest == False:
        return 1
    data = {
        "username": loginTest,
        "password": db.get(f'{idc}_password')
    }
    subdomain = db.get(f'{idc}_domain')

    answer = authorisation.login(subdomain, data)
    if "session" not in answer:
        print(answer)
        return 1

    SchoolList = Message()
    return SchoolList.schoolList(subdomain, answer["session"])


def peopleList(category) -> dict or 1:
    """
    ???????????????????? ???????????? ??????????

    Args:
        category ([str]): ["classruks", "administration", "specialists", "ext_5_teachers", "teachers", "parents",
                       "students"]

    Returns:
        [dict]: ??????:id
    """
    lists = idSchoolList(getID())[0][category]['user_list']
    return {f"{i['firstname']} {i['lastname']} {i['middlename']}": i['id'] for i in lists}


def idSend(idc, idp, message, name) -> bool or dict:
    authorisation = Authorization()
    loginTest = db.get(f'{idc}_login')
    if loginTest == False:
        return 1
    data = {
        "username": loginTest,
        "password": db.get(f'{idc}_password')
    }
    subdomain = db.get(f'{idc}_domain')

    answer = authorisation.login(subdomain, data)
    if "session" not in answer:
        print(answer)
        return 1

    args = {
        'receivers': str(idp),
        'subject':   str(name),
        'message':   str(message)
    }
    send = Message()
    return send.sendMessage(subdomain, answer["session"], args)


def idGet(idc) -> dict:
    authorisation = Authorization()
    loginTest = db.get(f'{idc}_login')
    if loginTest == False:
        return 1
    data = {
        "username": loginTest,
        "password": db.get(f'{idc}_password')
    }
    subdomain = db.get(f'{idc}_domain')

    answer = authorisation.login(subdomain, data)
    if "session" not in answer:
        print(answer)
        return 1

    message = Message()
    return message.getMessages(subdomain, answer["session"], {})


def idReport(idc) -> dict:
    authorisation = Authorization()
    loginTest = db.get(f'{idc}_login')
    if loginTest == False:
        return 1
    data = {
        "username": loginTest,
        "password": db.get(f'{idc}_password')
    }
    subdomain = db.get(f'{idc}_domain')

    answer = authorisation.login(subdomain, data)
    if "session" not in answer:
        print(answer)
        return 1

    portfolio = Portfolio()
    return portfolio.reportCard(subdomain, answer["session"], answer["answer"]["user"]["uid"])


def idFinal(idc, year) -> dict:
    authorisation = Authorization()
    loginTest = db.get(f'{idc}_login')
    if loginTest == False:
        return 1
    data = {
        "username": loginTest,
        "password": db.get(f'{idc}_password')
    }
    subdomain = db.get(f'{idc}_domain')

    answer = authorisation.login(subdomain, data)
    if "session" not in answer:
        print(answer)
        return 1

    portfolio = Portfolio()
    return portfolio.finalGrades(subdomain, answer["session"], answer["answer"]["user"]["uid"], year)


if __name__ == '__main__':
    # newUser(getID(), 'deniskedrovsky', 'Wtpmjgdaa1', '12ekb') # ???? ???????????? ?????? id
    # print(idProfile(getID())) # ??????????????
    print(idJournal(getID(), 0))  # ??????????????
    # print(peopleList("students")) # ??????????????
    # print(idSend(getID(), '3401', '????????', '?????????????????? ????????')) # ??????????????
    # print(idGet(getID())) # ??????????????
    # print(idReport(getID()))
    # print(idFinal(getID()))
    # print(idSchoolList(getID()))
