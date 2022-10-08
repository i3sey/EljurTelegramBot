from requests import Session
from Eljur.errors import _checkInstance, _checkStatus, _checkSubdomain, _fullCheck


class Profile:

    def getProfile(self, subdomain, session):
        # sourcery skip: dict-assign-update-to-union, inline-variable, switch
        """
        Получение информации о пользователе.
        Внимание. В данной функции специально не выводится СНИЛС, почта и мобильный телефон пользователя.

        :param subdomain: Поддомен eljur.ru                          // str
        :param session:   Активная сессия пользователя               // Session

        :return: Словарь с ошибкой или с информацией о пользователе: // dict
        """

        url = f"https://{subdomain}.eljur.ru/journal-user-preferences-action"

        soup = _fullCheck(subdomain, session, url)
        if "error" in soup:
            return soup

        label = None
        info = {}
        for tag in soup.find_all(["label", "span"], class_=["ej-form-label", "control-label"]):
            if tag.contents[0] == "СНИЛС":
                break

            if tag.name == "label":
                label = tag.contents[0]
                info.update([(label, None)])

            elif tag.name == "span":
                info[label] = tag.contents[0]

        return info


class Security:

    def changePassword(self, subdomain, session, old_password, new_password):
        """
        Изменение пароля в личном кабинете пользователя.

        :param subdomain:    Поддомен eljur.ru                                       // str
        :param session:      Активная сессия пользователя                            // Session
        :param old_password: Старый пароль.                                          // str
        :param new_password: Новый пароль, который пользователь желает использовать. // str

        :return: Словарь с ошибкой или bool ответ, в котором True - успешная смена пароля // dict или bool
        """

        subdomain = _checkSubdomain(subdomain)
        if "error" in subdomain:
            return subdomain

        checkSession = _checkInstance(session, Session)
        if "error" in checkSession:
            return checkSession
        del checkSession

        url = f"https://{subdomain}.eljur.ru/journal-messages-compose-action"
        getCookies = session.get(url=url, data={"_msg": "sent"})

        checkStatus = _checkStatus(getCookies, url)
        if "error" in checkStatus:
            return checkStatus
        del checkStatus

        data = {"csrf": getCookies.cookies.values()[0],
                "old_password": old_password,
                "new_password": new_password,
                "verify": new_password,
                "submit_button": "Сохранить"}

        url = f"https://{subdomain}.eljur.ru/journal-user-security-action/"
        answer = session.post(url=url, data=data)

        checkStatus = _checkStatus(answer, url)
        if "error" in checkStatus:
            return checkStatus
        del checkStatus

        return "Ваш пароль успешно изменен!" in answer.text


class Settings:

    def changeSing(self, subdomain, session, text):
        """
        Изменение подписи в новых сообщениях пользователя.

        :param subdomain: Поддомен eljur.ru                                                     // str
        :param session:   Активная сессия пользователя                                          // Session
        :param text:      Текст подписи                                                         // str

        :return: Словарь с ошибкой или bool ответ, в котором True - успешное изменение подписи. // dict или bool
        """

        subdomain = _checkSubdomain(subdomain)
        if "error" in subdomain:
            return subdomain

        checkSession = _checkInstance(session, Session)
        if "error" in checkSession:
            return checkSession
        del checkSession

        url = f"https://{subdomain}.eljur.ru/journal-index-rpc-action"
        data = {"method": "setPref",
                "0": "msgsignature",
                "1": text}

        changeSing = session.post(url=url, data=data)

        checkStatus = _checkStatus(changeSing, url)
        if "error" in checkStatus:
            return checkStatus

        return False if "result" not in checkStatus else checkStatus["result"]

    def switcher(self, subdomain, session, choose, switch):
        """
        Переключение настраиваиваемых функций в настройках.
        Доступно переключение следующих функций:
        `Отмечать сообщение прочитанным при его открытии на электронной почте` // 0 или checkforwardedemail
        `Отображать расписание обучающегося по умолчанию (вместо расписания класса)` // 1 или schedule_default_student

        :param subdomain: Поддомен eljur.ru                                                // str
        :param session: Активная сессия пользователя                                       // Session
        :param choose: Выбор переключаемой функции                                         // int или str
        :param switch: True/False                                                          // bool

        :return: Словарь с ошибкой или bool ответ, в котором True - успешное переключение. // dict или bool
        """

        strSwitch = ["checkforwardedemail", "schedule_default_student"]
        switchers = {"checkforwardedemail": {"on": "on",
                                             "off": "off"},
                     "schedule_default_student": {"on": "yes",
                                                  "off": "no"}}
        data = {"method": "setPref",
                "0": None,
                "1": None}

        subdomain = _checkSubdomain(subdomain)
        if "error" in subdomain:
            return subdomain

        checkSession = _checkInstance(session, Session)
        if "error" in checkSession:
            return checkSession
        del checkSession

        checkInt = _checkInstance(choose, int)
        if "error" in checkInt:
            checkStr = _checkInstance(choose, str)
            if "error" in checkStr:
                return checkStr
            if choose not in strSwitch:
                numStrSwitch = ["0", "1"]
                if choose in numStrSwitch:
                    data["0"] = strSwitch[int(choose)]
                else:
                    return {"error": {"error_code": -302,
                                      "error_msg": f"Вашего выбора нет в предложенных. {choose}"}}
            data["0"] = choose
        else:
            numSwitch = [0, 1]
            if choose not in numSwitch:
                return {"error": {"error_code": -302,
                                  "error_msg": f"Вашего выбора нет в предложенных. {choose}"}}
            data["0"] = strSwitch[choose]

        checkBool = _checkInstance(switch, bool)
        if "error" not in checkBool:
            return checkBool
        del checkBool, checkStr, checkInt

        if switch:
            data["1"] = switchers[data["0"]]["on"]
        else:
            data["1"] = switchers[data["0"]]["off"]

        url = f"https://{subdomain}.eljur.ru/journal-index-rpc-action"
        changeSing = session.post(url=url, data=data)

        checkStatus = _checkStatus(changeSing, url)
        if "error" in checkStatus:
            return checkStatus

        return False if "result" not in checkStatus else checkStatus["result"]
