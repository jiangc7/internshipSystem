import json

from flask import Blueprint, render_template, session

from queries import QuestionQueries, StudentSkillQueries, TechSkillQueries

questionRoute = Blueprint('questionRoute', __name__)


@questionRoute.route('/questionRoute/getAll')
def get_users():
    studentId = session['user_id']
    questions = QuestionQueries.getAll(studentId)
    studentSkills = StudentSkillQueries.getAllByStudentId(studentId)
    for que in questions:
        str = que['question'].replace('\r', '').replace('\n', '')
        strjson = json.loads(str)
        que['question']=strjson

    return render_template("question.html", questions=questions,skills=studentSkills)
