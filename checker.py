import datetime
import re

month = {"января": 1, "февраля": 2, "марта": 3, "апреля": 4, "мая": 5, "июня": 6,
         "июля": 7, "августа": 8, "сентября": 9, "октября": 10, "ноября": 11, "декабря": 12}


def checker(news, date_boarder):
    news = dict(news)
    ans = []
    for news_id, value in news.items():
        if re.search(r'[а-я]', value['date']) is None:
            date_parsed = value['date'].split(".")
            date = datetime.date(int(date_parsed[2]), int(date_parsed[1]), int(date_parsed[0]))
        else:
            date_parsed = value['date'].split(" ")
            date = datetime.date(int(date_parsed[2]), int(month[date_parsed[1]]), int(date_parsed[0]))

        if date > date_boarder:
            ans.append(int(news_id))
            continue
    return ans
