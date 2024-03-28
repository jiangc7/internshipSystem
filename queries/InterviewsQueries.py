import db


def insert(uid,project_id, student_id, interview_date,time, interview_type, interview_status):
    sqlCommand = """INSERT INTO interviews (interviewer ,project_id, student_id, interview_date,interview_time, interview_type, interview_status)
    VALUES ('%s','%s', '%s', '%s', '%s', '%s', '%s')""" % (uid,project_id, student_id, interview_date,time, interview_type, interview_status)
     
    result = db.DBOperatorInsertedId(sqlCommand)
    return result


def getAll():
    sqlCommand = """SELECT * FROM interviews """
     
    result = db.DBOperator(sqlCommand)
    return result


def update(id, interview_status):
    sqlCommand = """UPDATE interviews SET interview_status = '%s' WHERE id= '%s'  """ \
                 % (interview_status, id)
     
    result = db.DBOperator(sqlCommand)
    return result


def delete(id):
    sqlCommand = """DELETE FROM interviews WHERE id = '%s'""" % id
     
    result = db.DBOperator_update(sqlCommand)
    return result
