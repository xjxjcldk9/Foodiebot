import json
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from foodiebot.db import get_db
from foodiebot.auth import login_required
bp = Blueprint('profile', __name__, url_prefix='/profile')


# Can edit profile


@bp.route('/manage_food', methods=('GET', 'POST'))
@login_required
def manage_food():
    return render_template('profile/manage_food.html')


@bp.route('/get_food', methods=('GET', 'POST'))
@login_required
def get_food():
    db = get_db()
    foods_row = db.execute(
        'SELECT * FROM custom_food WHERE user_id=?',
        (g.user['id'],)
    ).fetchall()

    foods = []

    for food in foods_row:
        data = {}
        data['category'] = food['category']
        data['singlepeople'] = food['singlepeople']
        data['manypeople'] = food['manypeople']
        data['cheap'] = food['cheap']
        data['expensive'] = food['expensive']
        data['breakfast'] = food['breakfast']
        data['lunch'] = food['lunch']
        data['dinner'] = food['dinner']
        data['night'] = food['night']
        data['hot'] = food['hot']
        data['cold'] = food['cold']
        data['activate'] = food['activate']

        foods.append(data)

    return json.dumps(foods)


@bp.route('/save_food', methods=('GET', 'POST'))
@login_required
def save_food():
    db = get_db()
    # 先刪掉原本的

    db.execute(
        'DELETE FROM custom_food'
        ' WHERE user_id=?',
        (g.user['id'],)
    )
    db.commit()

    foodCards = json.loads(request.form["foodCards"])

    for foodCard in foodCards:
        db.execute(
            "INSERT INTO custom_food (category, singlepeople, manypeople, cheap, expensive, breakfast, lunch, dinner, night, hot, cold, user_id, activate) VALUES (?, ?,?,?,?,?,?,?,?,?,?,?,?)",
            (foodCard["category"], foodCard["singlepeople"], foodCard["manypeople"], foodCard["cheap"], foodCard['expensive'], foodCard["breakfast"], foodCard["lunch"], foodCard["dinner"],
             foodCard["night"], foodCard["hot"], foodCard["cold"], g.user['id'], foodCard["activate"]))
        db.commit()

    return redirect(url_for('profile.manage_food'))


@bp.route('/black_list', methods=('GET', 'POST'))
@login_required
def black_list():
    return render_template('profile/manage_black_list.html', black_list=black_list)


@bp.route('/get_black', methods=('GET', 'POST'))
@login_required
def get_black():
    db = get_db()
    blacks_row = db.execute(
        'SELECT * FROM custom_black_list WHERE user_id=?',
        (g.user['id'],)
    ).fetchall()

    blacks = []

    for black in blacks_row:
        data = {}
        data['name'] = black['name']

        blacks.append(data)

    return json.dumps(blacks)


@bp.route('/save_black', methods=('GET', 'POST'))
@login_required
def save_black():

    db = get_db()
    db.execute('DELETE FROM custom_black_list'
               ' WHERE user_id=?',
               (g.user['id'],))
    db.commit()

    blackCards = json.loads(request.form['blackCards'])

    for blackCard in blackCards:
        db.execute('INSERT INTO custom_black_list (name, user_id) VALUES (?,?)',
                   (blackCard['name'], g.user['id']))
        db.commit()

    return redirect(url_for('profile.black_list'))
