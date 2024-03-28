import json

from flask import Blueprint, render_template, request, make_response, jsonify, session

from queries import QuestionAnswerQueries, StudentQueries

studentQuestionsRoute = Blueprint('studentQuestionsRoute', __name__)


@studentQuestionsRoute.route('/studentQuestions/getAll')
def get_users():
    questionAnswers = QuestionAnswerQueries.getAll()
    return render_template("stuQuestion.html", questionAnswers=questionAnswers)


@studentQuestionsRoute.route('/studentQuestions/getByStudentId')
def getByStudentId():
    id = request.args.get("studentId")
    questionAnswers = QuestionAnswerQueries.getByStudentId(id)
    data = {"message": "ok", "code": "ok", "data": questionAnswers}
    return make_response(jsonify(data), 200)


@studentQuestionsRoute.route('/studentQuestions/addQuestionAnswer',methods=['post'])
def addQuestionAnswer():
    uId = session['user_id']
    que_7 = request.form.getlist('que_7[]')
    otherQues = request.form
    que_8 = request.form.getlist('que_8[]')
    newDic = merge_dict_with_list(otherQues,que_7,"que_7[]")
    newDic = merge_dict_with_list(newDic,que_8,"que_8[]")


    QuestionAnswerQueries.delete(uId)
    questionAnswers = QuestionAnswerQueries.batchInsert(uId,newDic)
    StudentQueries.updatePlacementStatus(uId,0)

    data = {"message": "ok", "code": "ok", "data": questionAnswers}
    return make_response(jsonify(data), 200)

def merge_dict_with_list(dictionary, key_list,name):
    new_dict = dictionary.copy()
    newdict = new_dict.copy()
    key_list = [x for x in key_list]

    for key in new_dict:
        if key ==name:
            newdict.pop(key)
    newdict[name[:-2]] = ','.join(key_list)

    return newdict