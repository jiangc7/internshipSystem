from flask import Blueprint, session, make_response, request
from flask import jsonify

from queries import NetworkInterviewQueries

speedInterviewRoute = Blueprint('speedInterviewRoute', __name__)


@speedInterviewRoute.route('/speed/getOneByIdAndType')
def get_one():
    user_id = session['user_id']
    role = session['role']
    participant = NetworkInterviewQueries.getOneByIDAndType(user_id, role)

    if len(participant) <= 0:
        latest_event = NetworkInterviewQueries.get_event()[0]
        data = {'message': 'no participate', 'code': 'ERROR',"event" :latest_event}
    else:
        data = {'message': 'participate', 'code': 'ok'}

    return make_response(jsonify(data), 200)


@speedInterviewRoute.route('/speed/add', methods=['get'])
def add():
    user_id = session['user_id']
    role = session['role']
    event_id = request.args.get("event_id")
    participant = NetworkInterviewQueries.insert(user_id, role,event_id)

    return make_response(jsonify(participant), 200)


@speedInterviewRoute.route('/speed/addEvent', methods=['post'])
def addEvent():
    location = request.form.get("location")
    decs = request.form.get("desc")
    starttime = request.form.get("starttime").split(' ')[0]
    startdate = request.form.get("startdate")

    participant = NetworkInterviewQueries.insert_event(startdate, starttime, location, session['user_id'], decs)

    return make_response(jsonify(participant), 200)


@speedInterviewRoute.route('/speed/getEvent')
def get_event():
    participant = NetworkInterviewQueries.get_event()

    return make_response(jsonify(participant[0]), 200)
