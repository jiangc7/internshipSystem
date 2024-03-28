import db

table_name = "t_question_answer"


def insert(student_id, question_id, question_answer):
    sqlCommand = """INSERT INTO question_answer (student_id, question_id, question_answer) VALUES ('%s', '%s', '%s')""" % (
        student_id, question_id, question_answer)

    id = db.DBOperatorInsertedId(sqlCommand)
    return id;


def getAll():
    sqlCommand = """SELECT * FROM question_answer """

    result = db.DBOperator(sqlCommand)
    return result;


def getByStudentId(studentId):
    sqlCommand = """SELECT
                        * 
                    FROM
                        question_answer qa
                        LEFT JOIN question qe ON qa.question_id = qe.id 
                    WHERE
                        student_id = %s """ % (studentId)

    result = db.DBOperator(sqlCommand)
    return result;


def update(student_id, question_id, question_answer):
    sqlCommand = """UPDATE question_answer SET  question_answer = '%s' WHERE student_id = '%s' and question_id = '%s' """ \
                 % (student_id, question_id, question_answer)

    result = db.DBOperatorInsertedId(sqlCommand)
    return result;


def delete(student_id):
    sqlCommand = """DELETE FROM question_answer WHERE student_id = '%s'""" % (
        student_id)

    result = db.DBOperator_update(sqlCommand)
    return result;


def batchInsert(id, formDatas):
    sqlCommand = """INSERT INTO question_answer (student_id, question_id, question_answer) VALUES"""
    for key in formDatas:
        queId = int(str(key).replace("que_", ""))
        sqlCommand += """  ('%s', '%s', '%s') ,""" % (id, queId, formDatas[key])
    sqlCommand = sqlCommand[:-1]

    print(sqlCommand)
    result = db.DBOperatorInsertedId(sqlCommand)
    return result
