from bs4 import BeautifulSoup
from requests import Session, post
import json
from bot.Eljur.errors import _checkStatus, _checkSubdomain, _findData


class Authorization:

    def register(self, code):
        """
        Регистрация пользователя eljur.ru.

        :param code: Единоразовый код, который можно получить в школе. // str

        :return: code/Не завершено                                     // str
        """
        return code

    def login(self, subdomain, data):
        """
        Подключение к пользователю eljur.ru.

        :param subdomain: Поддомен eljur.ru                             // str
        :param data:      Дата, состоящая из {"username": "ваш логин",
                                              "password": "ваш пароль"} // dict

        :return: Словарь с ошибкой или с положительным ответом:         // dict
                 answer // dict
                 session // Session
                 subdomain // str
                 result // bool
        """

        subdomain = _checkSubdomain(subdomain)
        if "error" in subdomain:
            return subdomain

        session = Session()
        url = f"https://{subdomain}.eljur.ru/ajaxauthorize"
        err = session.post(url=url, data=data)

        checkStatus = _checkStatus(err, url)
        if "error" in checkStatus:
            return checkStatus
        del checkStatus

        if not err.json()["result"]:
            return {"error": {"error_code": -103,
                              "error_msg": err.json()['error'],
                              "full_error": err.json()}}
        del err

        url = f"https://{subdomain}.eljur.ru/?show=home"
        account = session.get(url=url)
        checkStatus = _checkStatus(account, url)
        if "error" in checkStatus:
            return checkStatus

        soup = BeautifulSoup(account.text, 'lxml')

        sentryData = _findData(soup)
        del soup
        return {"answer": json.loads(sentryData[17:-1]), "session": session, "subdomain": subdomain, "result": True} if sentryData else {"error": {"error_code": -104, "error_msg": "Данные о пользователе не найдены."}}

    def recover(self, subdomain, email):
        """
        Восстановление пароля пользователя eljur.ru. через почту.

        Внимание! Для использования данной функции требуется привязать почту.
        В ином случае восстановление происходит через Администратора или другого лица вашей школы.

        :param subdomain: Домен вашей школы.                        // str
        :param email:     Ваша почта, привязанная к аккаунту eljur  // str

        :return: Словарь с ошибкой или с положительным ответом:     // dict
                 answer // dict
                 result // bool
        """

        subdomain = _checkSubdomain(subdomain)
        if "error" in subdomain:
            return subdomain

        url = f"https://{subdomain}.eljur.ru/ajaxrecover"
        answer = post(url=url,
                      data={"email": email})

        checkStatus = _checkStatus(answer, url)
        if "error" in checkStatus:
            return checkStatus

        return {"answer": "Сообщение успешно отправлено на почту.", "result": True} if answer.json()["result"] else {"error": {"error_code": -105, "error_msg": answer.json()['error'], "full_error": answer.json()}}
