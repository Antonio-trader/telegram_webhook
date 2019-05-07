from flask import Flask
from flask import request
from flask import jsonify
import requests
import json
import re

from flask_sslify import SSLify


app = Flask(__name__)
sslify = SSLify(app)


URL = 'https://api.telegram.org/bot778975045:AAHoTOIAkeR6BLYf6cG_WTxp8CAJ7dHoxPg/'


def write_json(data, filename='answer.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def send_message(chat_id, text='bla-bla-bla'):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer)
    return r.json()


def parse_text(text):
    pattern = r'/\w+'
    weather = re.search(pattern, text).group()
    return weather[1:]


def get_result(city):
    api_url = "http://api.openweathermap.org/data/2.5/weather"

    params = {
        'q': city,
        'appid': '11c0d3dc6093f7442898ee49d2430d20',
        'units': 'metric'
    }

    res = requests.get(api_url, params=params)
    data = res.json()
    template = 'Current temperature in {} is {}\nClouds = {}%\nSpeed wind is {} m/sec'
    return (template.format(city,
                          data["main"]["temp"],
                          data["clouds"]["all"],
                          data["wind"]["speed"]))


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        message = r['message']['text']

        pattern = r'/\w+'

        if re.search(pattern, message):
            w_result = get_result(parse_text(message))
            send_message(chat_id, text=w_result)

        return jsonify(r)
    return '<h1>Bot welcomes you</h1>'


if __name__ == '__main__':
    app.run()

