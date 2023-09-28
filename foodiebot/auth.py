import functools
import numpy as np

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from foodiebot.db import get_db

import jwt

bp = Blueprint('auth', __name__, url_prefix='/auth')


# 這邊需要更改


@bp.route('/login', methods=('GET', 'POST'))
def login():

    db = get_db()

    users = jwt.decode(request.form['credential'], options={
        "verify_signature": False})

    session['email'] = users['email']
    session['name'] = users['name']

    user = db.execute(
        'SELECT * FROM user WHERE email = ?', (users["email"],)
    ).fetchone()

    if user == None:
        return redirect(url_for('auth.user_info'))

    session.clear()
    session['user_id'] = user['id']
    session['user_name'] = user['username']

    # 一些儲存的東西
    session['result'] = []

    return redirect(url_for('restaurant.user_input'))


@bp.route('/user_info', methods=('GET', 'POST'))
def user_info():
    if request.method == 'POST':
        db = get_db()

        db.execute(
            'INSERT INTO user (username, email, gender, birthday) VALUES (?,?,?,?)',
            (session['name'], session['email'],
             request.form['stacked-gender'], request.form['stacked-date'])
        )

        db.commit()

        # 初次登陸，將default_food複製到custom_food_onboard

        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (session["email"],)
        ).fetchone()

        default_food = db.execute(
            'SELECT * FROM default_food'
        ).fetchall()

        A = default_food[:len(default_food)-10]
        B = default_food[-10:]

        for food in A:
            db.execute(
                "INSERT INTO custom_food_onboard (category, singlepeople, manypeople, cheap, expensive, breakfast, lunch, dinner, night, ordinary, hot, cold, user_id) VALUES (?, ?,?,?,?,?,?,?,?,?,?,?,?)",
                (food["category"], food["singlepeople"], food["manypeople"], food["cheap"], food['expensive'], food["breakfast"], food["lunch"], food["dinner"],
                    food["night"], food["ordinary"], food["hot"], food["cold"], user['id']),
            )
            db.commit()
        for food in B:
            db.execute(
                "INSERT INTO custom_food_reserve (category, singlepeople, manypeople, cheap, expensive, breakfast, lunch, dinner, night, ordinary, hot, cold, user_id) VALUES (?, ?,?,?,?,?,?,?,?,?,?,?,?)",
                (food["category"], food["singlepeople"], food["manypeople"], food["cheap"], food['expensive'], food["breakfast"], food["lunch"], food["dinner"],
                    food["night"], food["ordinary"], food["hot"], food["cold"], user['id']),
            )
            db.commit()

        default_black_list = db.execute(
            'SELECT * FROM default_black_list'
        ).fetchall()

        for black in default_black_list:
            db.execute(
                'INSERT INTO custom_black_list (name, user_id) VALUES (?,?)',
                (black['name'], user['id'])
            )
            db.commit()

        session.clear()
        session['user_id'] = user['id']
        session['user_name'] = user['username']

        # 一些儲存的東西
        session['result'] = []
        return redirect(url_for('restaurant.user_input'))

    return render_template('user_info.html')


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
