#!flask/bin/python
import json
import datetime

from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__, static_url_path="")
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'admin':
        return 'pigs'
    if username == "user":
        return "pass"
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


class News:
    def __init__(self, json_data):
        self.id = json_data["id"]
        self.title = json_data["Title"]
        self.url = json_data["URL"]
        self.to = json_data["To"]
        self.date = json_data["Date"]
        self.rating = json_data["Rating"]

    def __str__(self):
        return "id: " + self.id + "\nTitle: " + self.title + "\nURL: " + self.url


def get_all_news(who, date, count):
    with open('news.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        filtered_news = []
        for news in data['News']:
            if int(news['Date']) >= date and (int(news['To']) == who or int(news['To']) == 3):
                filtered_news.append(news)

        if len(filtered_news) > count:
            sorted(filtered_news, key=lambda news_: news_['Rating'])
            return filtered_news[-count:]
        else:
            return filtered_news


def make_public_news(news):
    new_news = []
    for n in news:
        d = {'URL': n['URL'], "Title": str(n["Title"]).strip(),
             "Date": str(datetime.date.fromtimestamp(n['Date']))}
        new_news.append(d)
    return new_news


@app.route('/vtb/api/v1.0/news', methods=['GET'])
@auth.login_required
def get_news():
    req = request.args

    who = int(req['who'])
    count = int(req.get("count", 3))
    if who != 1 and who != 2 or count < 1:
        abort(400)

    date = req['date']
    dates = list(map(int, date.split(".")))
    date = datetime.date(dates[2], dates[1], dates[0])
    date = datetime.datetime.fromisoformat(date.isoformat())

    return json.dumps({'news': make_public_news(get_all_news(who, date.timestamp(), count))}, ensure_ascii=False, separators=(',\n', ': '))


if __name__ == '__main__':
    app.run(debug=True)
