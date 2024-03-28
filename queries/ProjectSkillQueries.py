import db


def insert(project_id, skill_id):
    sqlCommand = """INSERT INTO project_skills (project_id, skill_id) VALUES ('%s', '%s')""" % (project_id, skill_id)
     
    result = db.DBOperatorInsertedId(sqlCommand)
    return result;


def getAll():
    sqlCommand = """SELECT * FROM project_skills """
     
    result = db.DBOperator(sqlCommand)
    return result;


def update():
    return """UPDATE project_skills WHERE id = '%s'"""


def delete(project_id, skill_id):
    sqlCommand = """DELETE FROM project_skills WHERE project_id = '%s' and skill_id = '%s' """ % (project_id, skill_id)
     
    result = db.DBOperator_update(sqlCommand)
    return result;


def batchInsert(id,skiils ):
    sqlCommand = """INSERT INTO project_skills (project_id, skill_id) VALUES"""
    for val in skiils:
        sqlCommand += """  ('%s', '%s') ,""" % (id, val)
    sqlCommand = sqlCommand[:-1]

    print(sqlCommand)
    result = db.DBOperatorInsertedId(sqlCommand)
    return result

def getAllByProjectId(PId):
    sqlCommand = """
                SELECT
                    ts.id,
                    sk.project_id,
                    ts.skill_name 
                FROM
                    techs_and_skills ts
                    LEFT JOIN project_skills sk ON sk.skill_id = ts.id 
                    AND sk.project_id = %s
     """%PId

    result = db.DBOperator(sqlCommand)
    return result



def deleteAll(project_id):
    sqlCommand = """DELETE FROM project_skills WHERE project_id = '%s'""" % (project_id)

    result = db.DBOperator_update(sqlCommand)
    return result