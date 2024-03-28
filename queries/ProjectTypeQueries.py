import db



def insert(type_name):
    sqlCommand = """INSERT INTO project_type ( type_name) VALUES ( '%s')""" % type_name
     
    id = db.DBOperatorInsertedId(sqlCommand)
    return id;


def getAll():
    sqlCommand = """SELECT * FROM project_type """
     
    result = db.DBOperator(sqlCommand)
    return result;


def update(id, type_name):
    sqlCommand = """UPDATE project_type SET type_name = '%s' WHERE id = '%s'""" \
                 % (type_name, id)
     
    result = db.DBOperatorInsertedId(sqlCommand)
    return result;


def delete(id):
    sqlCommand = """DELETE FROM project_type WHERE id = '%s'""" % id
     
    result = db.DBOperator_update(sqlCommand)
    return result;

