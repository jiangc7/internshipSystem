import datetime
import json

import pandas as pd
from flask import Blueprint, make_response, jsonify, session, render_template, request

import db
from StudentRoute import checkStudentProfileAndSurvey
from queries import StudentQueries, MentorQueries, MatchQueries, ProjectQueries, InterviewsQueries
from utils import SMTPHelper

matchRoute = Blueprint('matchRoute', __name__)


@matchRoute.route('/match/getMatch')
def getAllMatchs():
    data_two_d_array = combine_lists2D()
    return make_response(jsonify(data_two_d_array), 200)


def combine_lists2D():
    cursor = db.DBConnect()
    cursor.execute("""SELECT
                        id,
                        concat(first_name," ",last_name) as name
                        FROM student stu 
                        LEFT JOIN user u ON u.user_id = stu.id
                        where stu.placement_status !=2
                        """)
    students = cursor.fetchall()

    cursor.execute("SELECT * FROM project")
    projects = cursor.fetchall()

    matrix = [[0 for _ in range(len(projects))] for _ in range(len(students))]

    student_id_to_index = {student[0]: i for i, student in enumerate(students)}
    project_id_to_index = {project[0]: i for i, project in enumerate(projects)}

    cursor.execute("""SELECT
                        sp.project_id,
                        sp.student_id,
                        sp.will
                    FROM
                        student_project sp
                        INNER JOIN  student stu ON sp.student_id = stu.id 
                        AND (stu.placement_status !=2) 
                        """)
    student_projects = cursor.fetchall()

    for student_project in student_projects:
        project_id = student_project[0]
        student_id = student_project[1]
        will_value = student_project[2]
        student_index = student_id_to_index[student_id]
        project_index = project_id_to_index[project_id]
        matrix[student_index][project_index] = will_value

    cursor.execute("SELECT * FROM mentor_student")
    mentor_projects = cursor.fetchall()
    matchStudents = {}
    for mentor_project in mentor_projects:
        student_id = mentor_project[0]
        project_id = mentor_project[3]
        will_value = mentor_project[2]
        student_index = student_id_to_index[student_id]
        project_index = project_id_to_index[project_id]
        matrix[student_index][project_index] += will_value
        if matrix[student_index][project_index] == 4:
            if not session.__contains__('match_' + str(student_id) + "_" + str(project_id)):
                session['match_' + str(student_id) + "_" + str(project_id)] = 0
                matchStudents=aggregate_student_projects(matchStudents, student_id, project_id)
    if len(matchStudents.keys()) > 0:
        for stu_key in matchStudents.keys():
            session['_match_' + str(stu_key)] = matchStudents[stu_key]

    df = pd.DataFrame(matrix, index=[student[1] for student in students], columns=[project[1] for project in projects])
    print(df)
    # 将DataFrame转换为字典格式
    df_dict = df.to_dict(orient='split')
    result = []
    row_index = 0
    for index, row in df.iterrows():
        for j, value in enumerate(row):
            result.append([j, row_index, value])
        row_index += 1
    print(result)
    df_dict['data'] = result
    df_dict_records = df.to_dict(orient='records')
    # 将字典转换为JSON字符串
    json_str = json.dumps(df_dict)
    # 打印JSON字符串
    print(json_str)
    return json_str


def aggregate_student_projects(agg, student_id, project_id):
    if student_id in agg:
        agg[student_id].append(project_id)
    else:
        agg[student_id] = [project_id]
    return agg


@matchRoute.route('/match/processMatch')
def processMatch():
    for key, value in session.items():
        if key.find("_match_") > -1:
            stu_id = key.replace("_match_", "")
            print(stu_id)
            student = StudentQueries.getStudentById(stu_id)[0]
            mentor = MentorQueries.getMentorListinfo(value)
            mentorEmail = [men['email'] for men in mentor]
            to_student(student['email'], mentor)
            to_mentor(student, mentorEmail)

            MatchQueries.delete(stu_id,value)
            #insert into match table
            MatchQueries.insert(stu_id,value)
        data = {"message": 'ok', 'code': 'ok'}
    return make_response(jsonify(data), 200)


def to_student(stuEmail, mentorInfo):
    SMTPHelper.sentStudentMatchingNotify(stuEmail,mentorInfo)


def to_mentor(stuEmail, mentorEmail):
    SMTPHelper.sentMentorMatchingNotify(stuEmail,mentorEmail)

@matchRoute.route('/match/studentMatch')
@checkStudentProfileAndSurvey
def studentMatch():
    return render_template("student/matchproject.html")

@matchRoute.route('/match/mentorMatch')
def mentorMatch():
    return render_template("mentor/matchstudent.html")


@matchRoute.route('/match/studentMatchList')
def studentMatchList():
    stu_id = session['user_id']
    matchedProjects = MatchQueries.getStudentMatchList(stu_id)
    return make_response(jsonify(matchedProjects), 200)


@matchRoute.route('/match/mentorMatchList')
def mentorMatchList():
    matchedProjects = MatchQueries.getProjectMatchList(session['user_id'])
    return make_response(jsonify(matchedProjects), 200)


@matchRoute.route('/match/sendOffer',methods=['get'])
def sendOffer():
    stu_id = request.args.get("stu_id")
    pid = request.args.get("pid")
    intvId = request.args.get("intvId")

    # update student placement status to accept offer
    StudentQueries.update_status(stu_id,1)

    # update inter view status
    InterviewsQueries.update(intvId,4)

    # update project remain number of student
    ProjectQueries.update_num_of_stu(pid)

    data = {"message": 'ok', 'code': 'ok'}
    matchedProjects = MatchQueries.getProjectMatchList(session['user_id'])

    return make_response(jsonify(matchedProjects), 200)




