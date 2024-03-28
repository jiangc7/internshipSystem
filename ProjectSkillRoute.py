
import functools

from flask import Blueprint, render_template, request, session, make_response, jsonify

from queries import ProjectSkillQueries

projectSkillRoute = Blueprint('ProjectSkillRoute', __name__)


@projectSkillRoute.route('/projectSkillRoute/getAll')
def get_users():
    projectSkills = ProjectSkillQueries.getAll()
    return render_template("projectSkill.html", projectSkills=projectSkills)

@projectSkillRoute.route('/project/addOrUpdateProjectSkill', methods=["post"])
def addOrUpdateProjectSkill():
    pid = request.form.get("pid")
    skills = request.form.getlist("projectskill[]")
    
    try:
        ProjectSkillQueries.deleteAll(pid)
        ProjectSkillQueries.batchInsert(pid,skills)
        data = {'message': 'ok', 'code': 'ok'}
    except:
        data = {'message': 'Something wrong, please try again later', 'code': 'ERROR'}

    return make_response(jsonify(data), 200)
