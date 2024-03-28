import functools

from flask import Blueprint, render_template, request, session, make_response, jsonify

from enums.PlacementStatus import SubscripStatus
from queries import UsersQueries, ExternalStudentQueries, MentorQueries, StudentQueries, StudentSkillQueries, \
    InterviewsQueries, MatchQueries
from utils import MD5Helper, SMTPHelper

interviewRoute = Blueprint('interviewRoute', __name__)

@interviewRoute.route('/interview/addInterview', methods=["post"])
def resetpassword():
    stu_id = request.form.get("stu_id")
    user_id = session['user_id']
    startdate = request.form.get("startdate")
    pid = request.form.get("pid")
    starttime = request.form.get("starttime").split(' ')[0]
    location = request.form.get("location")


    InterviewsQueries.insert(user_id,pid,stu_id,startdate,starttime,location,0)
    matchedProjects = MatchQueries.getProjectMatchList(session['user_id'])
    return make_response(jsonify(matchedProjects),200)

@interviewRoute.route('/interview/delete', methods=["get"])
def delete():
    id = request.args.get("id")
    InterviewsQueries.delete(id)
    matchedProjects = MatchQueries.getProjectMatchList(session['user_id'])

    return make_response(jsonify(matchedProjects),200)


@interviewRoute.route('/interview/update', methods=["get"])
def update():
    id = request.args.get("intv_id")
    optionval = request.args.get("optionval")
    InterviewsQueries.update(id,optionval)
    matchedProjects = MatchQueries.getProjectMatchList(session['user_id'])

    return make_response(jsonify(matchedProjects),200)
