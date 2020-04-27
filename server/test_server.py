import click
from flask.cli import with_appcontext
from flask import current_app
import os
from .gdb import Neo4jInterface


@click.command('test-server')
@with_appcontext
def test_server_command():
    # Check relational database existence
    if not os.path.exists(current_app.config['DATABASE']):
        click.echo("Instance folder does not exist, run flask init-db first")
        return
    # Check neo4j auth
    try:
        Neo4jInterface(current_app.config['GRAPH_DB']['url'], current_app.config['GRAPH_DB']['username'],
                       current_app.config['GRAPH_DB']['pswd']).close()
    except Exception as e:
        click.echo(f"Incorrect username/password/url for neo4j database, got an error of type {type(e)}")
        return
    click.echo("All pre-test passed, you can run the server now")
