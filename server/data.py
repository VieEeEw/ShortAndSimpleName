from flask import Blueprint, make_response, request, session
from .db import get_db, get_graph_db

bp = Blueprint('data', __name__, url_prefix='/data')


@bp.route('/course/<subject>/<number>', method=['GET', 'PUT', 'PATCH', 'DELETE'])
def course_dispatch(subject, number):
    gdb = get_graph_db()
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


@bp.route('/courses', method=['GET'])
def courses():
    return get_graph_db().get_all_courses()
