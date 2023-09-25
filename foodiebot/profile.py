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
    db = get_db()

    on_board_foods = db.execute(
        'SELECT * FROM custom_food_onboard'
        ' WHERE user_id = ?',
        (session['user_id'],)
    ).fetchall()

    reserve_foods = db.execute(
        'SELECT * FROM custom_food_reserve'
        ' WHERE user_id = ?',
        (session['user_id'],)
    ).fetchall()

    foods = {
        'on_board': on_board_foods,
        'reserve': reserve_foods
    }

    return render_template('profile/manage_food.html', foods=foods)


@bp.route('/save_food', methods=('GET', 'POST'))
@login_required
def save_food():
    db = get_db()
    if request.method == 'POST':

        def helper(text):
            if text == 'false':
                return 0
            return 1
        # 先刪掉資料庫

        db.execute(
            'DELETE FROM custom_food_onboard'
            ' WHERE user_id=?',
            (session['user_id'],)
        )
        db.commit()

        db.execute(
            'DELETE FROM custom_food_reserve'
            ' WHERE user_id=?',
            (session['user_id'],)
        )
        db.commit()

        # 把新的資訊加入
        for food in request.form:
            information = request.form[food].split(',')

            if information[0] == 'on_board':
                db.execute(
                    "INSERT INTO custom_food_onboard (category,  breakfast, lunch, dinner, night,singlepeople, manypeople, cheap, expensive, ordinary, hot, cold, user_id) VALUES (?, ?,?,?,?,?,?,?,?,?,?,?,?)",
                    (food, helper(information[1]), helper(information[2]), helper(information[3]), helper(information[4]), helper(information[5]), helper(information[6]), helper(information[7]),
                     helper(information[8]), helper(information[9]), helper(information[10]), helper(information[11]), session['user_id']),
                )
                db.commit()
            else:
                db.execute(
                    "INSERT INTO custom_food_reserve (category,  breakfast, lunch, dinner, night,singlepeople, manypeople, cheap, expensive, ordinary, hot, cold, user_id) VALUES (?, ?,?,?,?,?,?,?,?,?,?,?,?)",
                    (food, helper(information[1]), helper(information[2]), helper(information[3]), helper(information[4]), helper(information[5]), helper(information[6]), helper(information[7]),
                     helper(information[8]), helper(information[9]), helper(information[10]), helper(information[11]), session['user_id']),
                )
                db.commit()

    return redirect(url_for('profile.manage_food'))


@bp.route('/black_list', methods=('GET', 'POST'))
@login_required
def black_list():
    db = get_db()

    black_list = db.execute(
        'SELECT * FROM custom_black_list'
        ' WHERE user_id = ?',
        (session['user_id'], )
    ).fetchall()

    return render_template('profile/manage_black_list.html', black_list=black_list)


@bp.route('/save_black', methods=('GET', 'POST'))
@login_required
def save_black():

    db = get_db()
    db.execute('DELETE FROM custom_black_list'
               ' WHERE user_id=?',
               (session['user_id'],))
    db.commit()

    for name in request.form['black'].split(','):
        db.execute('INSERT INTO custom_black_list (name, user_id) VALUES (?,?)',
                   (name, session['user_id']))
        db.commit()

    return redirect(url_for('profile.black_list'))
