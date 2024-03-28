import db



def insert(skill_name):
    sqlCommand = """INSERT INTO techs_and_skills ( skill_name) VALUES ( '%s')""" % (skill_name)
     
    id = db.DBOperatorInsertedId(sqlCommand)
    return id


def getAll():
    sqlCommand = """SELECT * FROM techs_and_skills """
     
    selectResult = db.DBOperator(sqlCommand)
    return selectResult


def update(id, company_name):
    sqlCommand = """UPDATE techs_and_skills SET  skill_name = '%s' WHERE id = '%s'"""%(company_name,id)
     
    affectedRows = db.DBOperatorInsertedId(sqlCommand)
    return affectedRows


def delete(id):
    sqlCommand = """DELETE FROM techs_and_skills WHERE id = '%s'""" % id
     
    affectedRows = db.DBOperator_update(sqlCommand)
    return affectedRows
