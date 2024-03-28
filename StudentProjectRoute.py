import json

from flask import Blueprint, render_template, request, session, make_response, jsonify

from StudentRoute import checkStudentProfileAndSurvey
from queries import StudentProjectQueries

studentProjectRoute = Blueprint('StudentProjectRoute', __name__)


@studentProjectRoute.route('/studentProject/getAll')
def getAll():
    stuProjects = StudentProjectQueries.getAll()
    return render_template("studentProject.html", stuProjects=stuProjects)


@studentProjectRoute.route('/studentProject/add',methods=["POST"])
def addPreferProject():
    pidList1 = request.form.get("pidList")
    pidList2= json.loads(pidList1)
    pidArr = [str(project['pid']) for project in pidList2]

    updatePids = StudentProjectQueries.getAllByStudentIdAndProjectId(session['user_id'], pidArr)
    values = [str(value) for d in updatePids for value in d.values()]
    if len(updatePids) >0:
        StudentProjectQueries.delete(session['user_id'],values)

    StudentProjectQueries.batchInsert(session['user_id'], pidList2)

    data = {"message": "ok", "code": "ok"}
    return make_response(jsonify(data), 200)

@studentProjectRoute.route('/studentProject/preferProject')
@checkStudentProfileAndSurvey
def preferProject():
    return render_template("studentProject.html")


@studentProjectRoute.route('/studentProject/getPreferredProject')
def getPreferredProject():
    projects = StudentProjectQueries.preferredProject(session['user_id'])
    return make_response(jsonify(projects), 200)

@studentProjectRoute.route('/studentProject/remove',methods=['get'])
def remove():
    pid=request.args.get("pid")
    StudentProjectQueries.delete(session['user_id'],pid)
    projects = StudentProjectQueries.preferredProject(session['user_id'])
    return make_response(jsonify(projects), 200)



def remove_elements(a, b):
    a[:] = [int(item) for item in a if int(item) not in b]
    return a;
