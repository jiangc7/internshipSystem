from flask import Blueprint, render_template

from queries import StudentQueries, StudentSkillQueries

studentSkillRoute = Blueprint('StudentSkillRoute', __name__)


@studentSkillRoute.route('/studentSkillRoute/getAll')
def get_users():
    studentSkills = StudentSkillQueries.getAll()
    return render_template("stuSkill.html", studentSkills=studentSkills)
