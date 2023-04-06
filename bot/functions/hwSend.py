import re
import json

async def hwSend(text):
    page = []
    num = []
    match = re.search('<b>(.*?)</b>', text)
    if match:
        subject = match.group(1)
    matches = re.findall('<code>(.*?)</code>', text)
    if len(matches) >= 2:
        hw = json.loads(matches[1].replace("'", '"'))
    if (len(hw['page']) if "page" in hw else 0) > 1 and (len(hw['number']) if "number" in hw else 2) <= 1:
        for i in hw['page']:
            page = page + ', ' + i
        return f'Предмет - <b>{subject}</b>, ищу гдз{" страница " + page if "page" in hw else ""}{", номер " + hw["number"][0] if "number" in hw else ""}', page, hw["number"][0] if "number" in hw else "", subject
    elif (len(hw['number']) if "number" in hw else 0) > 1 and (len(hw['page']) if "page" in hw else 2) <= 1:
        for i in hw['number']:
            num.append(i)
        return f'Предмет - <b>{subject}</b>, ищу гдз{" страница " + hw["page"][0] if "page" in hw else ""}{", номер " + num[0] if "number" in hw else ""}', hw["page"][0] if "page" in hw else "", num, subject
    elif (len(hw['number']) if "number" in hw else 0) > 1 and (len(hw['page']) if "page" in hw else 0) > 1:
        for i in hw['page']:
            page = page + ', ' + i
        for i in hw['number']:
            num.append(i)
        return f'Предмет - <b>{subject}</b>, ищу гдз{" страница " + page if "page" in hw else ""}{", номер " + num if "number" in hw else ""}', page, num, subject
    else:
        return f'Предмет - <b>{subject}</b>, ищу гдз{" страница " + hw["page"][0] if "page" in hw else ""}{", номер " + hw["number"][0] if "number" in hw else ""}', hw["page"][0] if "page" in hw else "", hw["number"][0] if "number" in hw else "", subject
