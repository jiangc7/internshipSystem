import os

from flask import Flask, request, session, make_response, jsonify
from flask import render_template

from CompanyRoute import companyRoute
from InterviewRoute import interviewRoute
from MentorRoute import mentorRoute
from ProjectRoute import projectRoute
from ProjectSkillRoute import projectSkillRoute
from ProjectTypeRoute import projectTypeRoute
from QuestionRoute import questionRoute
from StudentProjectRoute import studentProjectRoute
from StudentQuestionAnswerRoute import studentQuestionsRoute
from StudentRoute import studentRoute
from StudentSkillRoute import studentSkillRoute
from TechSkillRoute import techSkillRoute
from UserRoute import userRoute
from MatchRoute import matchRoute
from queries import StudentQueries, StudentSkillQueries
from utils import MD5Helper
from SpeedInterviewRoute import speedInterviewRoute
import uuid
from flask import send_from_directory

app = Flask(__name__)
script_dir = os.path.dirname(os.path.abspath(__file__))
# 在该路径下创建uploads目录
app.config['UPLOAD_FOLDER'] = os.path.join(script_dir, 'uploads')

app.config['SECRET_KEY'] = os.urandom(24)
app.register_blueprint(companyRoute)
app.register_blueprint(userRoute)
app.register_blueprint(interviewRoute)
app.register_blueprint(studentRoute)
app.register_blueprint(mentorRoute)
app.register_blueprint(techSkillRoute)
app.register_blueprint(studentQuestionsRoute)
app.register_blueprint(questionRoute)
app.register_blueprint(projectTypeRoute)
app.register_blueprint(projectSkillRoute)
app.register_blueprint(projectRoute)
app.register_blueprint(studentProjectRoute)
app.register_blueprint(studentSkillRoute)
app.register_blueprint(matchRoute)
app.register_blueprint(speedInterviewRoute)


@app.route("/")  # home page
def home():
    return render_template("index.html")


@app.route("/register")  # home page
def register():
    id = session.__contains__('user_id')
    if id:
        user_id_ = session['user_id']
        user = StudentQueries.getStudentById(user_id_)
        if len(user) > 0:  # if found a row return ok , if nothing found return error
            data = {"message": "ok", "code": "ok", "data": user[0]}

        else:
            data = {"message": "User doesn't exist", "code": "ERROR"}
        if session['role'] == 2:
            studentSkills = StudentSkillQueries.getAllByStudentId(user_id_)
            return render_template("register.html", user=user[0], studentSkills=studentSkills)

        else:
            return render_template("register.html", user=user[0])
    else:
        return render_template("register.html")


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename



    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.mkdir(app.config['UPLOAD_FOLDER'])
    fileId = uuid.uuid4()
    name, extension = os.path.splitext(filename)
    filename = str(fileId) + extension
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)

    data = {'message': 'file uploaded', 'code': 'ok', "filename":filename}
    return make_response(jsonify(data), 200)


@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route("/about")
def about():
    return render_template("/about.html")


@app.route("/contact")
def contact():
    return render_template("/contact.html")


@app.route("/login")
def login():
    return render_template("/login.html")


@app.route("/project")
def project():
    return render_template("/project.html")


@app.route("/student")
def student():
    return render_template("student/studentbase.html")


@app.route("/mentor")
def mentor():
    return render_template("mentor/mentorbase.html")


@app.route("/staff")
def staff():
    return render_template("staff/staffbase.html")


@app.route("/forgotPassword")
def forgotPassword():
    email = request.args.get("key")
    return render_template("forgotPassword.html", email=email)


if __name__ == '__main__':
    app.run(debug=True)

@app.route("/staffreport")
def staffreport():
    return render_template("staff/staffreport.html")

@app.route("/staffreport1")
def staffreport1():
    return render_template("staff/staffreport1.html")

@app.route("/staffreport2")
def staffreport2():
    return render_template("staff/staffreport2.html")

@app.route("/staffreport3")
def staffreport3():
    return render_template("staff/staffreport3.html")

@app.route("/contact1")
def contact1():
    return render_template("contact.html")


