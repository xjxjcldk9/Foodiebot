import functools
import numpy as np

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from foodiebot.db import get_db


bp = Blueprint('auth', __name__, url_prefix='/auth')


# 這邊需要更改


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':

        error = None

        db = get_db()
        user = db.execute(
            'SELECT * FROM user WHERE email=?',
            (request.form['stacked-email'],)
        ).fetchone()

        if user is None:
            error = '無此使用者'
        elif request.form['stacked-password'] != user['password']:
            error = '密碼錯誤'

        else:

            session.clear()
            session['user_id'] = user['id']
            session['user_name'] = user['username']

            # 一些儲存的東西
            session['result'] = []
            return redirect(url_for('restaurant.user_input'))
        flash(error)
    return render_template('auth/login.html')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        db = get_db()

        gender = request.form.get('stacked-gender')
        birthday = request.form.get('stacked-date')
        error = None

        if request.form['stacked-password'] != request.form['stacked-passwordB']:
            error = '密碼不一致'
        if error is None:

            try:
                db.execute(
                    'INSERT INTO user (username, email, password, gender, birthday) VALUES (?,?,?,?,?)',
                    (request.form['stacked-name'], request.form['stacked-email'], request.form['stacked-password'],
                     gender, birthday)
                )

                db.commit()
            except db.IntegrityError:
                error = "該 Email 已註冊過"

            else:
                user = db.execute(
                    'SELECT * FROM user WHERE email = ?', (
                        request.form['stacked-email'],)
                ).fetchone()

                default_food = db.execute(
                    'SELECT * FROM default_food'
                ).fetchall()

                # 給新註冊的用戶新增初始食物
                for food in default_food:
                    db.execute(
                        "INSERT INTO custom_food (category, singlepeople, manypeople, cheap, expensive, breakfast, lunch, dinner, night, hot, cold, user_id, activate) VALUES (?, ?,?,?,?,?,?,?,?,?,?,?,?)",
                        (food["category"], food["singlepeople"], food["manypeople"], food["cheap"], food['expensive'], food["breakfast"], food["lunch"], food["dinner"],
                            food["night"], food["hot"], food["cold"], user['id'], 1),
                    )
                    db.commit()

                default_black_list = db.execute(
                    'SELECT * FROM default_black_list'
                ).fetchall()

                # 給新註冊的用戶新增黑名單
                for black in default_black_list:
                    db.execute(
                        'INSERT INTO custom_black_list (name, user_id) VALUES (?,?)',
                        (black['name'], user['id'])
                    )
                    db.commit()

                return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
