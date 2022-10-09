import pymorphy2

morph = pymorphy2.MorphAnalyzer(lang='ru')

# https://pymorphy2.readthedocs.io/en/stable/user/grammemes.html
stopwords = ['NPRO', 'PREP', 'CONJ', 'PRCL', 'INTJ']


# Создаем мешки слов
def make_bag(text):
    text = text.lower()
    new_text = ""
    for s in text:
        if s.isalpha() or s.isnumeric() or s in " -$₽₿£¥€#@()%+":
            new_text += s
    words = new_text.split()
    total_words = set()
    for word in words:
        parsed_word = morph.parse(word)[0]
        if parsed_word.tag.POS in stopwords:
            continue
        total_words.add(parsed_word.normal_form)
    return total_words


def make_all_bags(data):
    all_bags = [set()] * len(data)
    for i, d in data.items():
        all_bags[int(i)] = make_bag(d['news'])
    return all_bags


def classify(test, all_bags):
    ratings = []
    for text in test:
        text_bag = make_bag(text)
        sum_pred = 0
        for bag in all_bags:
            score = len(text_bag.intersection(bag)) / len(text_bag.union(bag))
            sum_pred += score
        ratings.append(sum_pred)
    return ratings
