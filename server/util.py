from datetime import datetime
from typing import Tuple
from werkzeug.security import check_password_hash


def validate_token(db, netid, token, check_pswd=False, password=None) -> Tuple[int, str]:
    """
    Validate the token, return whether the http status code following an error message.
    If :param check_pswd is set to True, the method will also check
    :param db: The sqlite3 relational database, assume db is valid.
    :param netid: Net ID whose token will be validated, can be None.
    :param token: The token stored in session, can be None.
    :param check_pswd: A flag, if set True it will check password given
    :param password: Must be given if check_pswd is set True
    :return: http status code and an error message
    """
    if check_pswd and password is None:
        return 403, "Invalid password"
    if netid is None:
        return 403, "Invalid login status, try login again"
    if token is None:
        return 401, "Token required"
    meta = db.execute("SELECT token, xpire_t, pswd FROM user WHERE net_id=?", (netid,)).fetchone()
    if meta is None:
        return 403, 'Cannot find current user'
    s_token, e_time, pswd_hash = meta
    if s_token is None or e_time < datetime.utcnow():
        return 401, 'Token expired.'
    elif s_token != token:
        return 401, 'Invalid token.'
    if check_pswd and not check_password_hash(pswd_hash, password):
        return 403, "Net ID or password incorrect."
    return 200, "No error"
