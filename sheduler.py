import time
import datetime
import os
from interfaxParser import interfax_parse
from RIAparser import ria_parse
from RTparser import rt_parse
from checker import checker, month
import json
from classification import make_all_bags, classify
from vectorizing import make_embeddings, vectorise


def totimestamp(dt, epoch=datetime.datetime(1970, 1, 1)):
    td = dt - epoch
    return (td.microseconds + (td.seconds + td.days * 86400) * 10 ** 6) // 10 ** 6


def main(all_bags, embeddings, answers):
    interfax_parse()
    ria_parse()
    rt_parse()

    all_data = {'News': []}
    texts = []

    days = 5
    date_ago = datetime.date.today() - datetime.timedelta(days=days)
    with open("data/ria.json", "r", encoding='utf-8') as json_file:
        data = json.load(json_file)

    ria_ids = checker(data, date_ago)
    for i in ria_ids:
        current_news = data[str(i)]
        all_data['News'].append({'id': len(all_data['News']),
                                 'To': None,
                                 'Title': current_news['header'],
                                 'URL': current_news['url'],
                                 'Date': totimestamp(datetime.datetime.strptime(current_news['date'], '%d.%m.%Y')),
                                 'Rating': None})
        texts.append(current_news['news'])

    with open("data/rt_news.json", "r", encoding='utf-8') as json_file:
        data = json.load(json_file)

    rt_ids = checker(data, date_ago)
    for i in rt_ids:
        current_news = data[str(i)]
        date = current_news['date'].split()
        date[0] = '0' * (2 - len(date[0])) + date[0]
        date[1] = '0' * (2 - len(str(month[date[1]]))) + str(month[date[1]])
        all_data['News'].append({'id': len(all_data['News']),
                                 'To': None,
                                 'Title': current_news['header'],
                                 'URL': current_news['url'],
                                 'Date': totimestamp(datetime.datetime.strptime(".".join(date), '%d.%m.%Y')),
                                 'Rating': None})
        texts.append(current_news['news'])

    with open("data/interfax_news.json", "r", encoding='windows-1251') as json_file:
        data = json.load(json_file)

    interfax_ids = checker(data, date_ago)
    for i in interfax_ids:
        current_news = data[str(i)]
        date = current_news['date'].split()
        date[0] = '0' * (2 - len(date[0])) + date[0]
        date[1] = '0' * (2 - len(str(month[date[1]]))) + str(month[date[1]])
        all_data['News'].append({'id': len(all_data['News']),
                                 'To': None,
                                 'Title': current_news['header'],
                                 'URL': current_news['url'],
                                 'Date': totimestamp(datetime.datetime.strptime(".".join(date), '%d.%m.%Y')),
                                 'Rating': None})
        texts.append(current_news['news'])

    bag_ratings = classify(texts, all_bags)
    vector_ratings = vectorise(texts, embeddings, answers)

    for i in range(len(all_data['News'])):
        all_data['News'][i]['Rating'] = bag_ratings[i] + 10000 * vector_ratings[i][1]
        all_data['News'][i]['To'] = vector_ratings[i][0]

    with open("news.json", "w", encoding='utf-8') as out:
        out.write(json.dumps(all_data, ensure_ascii=False))


if __name__ == '__main__':
    with open('razmet.json', encoding='utf-8') as f:
        data = json.load(f)

    all_bags = make_all_bags(data)
    embeddings = make_embeddings(data, True)
    answers = list(data[i]['to'] for i in data.keys())

    if not os.path.exists('data'):
        os.mkdir('data')
    time_to_sleep = 60 * 60
    while True:
        main(all_bags, embeddings, answers)
        print(f'Task completed at {datetime.datetime.now()}, waiting {time_to_sleep} seconds...')
        time.sleep(time_to_sleep)
