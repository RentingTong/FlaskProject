# -*- coding: utf-8 -*-
"""
@date: 2020/09/17

@author: Tara

@description:
A weather widget.
"""
from flask import Flask, request, session, render_template
import os
import json
import ssl
import urllib.request

app = Flask(__name__, static_url_path="/static", static_folder="static")


@app.route("/", methods=["GET", "POST"])
def weather():
    meta_data = get_meta_data()['weather']
    api_key, basic_url = meta_data['api_key'], meta_data['basic_url']
    city = request.form['city'] if request.method == "POST" else meta_data['city']

    context = ssl._create_unverified_context()
    source = urllib.request.urlopen(url=f"{basic_url}q={city}&appid={api_key}&units=metric", context=context).read()

    data = get_target_data(json.loads(source))
    return render_template('weather.html', data=data)


# @app.route("/get_city", methods=["GET", "POST"])
# def get_input():
#     if request.method == "POST":
#         city = request.form['city']
#         # for k, v in request.form.items():
#         # print(f"{k} : {v}")
#         return city

# @app.route("/<city>", methods=["GET", "POST"])
# def specified_weather(city):
#     meta_data = get_meta_data()['weather']
#     api_key, basic_url = meta_data['api_key'], meta_data['basic_url']
#     city = city if request == "POST" else meta_data['city']
#
#     context = ssl._create_unverified_context()
#     source = urllib.request.urlopen(url=f"{basic_url}q={city}&appid={api_key}", context=context).read()
#
#     data = get_target_data(json.loads(source))
#     return render_template('weather.html', data=data)


def get_meta_data():
    """
    Get meta date from meta.json.
    :return: dict
    """
    meta_file_path = os.path.join(os.path.dirname(__file__), "meta.json")
    with open(meta_file_path) as f:
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
        "city": str(data_dict['name']),
        "coordinate": str(data_dict['coord']['lon']) + ' ' +
                      str(data_dict['coord']['lat']),
        "weather": str(data_dict['weather'][0]['main']) + ' - ' +
                   str(data_dict['weather'][0]['description']),
        "temp": str(data_dict['main']['temp']) + "°C",
        "temp_f": "{:.2f}".format(data_dict['main']['temp']*9/5 + 32) + "°F",
        "pressure": str(data_dict['main']['pressure']),
        "humidity": str(data_dict['main']['humidity']),
    }
    return data


@app.errorhandler(401)
def invalid_api_key(error):
    return "Invalid API Key", 401


@app.errorhandler(404)
def page_not_found(error):
    return "Not Found", 404


if __name__ == "__main__":
    app.run(debug=True)

    # api_key = json.loads("meta.json")
    # print(api_key)
    # print(get_meta_data())

    # import os
    # pictures_list = [f for f in os.listdir("/Users/tong/Documents/code/FlaskProject/app/static/img/")]
    # print(pictures_list)
    # print(len(pictures_list))
