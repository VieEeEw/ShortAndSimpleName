from flask import Blueprint, make_response, request, session
from .db import get_db, get_graph_db

data_bp = Blueprint('data', __name__, url_prefix='/data')


@data_bp.route('/course/<subject>/<number>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def course_dispatch(subject, number):
    # FIXME check token and net_id
    gdb = get_graph_db()
    if request.method == 'GET':
        pass
    elif request.method == 'PUT':
        pass
    elif request.method == 'PATCH':
        pass
    elif request.method == 'DELETE':
        pass


@data_bp.route('/courses', methods=['GET'])
def courses():
    return get_graph_db().get_all_courses()
