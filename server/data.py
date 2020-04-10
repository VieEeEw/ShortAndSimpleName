from flask import Blueprint, make_response, request, session
from .db import get_db, get_graph_db
from flask_cors import CORS

data_bp = Blueprint('data', __name__, url_prefix='/data')
CORS(data_bp)


@data_bp.route('/course/<subject>/<number>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
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


@data_bp.route('/courses', methods=['GET'])
def courses():
    return get_graph_db().get_all_courses()
