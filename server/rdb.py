import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


# For each request, get the database.
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """
    Close the current connection with neo4j database for each request
    :param e: Unknown error parameter
    :return: None
    """
    try:
        g.pop('db', None).close()
    except AttributeError:
        return


def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as sql:
        db.executescript(sql.read().decode('UTF-8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Relational database initialized")


def register_db(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
