import functools
from flask import Blueprint, flash, g, redirect, make_response, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        netid = request.form['net_id']
        password = request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM user WHERE net_id = ?', (netid,)).fetchone()
        if user is None:
            error = 'Netid not found, try register first.'
        elif not check_password_hash(user['pswd'], password):
            error = 'Incorrect username or password.'
        else:
            session.clear()
            session['netid'] = netid
            return redirect(url_for('index'))
        return make_response({
            'data': None,
            'error': error
        }, 403)
    elif request.method == 'GET':
        # TODO return a template of login page with render_template
        return redirect(url_for('index'))


@bp.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        netid = request.form['net_id']
        password = request.form['password']
        db = get_db()
        if netid is None or password is None:
            error = 'Invalid netid or password'
        elif db.execute('SELECT * FROM user WHERE net_id = ?', (netid,)).fetchone() is not None:
            error = f'Netid {netid} already registered, try login instead.'
        else:
            db.execute('INSERT INTO user(net_id, name, pswd) VALUES (?, ?, ?)',
                       (netid, request.form['name'] if 'name' in request.form else None, generate_password_hash(password)))
            db.commit()
            return redirect(url_for('index'))
        return make_response({
            'data': None,
            'error': error
        }, 403)
