from numpy import sin, cos, arccos
import random
from retry import retry
from datetime import datetime
import os
import pandas as pd
import numpy as np
import googlemaps
import functools
import json
import re

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort

from foodiebot.auth import login_required
from foodiebot.db import get_db


bp = Blueprint('restaurant', __name__, url_prefix='/restaurant')


def check_input_valid(inputs):
    return True


@bp.route('/choose_restaurant', methods=('GET', 'POST'))
@login_required
def user_input():
    result = None

    error = None
    if request.method == 'POST':

        if error is not None:
            flash(error)

        else:

            location_json = request.form['location']
            location = [float(s)
                        for s in re.findall(r'-?\d+.?\d*', location_json)]
            # location = tuple(location)
            params = {'lat': location,
                      'user_id': session['user_id']}

            session['result'] = choose_restaurant(params)

            return redirect(url_for("restaurant.show_result"))

    return render_template('restaurant/user_input.html')


@bp.route('/result')
def show_result():
    return render_template('restaurant/show_result.html')


@bp.route('/clearing')
@login_required
def clear_session():
    session['token'] = True
    session['result'] = []
    # can do some pow

    return redirect(url_for('restaurant.user_input'))


api_key = os.environ['GOOGLEMAP_API_KEY']
gmaps = googlemaps.Client(key=api_key)


def check_white(category, name):
    ''' 
    手動排除不好的東西...有待改進...
    '''

    if category in ["水餃",  "鍋貼"]:
        if "生水餃" or "冷凍" or "八方" in name:
            return False
    return True


def calculate_distance(lat, place):
    r = 6371.0

    # 所在地經緯度radian
    lat1, long1 = np.radians(lat)

    # 目的地
    long2 = np.radians(place['lng'])
    lat2 = np.radians(place['lat'])

    return round(r * arccos(cos(lat1) * cos(lat2) * cos(long1 - long2) + sin(lat1) * sin(lat2)), 2)


class user:
    def __init__(self, user_id, lat=None,
                 money=0, manypeople=0, radius=0.5, rating=3.5,  manual=None,
                 now_hour=datetime.now().hour, now_month=datetime.now().month, open=False):

        self.categories = None

        # 不吃類別
        self.user_id = user_id

        BL = get_db().execute(
            'SELECT name'
            ' FROM black_list'
            ' WHERE user_id = ?',
            (user_id,)
        ).fetchall()

        self.black_list = [bl['name'] for bl in BL]

        self.vegie = False

        # 不需問的資訊
        self.lat = lat
        self.now_hour = now_hour
        self.now_month = now_month

        # 手動輸入類別，直接取代list,若有新東西，也可加入預設類別！
        self.manual = manual

        # 要設計問題把東西問出來
        self.money = money
        self.manypeople = manypeople

        # 有機車2, 走路0.5
        self.radius = radius
        self.rating = rating

        # 不一定要開門
        self.open = open

        self.testing = None
        # 結果
        self.category = None
        self.result = None
        self.restaurant_information = None

    def get_categories(self):
        '''
        對搜尋類別進行限縮，直接從SQL資料庫撈
        '''

        # 處理時間
        if self.now_hour in range(10, 16):
            meal = 'lunch'
        elif self.now_hour in range(16, 22):
            meal = 'dinner'
        elif self.now_hour in range(5, 10):
            meal = 'morning'
        else:
            meal = 'night'

        # 溫度食物
        if self.now_month in range(7, 11):
            # 有些東西要炎熱才會吃
            temperature = 'hot'
        elif self.now_month in range(1, 5) or self.now_month == 12:
            # 有些東西要寒冷才會吃
            temperature = 'cold'
        else:
            temperature = 'ordinary'

        categories = get_db().execute(
            'SELECT f.category'
            ' FROM food f'
            ' WHERE ' + meal + '= 1'
            ' AND ' + temperature + '= 1'
            ' AND money BETWEEN 0 AND ? AND'
            ' manypeople BETWEEN 0 AND ? AND'
            ' f.category NOT IN('
            '  SELECT category FROM no_eat'
            '  WHERE user_id = ?'
            ' ) AND'
            ' f.category NOT IN ('
            '   SELECT category FROM last_eat'
            '   WHERE user_id = ?'
            ' );',
            (self.money, self.manypeople, self.user_id, self.user_id)
        ).fetchall()

        self.categories = [cat['category'] for cat in categories]

        # 把類別打亂
        random.shuffle(self.categories)

    @retry((Exception), tries=3, delay=2, backoff=0)
    def choose_food(self):
        '''
        回傳搜尋類別以及結果
        '''
        for category in self.categories[:10]:

            params = {
                'query': category,
                'location': self.lat,
                'radius': self.radius * 1000,
                'language': 'zh-TW',
                'max_price': self.money+1,
                'open_now': self.open
            }

            result = gmaps.places(**params)

            final_result = []

            # 過濾黑名單, 過濾評分太低
            for restaurant in result['results']:
                if (restaurant['rating'] > self.rating and
                    check_white(category, restaurant['name']) and
                        restaurant['name'] not in self.black_list and
                        calculate_distance(self.lat, restaurant['geometry']['location']) < self.radius):

                    if not self.vegie and '素' in restaurant['name']:
                        continue

                    # 檢查是否夠格
                    final_result.append(restaurant)

            m = len(final_result)
            if m > 1:
                self.category = category
                self.result = final_result
                self.restaurant_information = np.random.choice(self.result)
                break


def choose_restaurant(params):

    use = user(**params)
    use.get_categories()
    use.choose_food()

    # return {
    #    'category': np.random.random(),
    #    'name': np.random.random(),
    #    'star': np.random.random(),
    #    'distance': np.random.random()
    # }
    if use.restaurant_information is None:
        return "請將距離調大，或調整起始位置"

    return {
        'category': use.category,
        'name': use.restaurant_information['name'],
        'star': use.restaurant_information['rating'],
        'distance': calculate_distance(
            use.lat, use.restaurant_information['geometry']['location']),
    }
