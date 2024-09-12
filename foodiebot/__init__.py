import os

from flask import Flask, redirect, url_for


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # instance folder裡面裝db檔案或是key的檔案，不會push上去的東西
    # instance folder在app資料夾之外

    # 設定一些app會用的數值
    app.config.from_mapping(
        # TODO: key改到config.py去
        SECRET_KEY='dev'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        # 會override前面設定的東西，適合用在production時放秘密
        # 開silent這樣找不到檔案不會叫
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        # 在測試的時候也可以pass in 自己specify的config
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    @app.route('/')
    def index():
        return redirect(url_for('restaurant.user_input'))

    from . import restaurant
    app.register_blueprint(restaurant.bp)

    return app


app = create_app()
if __name__ == '__main__':
    app.run()
