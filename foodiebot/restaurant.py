from numpy import sin, cos, arccos
import random
from retry import retry
from datetime import datetime
import os
import numpy as np
import googlemaps

import re
import json

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
    session['IP'] = request.remote_addr
    error = None
    if request.method == 'POST':
        parameters = json.loads(request.form['parameters'])
        categories, black_list = get_categories_BL(parameters)

        if parameters['manual'] != '':
            categories = [parameters['manual']]
        category, result = get_restaurant(
            categories, black_list, parameters)

        if result is None:
            error = '查無結果 請調整參數或更改位置'
        else:
            session['category'] = category
            session['result'] = result
            return redirect(url_for('restaurant.show_result'))

    if error is not None:
        flash(error)

    return render_template('restaurant/user_input.html')


@bp.route('/show_result', methods=('GET', 'POST'))
def show_result():
    # 先檢查是否已填過表單
    # 是否登入
    if not session.get('user_id'):
        who = 1
    else:
        who = session['user_id']

    db = get_db()
    filled = db.execute(
        'SELECT * FROM response'
        ' WHERE IP = ? AND user_id = ? AND restaurant = ?',
        (session['IP'], who, session['result']['name'])
    ).fetchone()

    if request.method == 'POST':
        db.execute(
            'INSERT INTO response (IP, ts, user_id, category, restaurant, response) VALUES (?,CURRENT_TIMESTAMP,?,?,?,?)',
            (session['IP'], who, session['category'],
             session['result']['name'], request.form['response'])
        )
        db.commit()
        return redirect(url_for('restaurant.show_result'))

    return render_template('restaurant/show_result.html', filled=filled)


def get_categories_BL(parameters):

    now_hour = datetime.now().hour
    now_month = datetime.now().month

    # 處理時間
    if now_hour in range(10, 16):
        meal = ' AND lunch=1'
    elif now_hour in range(16, 22):
        meal = ' AND dinner=1'
    elif now_hour in range(5, 10):
        meal = ' AND morning=1'
    else:
        meal = ' AND night=1'

    # 季節
    if now_month in range(7, 11):
        # 有些東西要炎熱才會吃
        season = ' AND hot=1'
    elif now_month in range(1, 5) or now_month == 12:
        # 有些東西要寒冷才會吃
        season = ' AND cold=1'
    else:
        season = ''

    # 是否登入
    if not session.get('user_id'):
        who = 1
    else:
        who = session['user_id']

    db = get_db()
    categories_row = db.execute(
        ' SELECT category FROM custom_food'
        ' WHERE user_id = ?'
        ' AND singlepeople = ?'
        ' AND manypeople = ?'
        ' AND cheap = ?'
        ' AND expensive = ?'
        + meal
        + season
        + ' AND activate = 1',
        (who, parameters['singlepeople'], parameters['manypeople'],
         parameters['cheap'], parameters['expensive'])
    ).fetchall()

    categories = [category_row['category'] for category_row in categories_row]
    random.shuffle(categories)

    black_list_row = db.execute(
        ' SELECT name FROM custom_black_list'
        ' WHERE user_id = ?',
        (who, )
    )
    black_list = [black['name'] for black in black_list_row]

    return categories, black_list


@retry((Exception), tries=3, delay=2, backoff=0)
def get_restaurant(categories, black_list, parameters):

    if parameters['cheap'] == 1 & parameters['expensive'] == 0:
        min_price = 0
        max_price = 1
    elif parameters['cheap'] == 0 & parameters['expensive'] == 1:
        min_price = 2
        max_price = 4
    else:
        min_price = 0
        max_price = 4

    final_result = []
    for category in categories:
        results = gmaps.places(query=category,
                               location=parameters['location'],
                               radius=parameters['radius'] * 1000,
                               language='zh-TW',
                               min_price=min_price,
                               max_price=max_price,
                               open_now=parameters['open'])

        # 過濾黑名單, 過濾評分太低, 距離
        for restaurant in results['results']:
            if (restaurant['rating'] >= parameters['star'] and
                check_black(restaurant['name'], black_list) and
                    calculate_distance(parameters['location'], restaurant['geometry']['location']) <= parameters['radius']):

                final_result.append(restaurant)

        if len(final_result) >= 1:
            return category, np.random.choice(final_result)
    return None, None


def check_black(name, black_list):
    for black in black_list:
        if black in name:
            return False
    return True


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
