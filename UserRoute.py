import functools
import json

from flask import Blueprint, render_template, request, session, make_response, jsonify, url_for

from enums.PlacementStatus import SubscripStatus
from queries import UsersQueries, ExternalStudentQueries, MentorQueries, StudentQueries, StudentSkillQueries, \
    QuestionQueries
from utils import MD5Helper, SMTPHelper

userRoute = Blueprint('userRoute', __name__)


def login_require(func):

    @functools.wraps(func)
    def login_wrapper(*args, **kwargs):
        userId = session.__contains__('user_id')
        if not userId:
            return render_template("error.html", data='you have to login first!')
        else:
            print('start request')
            res = func(*args, **kwargs)
            return res

    return login_wrapper


@userRoute.route('/users/getAll')
@login_require
def get_users():
    users = UsersQueries.getAll()
    return render_template("users.html", users=users)


@userRoute.route('/users/delete/<id>')
def deleteUser(id):
    deleteId = UsersQueries.delete(id)
    return render_template("users.html")


@userRoute.route('/users/checkEmail')
def checkEmail():
    email = request.args.get("email")
    user = UsersQueries.getUserByEmail(email)
    if len(user) > 0:  # if found a row return ok , if nothing found return error
        data = {"message": "ok", "code": "ok"}
    else:
        data = {"message": "user email doesn't exist", "code": "error"}
    return make_response(jsonify(data), 200)


@userRoute.route('/users/sendPasswordEmail')
def sendPasswordEmail():
    email = request.args.get("email")
    try:
        SMTPHelper.sentPasswordEmail(email)
        data = {"message": "ok", "code": "ok"}
    except:
        data = {"message": "sending email failed", "code": "error"}
    return make_response(jsonify(data), 200)


@userRoute.route('/users/changePassword', methods=["post"])
def changePassword():
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = UsersQueries.getUserByEmail(email)
        if len(user) > 0:
            encryped = MD5Helper.md5_encrypt(password)
            UsersQueries.changePassword(user[0]['user_id'], encryped)
            data = {"message": "ok", "code": "ok"}
        else:
            data = {"message": "email doesn't exist", "code": "error"}

    except:
        data = {"message": "sending email failed", "code": "error"}
    return make_response(jsonify(data), 200)


@userRoute.route('/users/addOrUpdate', methods=["post"])
def addOrUpdateUser():
    firstname = request.form.get("firstname")
    userId = request.form.get("user_id")
    lastname = request.form.get("lastname")
    email = request.form.get("email")

    phone = request.form.get("phone")
    role = request.form.get("role")

    try:
        if not userId:
            password = request.form.get("password")
            encrypted = MD5Helper.md5_encrypt(password);

            id = UsersQueries.insert(firstname, lastname, encrypted, email, role)
            if id > 0:
                # check the role to see which sub table we need to insert
                match role:  # render different page by role
                    case "1":
                        # Mentor
                        cid = request.form.get("menCompany")
                        MentorQueries.insert(id, phone, "", cid)
                    case "2":
                        # Student
                        dob = request.form.get("dob")
                        gender = request.form.get("gender")
                        studentNo = request.form.get("studentNo")
                        alternativeName = request.form.get("alternativeName")
                        preferName = request.form.get("preferName")
                        # id,student_id_no, alternative_name, preferred_name, phone, cv, project_preference, personal_statements, placement_status,dob
                        StudentQueries.insert(id, studentNo, alternativeName, preferName, phone, "", "", "",
                                              SubscripStatus.not_available.value, gender,
                                              dob)
                data = {'message': 'Profile has been added successfully', 'code': 'ok'}
            else:
                data = {'message': 'You have successfully registered', 'code': 'ok'}

        else:
            rowCount = UsersQueries.update(userId, firstname, lastname)
            session['name'] = firstname + " " + lastname
            alternative_name = request.form.get("alternativeName")
            preferred_name = request.form.get("preferName")
            skills = request.form.getlist("stu_skills[]")
            dob = request.form.get("dob")
            project_preference = request.form.get("project_preference") if request.form.get("project_preference") is not None else ''
            personal_statements = request.form.get("personal_statement") if request.form.get("personal_statement") is not None else ''
            cv = request.form.get("fileLocation") if request.form.get("fileLocation") is not None else ''
            rowCountStu = StudentQueries.update(userId,alternative_name, preferred_name, phone, cv, project_preference, personal_statements,dob)
            print(rowCountStu)
            StudentSkillQueries.deleteAll(userId)
            StudentSkillQueries.batchInsert(userId,skills)
        data = {'message': 'Profile has been updated successfully', 'code': 'ok'}
    except:
        data = {'message': 'Something wrong, please try again later', 'code': 'ERROR'}

    return make_response(jsonify(data), 200)


