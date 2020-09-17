# -*- coding: utf-8 -*-
"""
@date: 2020/09/17

@author: Tara

@description:
A weather widget.
"""
from flask import Flask, render_template, request
import json
import urllib.request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def weather():
    city = request.form["city"] if request == "POST" else "Shanghai"
    meta_data = get_meta_data()
    api_key, basic_url = meta_data['api_key'], meta_data['basic_url']

    source = urllib.request.urlopen(f"{basic_url}q={city}&appid={api_key}").read()

    data = get_target_data(json.loads(source))
    return render_template('index.html', data=data)


def get_meta_data():
    with open('meta.json') as f:
        meta_data = json.load(f)
    return meta_data


def get_target_data(data_dict):
    '''
    Get wanted return weather data.
    :param data_dict: dict
    :return: dict
    '''
    data = {
        "country_code": str(data_dict['sys']['country']),
        "coordinate": str(data_dict['coord']['lon']) + ' ' +
                      str(data_dict['coord']['lat']),
        "temp": str(data_dict['main']['temp']) + 'k',
        "pressure": str(data_dict['main']['pressure']),
        "humidity": str(data_dict['main']['humidity']),
    }
    return data


@app.errorhandler(401)
def invalid_api_key():
    return "Invalid API Key", 401


@app.errorhandler(404)
def page_not_found():
    return "Not Found", 404


if __name__ == "__main__":
    # app.run(debug=True)
    # api_key = json.loads("meta.json")
    # print(api_key)
    print(get_meta_data())
