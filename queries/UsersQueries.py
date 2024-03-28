import db


def insert(first_name: object, last_name: object, password: object, email: object, role: object) -> object:
    sqlCommand = """INSERT INTO user ( first_name, last_name, password, email, role)
         VALUES ('%s', '%s', '%s', '%s', '%s')""" % (
        first_name, last_name, password, email, role)
    result = db.DBOperatorInsertedId(sqlCommand)
    return result


def getAll():
    sqlCommand = """SELECT * FROM user"""
    result = db.DBOperator(sqlCommand)
    return result

def getAllByRole(role):
    sqlCommand = """SELECT * FROM user where role = %s """%role
    result = db.DBOperator(sqlCommand)
    return result


def update(id, first_name, last_name):
    sqlCommand = """UPDATE user SET first_name = '%s', last_name = '%s' WHERE user_id = '%s' """ % (
    first_name, last_name, id)

    selectResult = db.DBOperator_update(sqlCommand)
    return selectResult


def delete(id):
    sqlCommand = """DELETE FROM user WHERE user_id = '%s'""" % id
    selectResult = db.DBOperator_update(sqlCommand)
    return selectResult


def getUserByEmail(email):
    sqlCommand = """SELECT * FROM user where email = '%s' """ % (email)
    selectResult = db.DBOperator(sqlCommand)
    return selectResult

def updateprofile(id, first_name, last_name, email):
    sqlCommand = """UPDATE user SET first_name = '%s', last_name = '%s',
                    email = '%s'  WHERE user_id = '%s' """ % (first_name, last_name, email,id)
    selectResult = db.DBOperator_update(sqlCommand)
    return selectResult

def changePassword(id, password):
    sqlCommand = """UPDATE user SET password = '%s' WHERE user_id = '%s' """ % (password, id)
    selectResult = db.DBOperator_update(sqlCommand)
    return selectResult

def checkPassword(email,password):
    sqlCommand = """SELECT * FROM user where email = '%s' and password = '%s' """ % (email,password)
    selectResult = db.DBOperator(sqlCommand)
    return selectResult

def getUserById(id):
    sqlCommand = """SELECT * FROM user where User_id = '%s' """ % (id)
    selectResult = db.DBOperator(sqlCommand)
    return selectResult