from datetime import datetime

from flask import Blueprint, make_response, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from hashlib import md5

from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        netid = request.json['net_id']
        password = request.json['password']
        db = get_db()
        user = db.execute('SELECT * FROM user WHERE net_id = ?', (netid,)).fetchone()
        if user is None:
            error = 'Netid not found, try register first.'
        elif not check_password_hash(user['pswd'], password):
            error = 'Incorrect username or password.'
        else:
            # If the token is invalid, generate a new token for the user
            if user['xpire_t'] < datetime.utcnow():
                new_token = md5(f"{password}{datetime.utcnow()}".encode()).hexdigest()
                db.execute("UPDATE user SET token = ? WHERE net_id = ?",
                           (new_token, netid))
                session['token'] = new_token
            return make_response({
                'status': "Login successfully"
            }, 200)
        return make_response({
            'error': error
        }, 403)


@bp.route('/register', methods=['POST'])
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
            new_token = md5(f"{password}{datetime.utcnow()}".encode()).hexdigest()
            db.execute('INSERT INTO user(net_id, name, pswd, token) VALUES (?, ?, ?, ?)',
                       (netid, request.json['name'] if 'name' in request.json else None,
                        generate_password_hash(password)), new_token)
            db.commit()
            return make_response({'status': "create successfully"}, 200)
        return make_response({
            'error': error
        }, 403)


@bp.route('/delete', method=['POST'])
def delete():
    netid = request.json['net_id']
    db = get_db()
    token, e_time = db.execute("SELECT token, xpire_t FROM user WHERE net_id=?", (netid,)).fetchone()
    if token is None or e_time > datetime.utcnow():
        error = 'Token expired.'
    elif token != session['token']:
        error = 'Invalid token.'
    else:
        db.execute("DELETE FROM user WHERE net_id=?", (netid,))
        db.commit()
        session.pop('token')
        return make_response({'status': "delete successfully"}, 200)
    return make_response({
        'error': error
    }, 403)
