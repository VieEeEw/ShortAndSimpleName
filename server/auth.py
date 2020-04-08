from flask import Blueprint, redirect, make_response, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from dateutil.parser import isoparse
from datetime import datetime

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
            # If the token is invalid, generate a new token for the user
            if isoparse(user['xpire_t']) < datetime.utcnow():
                db.execute("UPDATE user SET token = '[new_token]' WHERE net_id = ?",
                           (netid,))  # FIXME Change new_token to a valid new token
            return make_response({
                'status': "Login successfully"
            }, 200)
        return make_response({
            'error': error
        }, 403)


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
            db.execute('INSERT INTO user(net_id, name, pswd, token) VALUES (?, ?, ?, "[new_token]")',
                       (netid, request.form['name'] if 'name' in request.form else None,
                        generate_password_hash(password)))  # FIXME Change new_token to a valid new token
            db.commit()
            return make_response({'status': "create successfully"}, 200)
        return make_response({
            'error': error
        }, 403)
