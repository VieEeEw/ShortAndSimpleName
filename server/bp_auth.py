from datetime import datetime

from flask import Blueprint, make_response, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from hashlib import md5

from .rdb import get_db
from .util import validate_token

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# 401: Unauthorized for expired and invalid token
# 403: Forbidden

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
            token = md5(f"{password}{datetime.utcnow()}".encode()).hexdigest()
            db.execute("UPDATE user SET token = ? WHERE net_id = ?",
                       (token, netid))
            session['token'] = token
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
            new_token = md5(f"{password}{datetime.utcnow()}".encode()).hexdigest()
            db.execute('INSERT INTO user(net_id, `name`, pswd, token) VALUES (?, ?, ?, ?)',
                       (netid, request.json['name'] if 'name' in request.json else None,
                        generate_password_hash(password), new_token))
            db.commit()
            session['token'] = new_token
            return make_response({'status': "create successfully"}, 200)
        return make_response({
            'error': error
        }, 403)


@auth_bp.route('/delete', methods=['POST'])
def delete():
    netid = session['net_id']
    if netid is None:
        return make_response({'error': 'Invalid login status, try login again'}, 403)
    db = get_db()
    code, error = validate_token(db, netid, session['token'])
    if code != 200:
        return make_response({
            'error': error
        }, code)
    db.execute("DELETE FROM user WHERE net_id=?", (netid,))
    db.commit()
    session.pop('token')
    return make_response({'status': "delete successfully"}, 200)


@auth_bp.route('/update-pswd', methods=['POST'])
def update_pswd():
    netid = session['net_id']
    pswd = request.json['password']
    new_pswd = request.json['new_password']
    if netid is None:
        return make_response({'error': 'Invalid login status, try login again'}, 403)
    db = get_db()
    code, error = validate_token(db, netid, session['token'], check_pswd=True, password=pswd)
    if code != 200:
        return make_response({
            'error': error
        }, code)
    db.execute("UPDATE FROM user SET pswd=? WHERE net_id=?", (generate_password_hash(new_pswd), netid))
    db.commit()
    return make_response({'status': "delete successfully"}, 200)
