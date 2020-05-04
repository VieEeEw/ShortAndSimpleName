from flask import Flask, make_response
import os

SECRET_KEY = 'dev'


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY=SECRET_KEY,
                            DATABASE=os.path.join(
                                app.instance_path, 'server.sqlite'),
                            )

    from . import config
    app.config.from_object(config)
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        # If test_config is given
        app.config.from_mapping(test_config)
    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass
    # Add test command
    from .test_server import test_server_command
    app.cli.add_command(test_server_command)

    from .rdb import register_db
    from .gdb import register_graph_db
    register_db(app)
    register_graph_db(app)

    from .bp_auth import auth_bp
    from flask_cors import CORS
    CORS(auth_bp, supports_credentials=True, origin=["app.dev.localhost:8080"])
    app.register_blueprint(auth_bp)

    @app.route('/')
    def index():
        return 'Success!'

    # A test end point.
    @app.route('/check-config/<config_name>')
    def test(config_name):
        resp = make_response({"data": str(app.config[config_name])}, 200)
        resp.set_cookie("Cookie", value='cookie')
        return resp

    return app
