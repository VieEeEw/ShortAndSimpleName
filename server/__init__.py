from flask import Flask
import os

SECRET_KEY = 'dev'


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY=SECRET_KEY,
                            DATABASE=os.path.join(app.instance_path, 'server.sqlite')
                            )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass
    from .db import register_db
    register_db(app)

    from .auth import bp
    app.register_blueprint(bp)

    from .neo4j_interface import Neo4j_Interface
    neo4j_db = Neo4j_Interface('bolt://localhost:7687', 'neo4j', 'password')

    @app.route('/')
    def index():
        return 'Hello World!'

    @app.route('/about')
    def about():
        return "An about-us page"

    @app.route('/data/sections/<crn>')
    def neo4j_crn_data(crn):
        return neo4j_db.get_crn_data(crn)

    return app
