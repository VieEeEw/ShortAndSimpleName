from flask import Blueprint, make_response, request, session
from .gdb import get_graph_db
from .rdb import get_db
from .util import validate_token

data_bp = Blueprint('data', __name__, url_prefix='/data')


@data_bp.route('/course/<subject>/<number>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def course_dispatch(subject, number):
    gdb = get_graph_db()
    rdb = get_db()
    netid = session['net_id']
    code, msg = validate_token(rdb, netid, session['token'])
    if code != 200:
        return make_response({'error': msg}, code)
    if request.method == 'GET':
        return gdb.get_sections(subject, number)
    elif request.method == 'PUT':
        gdb.add_course(subject, number)
        return make_response({'status': 'add successfully'}, 200)
    elif request.method == 'PATCH':
        gdb.change_class_num(subject, number, list(request.json.values())[0])
        return make_response({'status': 'change successfully'}, 200)
    elif request.method == 'DELETE':
        gdb.delete_course(subject, number)
        return make_response({'status': 'delete successfully'}, 200)


@data_bp.route('/courses', methods=['GET'])
def courses():
    return get_graph_db().get_all_courses()


@data_bp.route('/crn', methods=['GET', 'POST', 'DELETE'])
def crn():
    rdb = get_db()
    netid = session['net_id']
    code, msg = validate_token(rdb, netid, session['token'])
    if code != 200:
        return make_response({'error': msg}, code)
    if request.method == 'GET':
        return make_response({'crns': [i[0] for i in rdb.execute("SELECT `crn` FROM `user_crn` WHERE net_id=?", (netid,)).fetchall()]},
                             200)
    elif request.method == 'POST':
        ls = rdb.execute("SELECT `crn` FROM `user_crn` WHERE net_id=?", (netid,)).fetchall()
        for CRN in set(request.json['crns']):
            if CRN in ls:
                continue
            rdb.execute("INSERT INTO user_crn(net_id, crn) VALUES(?, ?)", (netid, CRN))
            rdb.commit()
        return make_response({'status': 'add successfully'}, 200)
    elif request.method == 'DELETE':
        rdb.execute("DELETE FROM user_crn WHERE net_id=?", (netid, ))
        rdb.commit()
        return make_response({'status': 'delete successfully'}, 200)


@data_bp.route('/intersection', methods=['POST'])
def intersection():
    return get_graph_db().get_intersection(request.json['bl1'], request.json['bl2'])
