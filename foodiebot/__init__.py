import os

from flask import Flask
from flask import (redirect, url_for)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='c3624826cfab80f8433a7730a49441f60ad0f6891ff05b95cfbba0921cf98245',
        DATABASE=os.path.join(app.instance_path, 'foodiebot.sqlite'),
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db

    db.init_app(app)

    @app.route('/')
    def index():
        return redirect(url_for('restaurant.user_input'))

    from . import auth
    app.register_blueprint(auth.bp)

    from . import restaurant
    app.register_blueprint(restaurant.bp)

    from . import profile
    app.register_blueprint(profile.bp)

    return app
