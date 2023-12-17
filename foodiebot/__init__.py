import os

from flask import Flask
from flask import (redirect, url_for)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='c3624826cfab80f8433a7730a49441f60ad0f6891ff05b95cfbba0921cf98245'
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return redirect(url_for('restaurant.user_input'))

    from . import restaurant
    app.register_blueprint(restaurant.bp)

    return app


app = create_app()
if __name__ == '__main__':
    app.run()
