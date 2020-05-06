from flask import Blueprint, make_response, request, session
from .rdb import get_db
from .gdb import get_graph_db
from .rdb import get_db
from .util import validate_token

data_bp = Blueprint('data', __name__, url_prefix='/data')


@data_bp.route('/course/<subject>/<number>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def course_dispatch(subject, number):
    gdb = get_graph_db()
    rdb = get_db()
    netid = request.json['net_id']
    code, msg = validate_token(rdb, netid, session['token'])
    if code != 200:
        return make_response({'error': msg}, code)
    if request.method == 'GET':
        return gdb.get_sections(subject, number)
    elif request.method == 'PUT':
        gdb.add_course(subject, number)
        return make_response({'status': 'add successful'}, 200)
    elif request.method == 'PATCH':
        gdb.change_class_num(subject, number, list(request.json.values())[0])
        return make_response({'status': 'add successful'}, 200)
    elif request.method == 'DELETE':
        gdb.delete_course(subject, number)
        return make_response({'status': 'add successful'}, 200)


@data_bp.route('/courses', methods=['GET'])
def courses():
    return get_graph_db().get_all_courses()


@data_bp.route('/intersection', methods=['GET'])
def intersection():
    return get_graph_db().get_intersection(request.json['bl1'], request.json['bl2'])
