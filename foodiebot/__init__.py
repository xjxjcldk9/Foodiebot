import os

from flask import Flask, redirect, url_for


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        # TODO: key改到config.py去
        SECRET_KEY='dev'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:

        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    from . import restaurant
    app.register_blueprint(restaurant.bp)

    return app


app = create_app()
if __name__ == '__main__':
    app.run()
