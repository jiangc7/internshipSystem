from flask import Blueprint, render_template

from queries import ProjectQueries, ProjectTypeQueries

projectTypeRoute = Blueprint('projectTypeRoute', __name__)


@projectTypeRoute.route('/projectTypeRoute/getAll')
def get_users():
    projectType = ProjectTypeQueries.getAll()
    return render_template("projectType.html", projectType=projectType)
