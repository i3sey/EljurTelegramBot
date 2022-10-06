from bot.Eljur.errors import _fullCheck


def _checkForID(lesson_id):
    return lesson_id.has_attr("data-lesson_id")


def _pattern(att):
    return {"Всего": att.contents[3].contents[0], "По болезни": att.contents[5].contents[0], "По ув. причине": att.contents[7].contents[0], "По неув. причине": att.contents[9].contents[0]}


class Portfolio:

    def reportCard(self, subdomain, session, user_id, quarter="I"):
        """
        Получение списка оценок.

        :param subdomain: Поддомен eljur.ru                                                     // str
        :param session:   Активная сессия пользователя                                          // Session
        :param user_id:   ID пользователя                                                       // str
        :param quarter:   Четверть (I, II, III, IV)                                             // str

        :return: Словарь с ошибкой или ответом (отсутствие оценок или словарь с оценками)       // dict
        """

        url = f"https://{subdomain}.eljur.ru/journal-student-grades-action/u.{user_id}/sp.{quarter}+четверть"

        soup = _fullCheck(subdomain, session, url)
        if "error" in soup:
            return soup

        if answer := soup.find("div", class_="page-empty"):
            return {"answer": answer.contents[0],
                    "result": False}

        card = {}
        subjects = soup.find_all("div", class_="text-overflow lhCell offset16")

        for subject in subjects:
            scores = [{score.attrs["mark_date"], score.contents[1].contents[0]} for score in soup.find_all("div", class_=["cell blue", "cell"], attrs={"name": subject.contents[0]}) if "mark_date" in score.attrs and score.attrs["id"] != "N"]

            card |= [(subject.contents[0], scores)]
        card.update(result=True)

        return card

    def attendance(self, subdomain, session, user_id, quarter="I"):
        """
        Изменение подписи в новых сообщениях пользователя.

        :param subdomain: Поддомен eljur.ru                                                             // str
        :param session:   Активная сессия пользователя                                                  // Session
        :param user_id:   ID пользователя                                                               // str
        :param quarter:   Четверть (I, II, III, IV)                                                     // str

        :return: Словарь с ошибкой или ответом в виде словаря с предметами и пропущенными уроками       // dict
        """
        url = f"https://{subdomain}.eljur.ru/journal-app/view.miss_report/u.{user_id}/sp.{quarter}+четверть"

        soup = _fullCheck(subdomain, session, url)
        if "error" in soup:
            return soup

        if answer := soup.find("div", class_="page-empty"):
            return {"answer": answer.contents[0],
                    "result": False}

        card = {}
        subjects = soup.find_all(_checkForID)

        for subject in subjects:
            lessonInfo = _pattern(subject)
            if not subject.contents[1].contents:
                subject.contents[1].contents = ["Всего"]
            card |= [(subject.contents[1].contents[0], lessonInfo)]

        days = soup.find_all("tr", attrs={"xls": "hrow"})
        daysInfo = _pattern(days[1])

        card.update([(days[1].contents[1].contents[0], daysInfo)])

        return card
