import os

from flask import Flask
from flask import (redirect, url_for)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'foodiebot.sqlite'),
    )
    # set optional bootswatch theme
    app.config['FLASK_ADMIN_SWATCH'] = 'Superhero'

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

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
