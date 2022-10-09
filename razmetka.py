import json

with open("1stTry.json", "r", encoding='utf-8') as json_file:
    data = json.load(json_file)

with open("razmet.json", "w", encoding='utf-8') as out:
    mini_data = {}
    for i in data:
        news = data[i]
        print(news['header'])
        to = int(input())
        if to == -1:
            print('Last id: {}', i)
            break
        # -1 - выход, 0 - никому, 1-директору, 2 - бухгалтеру, 3 - обоим
        mini_data[i] = news
        mini_data[i]['to'] = to
    out.write(json.dumps(mini_data, ensure_ascii=False))
