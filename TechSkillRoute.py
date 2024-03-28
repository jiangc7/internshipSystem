from flask import Blueprint, render_template
from flask import jsonify

from queries import UsersQueries, TechSkillQueries

techSkillRoute = Blueprint('techSkillRoute', __name__)


@techSkillRoute.route('/techSkill/getAll')
def get_users():
    skills = TechSkillQueries.getAll()
    return render_template("skills.html", skills=skills)
