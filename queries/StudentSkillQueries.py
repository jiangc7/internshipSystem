import db



def insert(student_id, skill_id):
    sqlCommand = """INSERT INTO student_skills ( student_id, skill_id) VALUES ('%s', '%s')""" \
                 % (student_id, skill_id)
     
    id = db.DBOperatorInsertedId(sqlCommand)
    return id


def getAll():
    sqlCommand = """SELECT * FROM student_skills """
     
    result = db.DBOperator(sqlCommand)
    return result


def batchInsert(id,skiils ):
    sqlCommand = """INSERT INTO student_skills (student_id, skill_id) VALUES"""
    for val in skiils:
        sqlCommand += """  ('%s', '%s') ,""" % (id, val)
    sqlCommand = sqlCommand[:-1]

    print(sqlCommand)
    result = db.DBOperatorInsertedId(sqlCommand)
    return result

def getAllByStudentId(sId):
    sqlCommand = """
                SELECT
                    ts.id,
                    sk.student_id,
                    ts.skill_name 
                FROM
                    techs_and_skills ts
                    LEFT JOIN student_skills sk ON sk.skill_id = ts.id 
                    AND sk.student_id = %s
     """%sId

    result = db.DBOperator(sqlCommand)
    return result


def delete(student_id, skill_id):
    sqlCommand = """DELETE FROM student_skills WHERE student_id = '%s' and skill_id = '%s'""" %(student_id, skill_id)
     
    result = db.DBOperator_update(sqlCommand)
    return result


def deleteAll(student_id):
    sqlCommand = """DELETE FROM student_skills WHERE student_id = '%s'""" % (student_id)

    result = db.DBOperator_update(sqlCommand)
    return result
