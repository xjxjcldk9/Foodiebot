from numpy import sin, cos, arccos
import random
from retry import retry
from datetime import datetime
import os
import numpy as np
import googlemaps

import re

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort

from foodiebot.auth import login_required
from foodiebot.db import get_db


bp = Blueprint('restaurant', __name__, url_prefix='/restaurant')


@bp.route('/choose_restaurant', methods=('GET', 'POST'))
def user_input():
    session['IP'] = request.remote_addr
    error = None
    if session.get('result'):
        if session['result'] == None:
            error = '發生錯誤！請重新選擇地點、或是調整參數'

    if error is not None:
        flash(error)
    if request.method == 'POST':

        location_json = request.form['location']
        location = [float(s)
                    for s in re.findall(r'-?\d+.?\d*', location_json)]

        radius = request.form['radius']

        money_cheap = request.form['money_cheap']
        money_expensive = request.form['money_expensive']
        people_single = request.form['people_single']
        people_multiple = request.form['people_multiple']
        store_open = request.form['store_open']
        store_either = request.form['store_either']
        rating = float(request.form['rating'])

        search = request.form['search']

        params = {'lat': location,
                  'radius': float(radius) / 1000,
                  'money': (money_cheap, money_expensive),
                  'manypeople': (people_single, people_multiple),
                  'open': (store_open, store_either),
                  'rating': rating}

        if session.get('user_id'):
            params['user_id'] = session['user_id']
        else:
            params['user_id'] = 1

        if search != '':
            params['manual'] = search

        session['result'] = choose_restaurant(params)

        return redirect(url_for("restaurant.show_result"))

    return render_template('restaurant/user_input.html')


@bp.route('/result', methods=('GET', 'POST'))
def show_result():
    db = get_db()

    if session['result'] != None:

        if session.get('user_id'):
            filling = db.execute(
                'SELECT * FROM response'
                ' WHERE user_id = ?'
                ' AND IP = ?'
                ' AND restaurant = ?',
                (session['user_id'], session['IP'], session['result']['name'])
            ).fetchone()
            who = session['user_id']
        else:
            filling = db.execute(
                'SELECT * FROM response'
                ' WHERE restaurant = ?'
                ' AND IP = ?',
                (session['result']['name'], session['IP'])
            ).fetchone()
            who = 1
        if filling:
            filled = True
        else:
            filled = False
    else:
        return redirect(url_for('restaurant.user_input'))
    if request.method == 'POST':

        db.execute(
            'INSERT INTO response (IP, ts, user_id, category, restaurant, response) VALUES (?,CURRENT_TIMESTAMP,?, ?,?,?)',
            (session['IP'], who, session['result']['category'],
             session['result']['name'], request.form['response'])
        )
        db.commit()
        return redirect(url_for('restaurant.show_result'))

    return render_template('restaurant/show_result.html', filled=filled)


# api_key = os.getenv('GOOGLEMAP_API_KEY')
api_key = 'AIzaSyAd5FeE-Wb0Bc9r2uHPZngmVuOIi1cYJT8'
gmaps = googlemaps.Client(key=api_key)


def calculate_distance(lat, place):
    r = 6371.0

    # 所在地經緯度radian
    lat1, long1 = np.radians(lat)

    # 目的地
    long2 = np.radians(place['lng'])
    lat2 = np.radians(place['lat'])

    return round(r * arccos(cos(lat1) * cos(lat2) * cos(long1 - long2) + sin(lat1) * sin(lat2)), 2)


class user:
    def __init__(self, money, manypeople, radius, rating, user_id, lat, manual=None,
                 now_hour=datetime.now().hour, now_month=datetime.now().month, open=False):

        self.categories = None

        self.user_id = user_id

        if user_id == 1:
            BL = get_db().execute(
                'SELECT name'
                ' FROM default_black_list'
            ).fetchall()
        else:
            BL = get_db().execute(
                'SELECT name'
                ' FROM custom_black_list'
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

        self.money = money
        self.manypeople = manypeople

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

        def helper(text):
            if text == 'true':
                return 1
            return 0

        # 處理時間
        if self.now_hour in range(10, 16):
            meal = ' lunch'
        elif self.now_hour in range(16, 22):
            meal = ' dinner'
        elif self.now_hour in range(5, 10):
            meal = ' morning'
        else:
            meal = ' night'

        # 溫度食物
        if self.now_month in range(7, 11):
            # 有些東西要炎熱才會吃
            temperature = 'hot'
        elif self.now_month in range(1, 5) or self.now_month == 12:
            # 有些東西要寒冷才會吃
            temperature = 'cold'
        else:
            temperature = 'ordinary'

        if self.user_id == 1:
            fromwhere = ' FROM default_food WHERE'
        else:
            fromwhere = ' FROM custom_food_onboard WHERE user_id = ' + \
                str(self.user_id) + ' AND '

        categories = get_db().execute(
            'SELECT category'
            + fromwhere
            + meal + '= 1'
            ' AND ' + temperature + '= 1'
            ' AND ordinary = 1'
            ' AND cheap = ?'
            ' AND expensive = ?'
            ' AND singlepeople = ?'
            ' AND manypeople = ?;',
            (helper(self.money[0]), helper(self.money[1]),
             helper(self.manypeople[0]), helper(self.manypeople[1]))
        ).fetchall()

        self.categories = [cat['category'] for cat in categories]

        # 把類別打亂
        random.shuffle(self.categories)

    @retry((Exception), tries=3, delay=2, backoff=0)
    def choose_food(self):
        '''
        回傳搜尋類別以及結果
        '''

        if self.money == ('true', 'false'):
            min_price, max_price = (0, 1)
        elif self.money == ('false', 'true'):
            min_price, max_price = (1, 4)
        else:
            min_price, max_price = (0, 4)

        if self.open == ('true', 'false'):
            ifopen = True
        else:
            ifopen = False

        def search_and_check(q):
            params = {
                'query': q,
                'location': self.lat,
                'radius': self.radius * 1000,
                'language': 'zh-TW',
                'min_price': min_price,
                'max_price': max_price,
                'open_now': ifopen
            }

            def black_name(name):
                for black in self.black_list:
                    if black in name:
                        return False
                return True

            result = gmaps.places(**params)
            final_result = []

            # 過濾黑名單, 過濾評分太低
            for restaurant in result['results']:
                if (restaurant['rating'] > self.rating and
                    black_name(restaurant['name']) and
                        calculate_distance(self.lat, restaurant['geometry']['location']) < self.radius):

                    # 檢查是否夠格
                    final_result.append(restaurant)

            m = len(final_result)
            if m > 0:
                self.category = q
                self.result = final_result
                self.restaurant_information = np.random.choice(self.result)

        if self.manual is None:
            for category in self.categories[:10]:
                search_and_check(category)
                if self.category:
                    break
        else:
            search_and_check(self.manual)


def choose_restaurant(params):

    use = user(**params)

    if not use.manual:
        use.get_categories()

    use.choose_food()

    # return {
    #    'test': use.categories,
    #    'category': use.restaurant_information,

    # 'name': np.random.random(),
    # 'star': np.random.random(),
    # 'distance': np.random.random()
    # }

    if use.restaurant_information is None:
        return None

    return {
        'check': use.categories,
        'category': use.category,
        'name': use.restaurant_information['name'],
        'star': use.restaurant_information['rating'],
        'distance': calculate_distance(
            use.lat, use.restaurant_information['geometry']['location']),
    }
