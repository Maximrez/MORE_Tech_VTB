from sentence_transformers import SentenceTransformer
from math import sqrt, exp


def count_score(v1, v2):
    return exp(-sqrt(sum(map(lambda x: x ** 2, (v1[i] - v2[i] for i in range(len(v1)))))))


def make_embeddings(data, show=False):
    all_news = [""] * len(data)
    for i, d in data.items():
        all_news[int(i)] = d['news']

    model = SentenceTransformer('distilbert-base-nli-mean-tokens')
    embeddings = model.encode(all_news, show_progress_bar=show)

    return embeddings


def vectorise(test, embeddings, answers):
    entry_to1 = 0.0035
    entry_to2 = 0.0015

    classes = []

    for text in test:
        text_vector = make_embeddings({'0': {'news': text}})[0]
        sum_pred1 = 0
        sum_pred2 = 0
        count_scores = 0
        for v2, to in zip(embeddings, answers):
            score = count_score(text_vector, v2)
            count_scores += 1
            if to == 1:
                sum_pred1 += score
            elif to == 2:
                sum_pred2 += score
            elif to == 3:
                sum_pred1 += score
                sum_pred2 += score
        p_to1 = sum_pred1 / count_scores
        p_to2 = sum_pred2 / count_scores

        if p_to1 >= entry_to1 and p_to2 >= entry_to2:
            classes.append((3, p_to1 + p_to2))
        elif p_to1 >= entry_to1:
            classes.append((1, p_to1))
        elif p_to2 >= entry_to2:
            classes.append((2, p_to2))
        else:
            classes.append((0, 0))

    return classes
