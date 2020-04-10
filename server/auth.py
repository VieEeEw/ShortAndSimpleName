from datetime import datetime

from flask import Blueprint, make_response, request
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
from flask_cors import CORS

CORS(auth_bp)


@auth_bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        netid = request.json['net_id']
        password = request.json['password']
        db = get_db()
        user = db.execute(
            'SELECT * FROM user WHERE net_id = ?', (netid,)).fetchone()
        if user is None:
            error = 'Netid not found, try register first.'
        elif not check_password_hash(user['pswd'], password):
            error = 'Incorrect username or password.'
        else:
            # If the token is invalid, generate a new token for the user
            if user['xpire_t'] < datetime.utcnow():
                db.execute("UPDATE user SET token = '[new_token]' WHERE net_id = ?",
                           (netid,))  # FIXME Change new_token to a valid new token
            return make_response({
                'status': "Login successfully"
            }, 200)
        return make_response({
            'error': error
        }, 403)


@auth_bp.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        netid = request.json['net_id']
        password = request.json['password']
        db = get_db()
        if netid is None or password is None:
            error = 'Invalid netid or password'
        elif db.execute('SELECT * FROM user WHERE net_id = ?', (netid,)).fetchone() is not None:
            error = f'Netid {netid} already registered, try login instead.'
        else:
            db.execute('INSERT INTO user(net_id, name, pswd, token) VALUES (?, ?, ?, "[new_token]")',
                       (netid, request.json['name'] if 'name' in request.json else None,
                        generate_password_hash(password)))  # FIXME Change new_token to a valid new token
            db.commit()
            return make_response({'status': "create successfully"}, 200)
        return make_response({
            'error': error
        }, 403)
