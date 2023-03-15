from Eljur.errors import _fullCheck


class Timetable:

    def numklassGetting(self, subdomain, session, week=0):
        """
        Получение страницы расписания.

        :param week:      Нужная вам неделя (even, odd, both)      // str
        :param subdomain: Поддомен eljur.ru                        // str
        :param session:   Активная сессия пользователя             // Session

        :return: Словарь с ошибкой или с расписанием пользователя: // dict
                 answer // dict
                 result // bool
        """
        url = f'https://{subdomain}.eljur.ru/journal-schedule-action/'
        
        soup = _fullCheck(subdomain, session, url)
        if "error" in soup:
            return soup
        
        if answer := soup.find("td", class_="left left_min"):
            return answer
            
        
        return

    def journal(self, subdomain, session, week=0):
        """
        Получение страницы дневника с расписанием и оценками.

        :param subdomain: Поддомен eljur.ru                                             // str
        :param session:   Активная сессия пользователя                                  // Session
        :param week:      Нужная вам неделя (0, -1, 3 и.т.д). По умолчанию 0 (нынешняя) // str

        :return: Словарь с ошибкой или с расписанием пользователя:                      // dict
                 answer // dict
                 result // bool
        """
        return
