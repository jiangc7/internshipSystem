from flask import Blueprint, render_template, request, session, redirect, jsonify, make_response, json

from queries import UsersQueries, MentorQueries, ProjectQueries, CompanyQueries, StudentQueries
from utils import MD5Helper,SMTPHelper


mentorRoute = Blueprint('mentorRoute', __name__)


@mentorRoute.route('/mentor/getAll')
def getAll():
    mentors = MentorQueries.getAll()
    return render_template("mentors.html", mentors=mentors)

@mentorRoute.route('/mentor/getAllJson')
def getAllJson():
    mentors = MentorQueries.getAll()
    return make_response(jsonify(mentors), 200)

@mentorRoute.route('/mentor/delete/<id>')
def delete(id):
    deleteId = UsersQueries.delete(id)
    return render_template("users.html")

@mentorRoute.route('/mentor/deleteJson/<id>')
def deleteJson(id):
    projects =ProjectQueries.getProjectAll(None,None,id)
    if len(projects)>0:
        data = {"message": "Mentor deleted failed as their projects need to be deleted first! ", "code": "error"}
        return make_response(jsonify(data), 200)

    deleteId = UsersQueries.delete(id)
    mentors = MentorQueries.getAll()
    return make_response(jsonify(mentors), 200)


@mentorRoute.route('/mentor/addOrUpdate')
def addOrUpdate():
    mentorId = request.form.get("mentorId")
    phone = request.form.get("phone")
    summary = request.form.get("summary")
    id = MentorQueries.insert(mentorId, phone, summary)
    if id >0:
        return render_template("mentors.html")
    #  MentorQueries.update(mentorId, phone, summary)

    return render_template("mentors.html",errorMsg="add mentors wrong")

@mentorRoute.route('/mentor/project')
def mentorproject():
    role = session['role']
    if role == 1:
        mentor=MentorQueries.getMentorinfo(session['user_id'])
        projects = ProjectQueries.getProjectAll(None,mentor[0]['company_id'],session['user_id'])
    else:
        projects = ProjectQueries.getProjectAll(None,None,None)
    return render_template("mentor/project.html", projects=projects)

@mentorRoute.route('/mentor/profile')
def mentorprofile():
    id = session['user_id']
    profile = MentorQueries.getMentorinfo(id)
    return render_template("mentor/mentorprofile.html", profile=profile)

@mentorRoute.route('/mentor/getMentorData')
def getMentorData():
    id = request.args.get("mId")
    profile = MentorQueries.getMentorinfo(id)
    return make_response(jsonify(profile[0]), 200)

@mentorRoute.route('/mentor/updateprofile')
def mentorupdateprofile():
    id = session['user_id']
    profile = MentorQueries.getMentorinfo(id)
    return render_template("mentor/mentorUpdateprofile.html", profile=profile)

@mentorRoute.route('/mentor/Update',methods=["POST"])
def Update():
    id = request.form.get("mentorid")
    first_name = request.form.get("firstname")
    last_name = request.form.get("lastname")
    # password = request.form.get("password")
    email = request.form.get("email")
    phone = request.form.get("phone")
    summary = request.form.get("summary")
    UsersQueries.updateprofile(id, first_name, last_name, email)
    MentorQueries.update(id, phone, summary)

    profile = MentorQueries.getMentorinfo(id)
    return render_template("mentor/mentorprofile.html", profile=profile)


@mentorRoute.route('/mentor/UpdateJson',methods=["POST"])
def UpdateJson():
    id = request.form.get("mentorid")
    first_name = request.form.get("firstname")
    last_name = request.form.get("lastname")
    # password = request.form.get("password")
    email = request.form.get("email")
    phone = request.form.get("phone")
    summary = request.form.get("summary")
    UsersQueries.updateprofile(id, first_name, last_name, email)
    MentorQueries.update(id, phone, summary)
    profile = MentorQueries.getMentorinfo(id)
    mentors = MentorQueries.getAll()
    return make_response(jsonify(mentors), 200)

@mentorRoute.route('/mentor/getProjectAllJson')
def getProjectAllJson():
    role = session['role']
    if role == 1:
        mentor = MentorQueries.getMentorinfo(session['user_id'])
        projects = ProjectQueries.getProjectAll(None, mentor[0]['company_id'],session['user_id'])
    else:
        projects = ProjectQueries.getProjectAll(None, None,None)
    return make_response(jsonify(projects), 200)



@mentorRoute.route('/companyprofile')
def companyprofile():
    userid = session['user_id']
    company = CompanyQueries.getcompany(userid)
    print(company)
    return render_template("mentor/companyprofile.html", company=company)


@mentorRoute.route('/updatecompanyprofile',methods=['POST'])
def updatecompanyprofile():
    companyid = request.form.get("companyid")
    company_name = request.form.get("company_name")
    region = request.form.get("region")
    city = request.form.get("city")
    street = request.form.get("street")
    website = request.form.get("website")
    updateid = MentorQueries.updatecompany(company_name, region,city,street,website,companyid)
    if updateid >0:
        return redirect("/companyprofile")

    return redirect("/companyprofile",errorMsg="add mentors wrong")

@mentorRoute.route('/mentor/prestudent')
def prestudent():
    return render_template("/mentor/preferredStu.html")



@mentorRoute.route('/studentMentor/add',methods=["POST"])
def addPreferStudent():
    stuList = request.form.get("sidList")
    stuList2= json.loads(stuList)
    sidArr = [str(student['sid']) for student in stuList2]

    updateSids = MentorQueries.getAllByStudentIdAndProjectId(sidArr,session['user_id'])
    values = [str(value) for d in updateSids for value in d.values()]

    if len(updateSids) >0:
        MentorQueries.deleteByStudentIds(session['user_id'],values)

    MentorQueries.batchInsert(session['user_id'], stuList2)

    data = {"message": "ok", "code": "ok"}
    return make_response(jsonify(data), 200)


@mentorRoute.route('/contactstaff')
def contactstaff():
    return render_template("/mentor/contactstaff.html")

@mentorRoute.route('/contactstaffsend', methods=['POST'])
def contactstaffmail():
    mentor=MentorQueries.getMentorinfo(session['user_id'])
    subject = request.form.get("subject")
    body = request.form.get("body")
    SMTPHelper.sendEmail(subject,body,mentor[0]['email'])
    MSG = 'Thank you! Email has been sent!'
    return render_template("/mentor/contactstaff.html", MSG=MSG)


@mentorRoute.route('/studentMentor/remove',methods=["POST"])
def removePreStudent():
    sid = request.form.get("sid")
    MentorQueries.deleteByStudentIds(session['user_id'],sid)

    userId = session['user_id']
    user = StudentQueries.getPreferredStudent(userId)


    return make_response(jsonify(user), 200)

