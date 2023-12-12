from numpy import sin, cos, arccos
import random
from retry import retry
from datetime import datetime, timezone, timedelta
import os
import numpy as np
import googlemaps

import time
import re
import json
import secrets

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort

from foodiebot.auth import login_required
from foodiebot.db import get_db


bp = Blueprint('restaurant', __name__, url_prefix='/restaurant')


api_key = 'AIzaSyC5FeD_HmfWXFtg-q1_3U5UXgLGzWXFxQE'
gmaps = googlemaps.Client(key=api_key)


@bp.route('/user_input', methods=('GET', 'POST'))
def user_input():
    if request.method == 'POST':
        parameters = json.loads(request.form['parameters'])
        session['parameters'] = parameters

        categories = []
        if parameters['manual'] != '':
            categories = [parameters['manual']]
        else:
            # sort categories according to weight
            categories_weight = {'Chinese restaurant': 3, 'Chicken restaurant': 2,
                                 'Ramen restaurant': 1, 'Cold noodle restaurant': 1,
                                 'Deli': 10, 'Restaurant': 10, 'Italian restaurant': 2,
                                 'Noodle shop': 8, 'Chinese noodle restaurant': 3,
                                 'Dumpling restaurant': 2, 'Cantonese restaurant': 4,
                                 'Porridge restaurant': 1, 'Taiwanese restaurant': 4,
                                 'Hong Kong style fast food restaurant': 3, 'Mandarin restaurant': 4}

            p = np.zeros(len(categories_weight))
            i = 0
            for key, val in categories_weight.items():
                categories.append(key)
                p[i] = val
                i += 1

            p /= p.sum()

            rng = np.random.default_rng(secrets.randbits(128))

            categories = rng.choice(categories, size=len(
                categories), replace=False, p=p)

        category, result = get_restaurant(parameters, categories)

        if result is None:
            return redirect(url_for('restaurant.error'))
        else:
            session['category'] = category
            session['result'] = result
            return redirect(url_for('restaurant.show_result'))

    return render_template('restaurant/user_input.html')


@bp.route('/test')
def test():
    return render_template('restaurant/test.html')


@bp.route('/error')
def error():
    return render_template('restaurant/error.html')


@bp.route('/show_result', methods=('GET', 'POST'))
def show_result():
    return render_template('restaurant/show_result.html')


@retry((Exception), tries=3, delay=2, backoff=0)
def get_restaurant(parameters, categories):

    if parameters['cheap'] == 1 and parameters['expensive'] == 0:
        min_price = 0
        max_price = 1
    elif parameters['cheap'] == 0 and parameters['expensive'] == 1:
        min_price = 2
        max_price = 4
    else:
        min_price = 0
        max_price = 4

    restaurants = []

    # 抽取
    for category in categories[:7]:
        places_params = {
            'query': category,
            'location': parameters['location'],
            'radius': parameters['radius'] * 1000,
            'language': 'zh-TW',
            'min_price': min_price,
            'max_price': max_price,
            'open_now': parameters['open']
        }

        search_results = gmaps.places(**places_params)

        append_restaurant(search_results, parameters,
                          restaurants, max_price, min_price)

        while search_results.get('next_page_token'):
            time.sleep(2)
            places_params['page_token'] = search_results.get('next_page_token')
            search_results = gmaps.places(**places_params)
            append_restaurant(search_results, parameters,
                              restaurants, max_price, min_price)

        if len(restaurants) > 0:
            rng = np.random.default_rng(secrets.randbits(128))
            result = rng.choice(restaurants, size=1)[0]
            return category, result

    return None, None


def append_restaurant(search_results, parameters, restaurants, max_price, min_price):
    for restaurant in search_results['results']:
        if (restaurant['rating'] >= parameters['star'] and
            restaurant['price_level'] <= max_price and
            restaurant['price_level'] >= min_price and
                calculate_distance(parameters['location'], restaurant['geometry']['location']) <= parameters['radius']):

            restaurants.append(restaurant)


def calculate_distance(location, place):
    # 公里
    r = 6371.0

    # 所在地經緯度radian
    lng1 = np.radians(location['lng'])
    lat1 = np.radians(location['lat'])

    # 目的地
    lng2 = np.radians(place['lng'])
    lat2 = np.radians(place['lat'])

    return round(r * arccos(cos(lat1) * cos(lat2) * cos(lng1 - lng2) + sin(lat1) * sin(lat2)), 2)