@userRoute.route('/users/checkStudentExsit', methods=["post"])
def checkStudentExsit():
    if request.form.get("user_id"):
        data = {'message': 'ok', 'code': 'ok'}
        return make_response(jsonify(data), 200)
    else:
        studentNo = request.form.get("studentNo")
        studentData = ExternalStudentQueries.getOneByStudentNo(studentNo)
        if len(studentData) > 0:
            if studentData[0]['ifCurrentlyEnrolled'] == '1':
                studentRegiData = StudentQueries.getStudentByStudentNo(studentNo)
                if len(studentRegiData) == 0:
                    data = {'message': 'ok', 'code': 'ok'}
                else:
                    data = {'message': 'student is already registered', 'code': 'ERROR'}
            else:
                data = {'message': 'student is not enrolled', 'code': 'ERROR'}
        else:
            data = {'message': 'student no doesn\'t  exist', 'code': 'ERROR'}
    return make_response(jsonify(data), 200)


# user login, email and role need to be passed, to match the database stored data.
@userRoute.route("/users/login", methods=["post"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    userData = UsersQueries.getUserByEmail(email)  # check if the email and role is matched
    if len(userData) > 0:
        print(userData)
        data = userData[0]
        checkResult = MD5Helper.check_match(data['password'], password)
        if not checkResult:
            return render_template("login.html", data="Login details incorrect. Please try again")
        session['user_id'] = data['user_id']  # if matched, put the user on session variable.
        session['name'] = data['first_name'] + " " + data['last_name']
        role = data['role']
        session['role'] = role
        session['email'] = data['email']
        match role:  # render different page by role
            case 0:
                # staff
                return render_template('students.html')
            case 1:
                # Mentor
                return render_template('students.html')
            case 2:
                # Student
                user_id_ = session['user_id']
                user = StudentQueries.getStudentById(user_id_)
                if user[0]['placement_status'] ==3:
                    questions = QuestionQueries.getAll(user_id_)
                    for que in questions:
                        str = que['question'].replace('\r', '').replace('\n', '')
                        strjson = json.loads(str)
                        que['question'] = strjson
                    return render_template("question.html", questions=questions, errorMsg="Please complete our survey first")
                elif user[0]['placement_status'] ==1 :
                    return render_template("student/matchproject.html",message="Congratulations, you got an offer!")
                else:
                    studentSkills = StudentSkillQueries.getAllByStudentId(user_id_)
                    return render_template("register.html", user=user[0], studentSkills=studentSkills)

    else:  # if not matched, pop-up return error message
        return render_template("login.html", data="Login details incorrect. Please try again")


# user logout, email and role need to be passed, to match t
# he database stored data.
@userRoute.route("/users/logOut")
@login_require
def logOut():
    session['user_id'] = None  # if matched, put the user on session variable.
    session['name'] = None
    session['role'] = None
    session['email'] = None
    session.clear()

    return render_template('student/studentbase.html')

@userRoute.route('/users/checkPassword')
def checkPassword():
    id = request.args.get("id")
    password = request.args.get("oldpassword")
    userData = UsersQueries.getUserById(id)  # check if the email and role is matched
    if len(userData) > 0:
        data = userData[0]
        checkResult = MD5Helper.check_match(data['password'], password)
        if not checkResult:
            data = {"message": "user email doesn't exist", "code": "error"}
            return make_response(jsonify(data), 200)
        else:
            data = {"message": "ok", "code": "ok"}
            return make_response(jsonify(data), 200)


@userRoute.route('/users/resetpassword', methods=["post"])
def resetpassword():
    userId = request.form.get("userId")
    email = request.form.get("email")
    password = request.form.get("password")
    
    encrypted = MD5Helper.md5_encrypt(password);
    try:
        UsersQueries.changePassword(userId, encrypted)
        data = {'message': 'ok', 'code': 'ok'}
    except:
        data = {'message': 'Something wrong, please try again later', 'code': 'ERROR'}

    return make_response(jsonify(data), 200)