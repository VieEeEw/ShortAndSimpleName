from flask import Flask
import os

SECRET_KEY = 'dev'


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY=SECRET_KEY,
                            DATABASE=os.path.join(
                                app.instance_path, 'server.sqlite')
                            )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass
    from .db import register_db, register_graph_db
    register_db(app)
    register_graph_db(app)

    from .auth import auth_bp
    from flask_cors import CORS
    CORS(auth_bp)
    app.register_blueprint(auth_bp)

    @app.route('/')
    def index():
        return 'Success!'

    return app
