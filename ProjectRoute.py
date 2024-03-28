
import functools

from flask import Blueprint, render_template, request, session, make_response, jsonify

from queries import ProjectQueries, ProjectSkillQueries


projectRoute = Blueprint('projectRoute', __name__)


@projectRoute.route('/project/getAll')
def get_users():
    projects = ProjectQueries.getAll()
    return render_template("project.html", projects=projects)



@projectRoute.route('/project/getProjectByIds')
def getProjectByIds():
    idarr = request.args.get("idArr")
    print(idarr)
    projects = ProjectQueries.getProjectAll(idarr,None,None)
    data ={"message":'ok','code':'ok','data':projects}
    return make_response(jsonify(data), 200)

@projectRoute.route('/project/getProjectsByCompanyId')
def getProjectsByCompany():
    comId = request.args.get("comId")
    print(comId)
    projects = ProjectQueries.getProjectByCoampny(comId)
    data ={"message":'ok','code':'ok','data':projects}
    return make_response(jsonify(data), 200)

@projectRoute.route('/project/getAlltypeJson')
def getAlltypeJson():
    types = ProjectQueries.getAlltype()
    return make_response(jsonify(types), 200)

@projectRoute.route('/Project/addOrUpdate', methods=["post"])
def addOrUpdateProject():
    id = request.form.get("pid")
    project_title = request.form.get("project_title")
    userId = request.form.get("user_id")
    description = request.form.get("description")
    Number_of_student = request.form.get("Number_of_student")

    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    projecttype = request.form.get("projecttype")
    remain_number_of_student = request.form.get("remain_number_of_student")

    try:
        
            userid = session['user_id']
            if(id):
                result = ProjectQueries.update(id, project_title, description, Number_of_student, projecttype, start_date, end_date,remain_number_of_student)
                data = {'message': 'Profile has been updated successfully', 'code': 'ok'}               
            else:
                result = ProjectQueries.insert(project_title, description, Number_of_student, projecttype, start_date, end_date, Number_of_student,userid)
                data = {'message': 'Profile has been added successfully', 'code': 'ok'}
               
            print(result)
            
    except:
            data = {'message': 'Something wrong, please try again later', 'code': 'ERROR'}

    return make_response(jsonify(data), 200)

@projectRoute.route('/Project/updateProject')
def updateProject():
    id = session['user_id']
    profile = ProjectQueries.getProjectinfo(id)
    return render_template("mentor/mentorUpdateprofile.html", profile=profile)

@projectRoute.route('/project/getAllprofileAndtypeJson')
def getAllprofileAndtypeJson():

    types = ProjectQueries.getAlltype()
    idarr = request.args.get("pid")
    print(idarr)
    projects = ProjectQueries.getProjectAll(idarr,None,None)
    data ={"message":'ok','code':'ok','projects':projects,'types':types}

    return make_response(jsonify(data), 200)



@projectRoute.route('/project/getAllskillJson')
def getAllskillJson():
    pid = request.args.get("pid")
    skills = ProjectSkillQueries.getAllByProjectId(pid)
    data ={"message":'ok','code':'ok','skills':skills}
    return make_response(jsonify(data), 200)